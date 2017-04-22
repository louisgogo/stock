from dataBase import connection
import requests
from bs4 import BeautifulSoup
import re
from lxml import etree
import time

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
        company_Place = "深市主板"
        company.append((company_Id, company_Name, company_Place))
    for i in companyList_ZX:
        i = i.get_text()
        company_Id = re.search(re.compile(
            "([0-9]+) (.+)"), i).group(1)
        company_Name = re.search(re.compile(
            "([0-9]+) (.+)"), i).group(2).strip()
        company_Place = "中小企业板"
        company.append((company_Id, company_Name, company_Place))
    for i in companyList_CY:
        i = i.get_text()
        company_Id = re.search(re.compile(
            "([0-9]+) (.+)"), i).group(1)
        company_Name = re.search(re.compile(
            "([0-9]+) (.+)"), i).group(2).strip()
        company_Place = "创业板"
        company.append((company_Id, company_Name, company_Place))
    for i in companyList_SH:
        i = i.get_text()
        company_Id = re.search(re.compile(
            "([0-9]+) (.+)"), i).group(1)
        company_Name = re.search(re.compile(
            "([0-9]+) (.+)"), i).group(2).strip()
        company_Place = "沪市主板"
        company.append((company_Id, company_Name, company_Place))
    sql = "INSERT INTO company(company_Id,company_Name,company_Place) VALUES (%s,%s,%s) "
    cur.executemany(sql, company)
    conn.commit()


def financial_collection(year, mm, family, company_Id):
    url = 'http://www.cninfo.com.cn/information/stock/{0}_.jsp?stockCode={1}'.format(
        family, company_Id)
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
        'Referer': 'http://www.cninfo.com.cn/information/%s/szmb%s.html' % (family, company_Id),
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
    }
    data = {'yyyy': year,
            'mm': mm,
            'cwzb': family,
            'button2': '�ύ'
            }
    s = requests.Session()
    count = 0
    while True:
        time.sleep(1)
        try:
            count += 1
            html = s.post(url, headers=headers,
                          allow_redirects=True, data=data)
            html = s.get(url, headers=headers,
                         allow_redirects=False, data=data)
            html.encoding = 'gbk'
            html = etree.HTML(html.content)
            content = html.xpath(
                '//div[@class="zx_left"]/div[@class="clear"]/table/tr/td[not(@rowspan)]//text()')
            unit = html.xpath(
                '//div[@class="zx_left"]/div[@class="zx_right_title"]/p//text()')
            unit = re.search(re.compile('\(单位：(.+)\)'), str(unit)).group(1)
        except Exception as e:
            print(e, "出现问题，重新执行")
            time.sleep(2)
            if count >= 10:
                print("数据采集有问题，跳过该数据继续采集...")
                break
        else:
            break
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
    print(data)
    sql = "INSERT INTO financialsheet(company_Family,company_Id,accounting,amount,unit,period) VALUES (%s,%s,%s,%s,%s,%s) "
    cur.executemany(sql, data)
    conn.commit()


if __name__ == "__main__":
    financial_collection('2016', '-12-31', 'balancesheet', '000001')
