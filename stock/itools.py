import requests
from lxml import etree
import re
import os
import zipfile
from selenium import webdriver


def web_Reader(url, headers, data):
    # 读取网页内容
    s = requests.Session()
    s.keep_alive = False
    count = 0
    while True:
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
        # 判断压缩包是否已经损坏
        try:
            zipfile.ZipFile(filePath, "r")
        except:
            os.remove(filePath)
        id = i.split('_')[2]
        family = i.split('_')[1]
        idFamily.append((id, family))
    print("空文件清理完毕")
    return idFamily


def vpn_List():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("http://www.gatherproxy.com/en/proxylist/anonymity/?t=Anonymous")
    js = "var q=document.body.scrollTop=500"
    driver.execute_script(js)
    driver.find_element_by_tag_name("input").click()
    # 读取具体的页码
    count = len(driver.find_elements_by_xpath(
        "//div[@class='pagenavi']/a")) + 1
    ipList = []
    for a in range(1, count + 1):
        js = "var q=document.body.scrollTop=100000"
        driver.execute_script(js)
        try:
            driver.find_element_by_link_text(str(a)).click()
        except:
            pass
        html = etree.HTML(driver.page_source)
        content = html.xpath(
            '//div[@class="proxy-list"]/table//tr')
        for tr in content:
            try:
                td = tr.xpath('./td//text()')
                print(td)
                if int(re.search('(.*)ms', td[10]).group(1)) <= 300 and int(td[7]) > 100:
                    ip = td[2] + ':' + td[4]
                    ipList.append(ip)
            except:
                pass
    with open('vpn.txt', 'w') as f:
        for i in ipList:
            f.write(i + '\n')
    return ipList


if __name__ == '__main__':
    ipList = vpn_List()
    # idFamily = file_Del()
    # print(idFamily)
    # print(('000001', 'lrb') in idFamily)
    # dateYear, dateMonth = date_Change('2016', '-09-30')
    # print(dateYear, dateMonth)
    family = 'balancesheet'
    company_Id = '000002'
    # url = "http://www.cninfo.com.cn/information/%s/szmb%s.html" % (
    #    family, company_Id)
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
    # web_Reader(url, headers, data)
