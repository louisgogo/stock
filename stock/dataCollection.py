from dataBase import connection
import requests
from bs4 import BeautifulSoup
import re

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
    cur.close()
    conn.close()


def financial_collection(year, mm, family, company_Id):
    url = 'http://www.cninfo.com.cn/information/stock/{0}_.jsp?stockCode={1}'.format(
        family, company_Id)
    # type可选参数包括：incomestatements，balancesheet，cashflow，financialreport，注意变更url和data中对应的参数;
    # year格式：2015；mm格式：-12-31，-09-30，-06-30，-03-31
    headers = {
        'Host': 'www.cninfo.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/css,*/*;q=0.1',
        'Connection': 'keep-alive'
    }
    data = {'yyyy': year,
            'mm': mm,
            'cwzb': family
            }
    html = requests.post(url, headers=headers,
                         allow_redirects=False, data=data)
    print(html.encoding)
    html.encoding = 'gbk'
    print(html.text)

if __name__ == "__main__":
    company_Collection()
    financial_collection('2015', '-12-31', 'balancesheet', '000002')
