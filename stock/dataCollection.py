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
    while True:
        try:
            html = requests.get(url, headers=headers)
            html.encoding = "utf-8"
            BsObj = BeautifulSoup(html.text, 'html.parser')
            companyList = BsObj.findAll("ul", {'class': 'company-list'})
            print(html.status_code)
        except Exception as e:
            print("网页读取有问题：", e)
        else:
            break
    for i in companyList:
        company_Id = re.findall(re.compile(
            "([0-9]+)(.+)"), i.get_text())
        company_Name = re.findall(re.compile(
            "([0-9]+)(.+)"), i.get_text())
        company.append((company_Id, company_Name))
    print(company)


if __name__ == "__main__":
    company_Collection()
