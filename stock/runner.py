from dataBase import connection, build
from dataCollection import company_Collection, financial_collection
import datetime
import time


def run():
    companyid_List = []
    build()
    conn = connection()
    cur = conn.cursor()
    company_Collection()
    cur.execute('select company_Id,company_Name,company_Place from company')
    result = cur.fetchall()
    for i in list(result):
        company_Id, company_Name, company_Place = i
        companyid_List.append(company_Id)
    print(companyid_List)
    year = (datetime.date.today().year - 1, datetime.date.today().year -
            2, datetime.date.today().year - 3)
    mm = ('-12-31', '-09-30', '-06-30', '-03-31')
    family = ('balancesheet', 'incomestatements',
              'cashflow', 'financialreport')
    for id in companyid_List:
        for f in family:
            url = "http://www.cninfo.com.cn/information/%s/szmb%s.html" % (
                f, id)
            date = financial_collection(
                url, '2016', '-12-31', 'f', 'id')


if __name__ == "__main__":
    run()
