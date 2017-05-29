import requests
import time
from lxml import etree
import re
import os


def web_Reader(url, headers, data):
    # 读取网页内容
    s = requests.Session()
    count = 0
    while True:
        time.sleep(0)
        try:
            count += 1
            html = s.post(url, headers=headers,
                          allow_redirects=True, data=data)
            html.encoding = 'gbk'
            html = etree.HTML(html.content)
            content = html.xpath(
                '//div[@class="zx_left"]/div[@class="clear"]/table/tr/td[not(@rowspan)]//text()')
            unit = html.xpath(
                '//div[@class="zx_left"]/div[@class="zx_right_title"]/p//text()')
            unit = re.search(re.compile('\(单位：(.+)\)'), str(unit)).group(1)
        except Exception as e:
            print(e, "出现问题，重新执行")
            time.sleep(3)
            if count >= 50:
                print("数据采集有问题，跳过该数据继续采集...")
                break
        else:
            break
    return content, unit


def date_Change(dateYear, dateMonth):
    dateDict = {'年度': '-12-31', '年1-3月': '-03-31', '年1-6月': '-06-30',
                '年1-9月': '-09-30', '一季': '-03-31', '中期': '-06-30', '三季': '-09-30'}
    try:
        dateMonth = dateDict[dateMonth]
    except Exception as e:
        print(e)
        pass
    dateYear = int(dateYear)
    return dateYear, dateMonth


def file_Del():
    idFamily = []
    path = os.path.dirname(__file__) + '\data'
    fileList = os.listdir(path)
    for i in fileList:
        filePath = os.path.dirname(__file__) + '\data\%s' % i
        if os.path.getsize(filePath) == 14203:
            os.remove(filePath)
        id = i.split('_')[2]
        family = i.split('_')[1]
        idFamily.append((id, family))
    print("空文件清理完毕")
    return idFamily


if __name__ == '__main__':
    idFamily = file_Del()
    print(idFamily)
    print(('000001', 'lrb') in idFamily)
    dateYear, dateMonth = date_Change('2016', '-09-30')
    print(dateYear, dateMonth)
    family = 'balancesheet'
    company_Id = '000002'
    url = "http://www.cninfo.com.cn/information/%s/szmb%s.html" % (
        family, company_Id)
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
    data = {'yyyy': '2016',
            'mm': '-12-31',
            'cwzb': family,
            'button2': '�ύ'
            }
    web_Reader(url, headers, data)
