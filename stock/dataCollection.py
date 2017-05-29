from dataBase import connection
import requests
from bs4 import BeautifulSoup
import re
from lxml import etree
from itools import web_Reader, date_Change
import os
import json
import datetime
import zipfile

conn = connection()
cur = conn.cursor()


def company_Collection():
    company = []
    url = 'http://www.cninfo.com.cn/cninfo-new/information/companylist'
    headers = {
        'Host': 'www.cninfo.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/css,*/*;q=0.1',
        'Connection': 'keep-alive'
    }
    condition = True
    while condition:
        try:
            html = requests.get(url, headers=headers)
            html.encoding = "utf-8"
            BsObj = BeautifulSoup(html.text, 'html.parser')
            companyList_SZ = BsObj.find(
                "div", {'id': 'con-a-1'}).findAll("li")
            companyList_ZX = BsObj.find(
                "div", {'id': 'con-a-2'}).findAll("li")
            companyList_CY = BsObj.find(
                "div", {'id': 'con-a-3'}).findAll("li")
            companyList_SH = BsObj.find(
                "div", {'id': 'con-a-4'}).findAll("li")
            if html.status_code == 200:
                condition = False
        except Exception as e:
            print("网页读取有问题：", e)
    for i in companyList_SZ:
        i = i.get_text()
        company_Id = re.search(re.compile(
            "([0-9]+) (.+)"), i).group(1)
        company_Name = re.search(re.compile(
            "([0-9]+) (.+)"), i).group(2).strip()
        company_Place = "szmb"
        company.append((company_Id, company_Name, company_Place))
    for i in companyList_ZX:
        i = i.get_text()
        company_Id = re.search(re.compile(
            "([0-9]+) (.+)"), i).group(1)
        company_Name = re.search(re.compile(
            "([0-9]+) (.+)"), i).group(2).strip()
        company_Place = "szsme"
        company.append((company_Id, company_Name, company_Place))
    for i in companyList_CY:
        i = i.get_text()
        company_Id = re.search(re.compile(
            "([0-9]+) (.+)"), i).group(1)
        company_Name = re.search(re.compile(
            "([0-9]+) (.+)"), i).group(2).strip()
        company_Place = "szcn"
        company.append((company_Id, company_Name, company_Place))
    for i in companyList_SH:
        i = i.get_text()
        company_Id = re.search(re.compile(
            "([0-9]+) (.+)"), i).group(1)
        company_Name = re.search(re.compile(
            "([0-9]+) (.+)"), i).group(2).strip()
        company_Place = "shmb"
        company.append((company_Id, company_Name, company_Place))
    sql = "INSERT INTO company(company_Id,company_Name,company_Place) VALUES (%s,%s,%s) "
    cur.executemany(sql, company)
    conn.commit()


def data_Collection(content, family, company_Id, unit):
    # 收集并存储股票信息
    data = []
    period = content[1]
    if family in ('incomestatements', 'balancesheet', 'cashflow'):
        for i in range(4, len(content), 2):
            if content[i + 1] == '\xa0':
                pass
            else:
                if "合计" not in content[i]:
                    if "总计" not in content[i]:
                        if "小计" not in content[i]:
                            if content[i + 1] == ' ':
                                content[i + 1] = 0
                            else:
                                content[
                                    i + 1] = str(content[i + 1]).replace(",", "")
                            data.append(
                                (family, company_Id, content[i], content[i + 1], unit, period))
    else:
        for i in range(4, len(content), 3):
            if content[i + 2] == "\xa0":
                pass
            else:
                if "合计" or "总计" or "小计" not in content[i]:
                    if content[i + 2] == ' ':
                        content[i + 2] = 0
                    else:
                        content[i + 2] = content[i + 2].replace(",", "")
                    data.append(
                        (family, company_Id, content[i], content[i + 2], unit, period))
    # print(data)
    return data


def financial_collection(url, year, mm, family, company_Id):
    # type可选参数包括：incomestatements，balancesheet，cashflow，financialreport，注意变更url和data中对应的参数;
    # year格式：2015；mm格式：-12-31，-09-30，-06-30，-03-31
    headers = {
        'Host': 'www.cninfo.com.cn',
        'Connection': 'keep-alive',
        'Content-Length': '61',
        'Cache-Control': 'max-age=0',
        'Origin': 'http://www.cninfo.com.cn',
        U'pgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'DNT': '1',
        # 'Referer': 'http://www.cninfo.com.cn/information/%s/szmb%s.html' % (family, company_Id),
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
    }
    data = {'yyyy': year,
            'mm': mm,
            'cwzb': family,
            'button2': '�ύ'
            }
    content, unit = web_Reader(url, headers, data)
    data = data_Collection(content, family, company_Id, unit)
    return content[1], data


def data_Down(stocktype, code, proxy, ip):
    # 'market': 'sz','type': 'lrb'|'fzb','code': '000001','orgid': 'gssz0000001',
    # 'minYear': '2015','maxYear': '2017','cw_code': '000001'
    headers = {
        'Host': 'www.cninfo.com.cn',
        'Connection': 'keep-alive',
        'Content-Length': '61',
        'Cache-Control': 'max-age=0',
        'Origin': 'http://www.cninfo.com.cn',
        U'pgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'DNT': '1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
    }
    # 提取出该股票代码的最早的报表年份
    data = {'keyWord': code,
            'maxNum': 10,
            'hq_or_cw': 2
            }
    url = 'http://www.cninfo.com.cn/cninfo-new/data/query'
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.Session()
    s.keep_alive = False
    while True:
        try:
            html = s.post(url, headers=headers,
                          allow_redirects=True, data=data)
            info = json.loads(html.text)
        except Exception as e:
            print("dataDown-001出现问题，重新执行，问题原因：", e)
        else:
            break
    if info == []:
        print("该公司信息不存在")
        return False
    info = info[0]
    minYear = info['startTime']
    maxYear = datetime.date.today().year
    market = info['market']
    orgid = info['orgId']

    # 提取出对应的报表数据
    data = {'market': market,
            'type': stocktype,
            'code': code,
            'orgid': orgid,
            'minYear': minYear,
            'maxYear': maxYear,
            'cw_code': code
            }
    url = 'http://www.cninfo.com.cn/cninfo-new/data/download'
    s = requests.Session()
    s.keep_alive = False
    title = market + '_' + stocktype + '_' + code + \
        '_' + str(minYear) + '_' + str(maxYear)
    # count用来统计错误的次数
    count = 0
    while True:
        try:
            if count == 5:
                print("尝试次数到上限，更换下一个代理地址！")
                return True
            if proxy == 1:
                proxies = {"http": "http://" + ip,
                           "https": "https://" + ip
                           }
                html = s.post(url, headers=headers,
                              allow_redirects=True, data=data, proxies=proxies)
            else:
                html = s.post(url, headers=headers,
                              allow_redirects=True, data=data)
        except Exception as e:
            print("dataDown-002出现问题，重新执行，问题原因：", e)
            count += 1
        else:
            break
    path = os.path.join(os.path.dirname(__file__) + '\data\%s.zip' % title)
    with open(path, "wb") as code:
        code.write(html.content)
        print(title, "文件生成完毕")
    try:
        zipfile.ZipFile(path, "r")
    except:
        os.remove(path)
        print("压缩包已经损坏，进行删除")
        return True
    print(os.path.getsize(path))
    return False


if __name__ == "__main__":
    # data_Down('fzb', '000005', 0, '201.236.222.231:8080')
    family = 'balancesheet'
    company_Id = '000002'
    url = "http://www.cninfo.com.cn/information/%s/szmb%s.html" % (
        family, company_Id)
    date = financial_collection(
        url, 2014, '-12-31', 'balancesheet', 'company_Id')
    print(date)
    company_Id = '000001'
    url = 'http://www.cninfo.com.cn/information/stock/{0}_.jsp?stockCode={1}'.format(
        family, company_Id)
    financial_collection(url, 2015, '-12-31', 'balancesheet', 'company_Id')
