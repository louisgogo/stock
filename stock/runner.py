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
    alldate = []
    for i in year:
        for j in mm:
            alldate.append((i, j))
    if 4 <= datetime.date.today().month:
        alldate.append((datetime.date.today().year, '-03-31'))
        if 7 <= datetime.date.today().month:
            alldate.append((datetime.date.today().year, '-06-30'))
            if 9 <= datetime.date.today().month:
                alldate.append((datetime.date.today().year, '-09-30'))
    alldate = set(alldate)
    print(alldate)
    family = ('balancesheet', 'incomestatements',
              'cashflow', 'financialreport')
    for id in companyid_List:
        for f in family:
            url = "http://www.cninfo.com.cn/information/%s/szmb%s.html" % (
                f, id)
            date = financial_collection(
                url, '2016', '-12-31', f, id)
            # 此处的日期可以随意填写，都会返回最新的报表数据的日期date
            dateYear = date[:3]
            dateMonth = date[4:]


if __name__ == "__main__":
    run()
