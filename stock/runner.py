from dataBase import connection, build, insert
from dataCollection import company_Collection, financial_collection
import datetime
import time
from itools import date_Change


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
        companyid_List.append((company_Id, company_Place))
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
    print(alldate)
    # alldate代表前三年的全部日期，格式为数字，字符串
    print("→" * 50)
    family = ('balancesheet', 'incomestatements',
              'cashflow', 'financialreport')
    for id in companyid_List:
        for f in family:
            url = "http://www.cninfo.com.cn/information/%s/%s%s.html" % (
                f, id[1], id[0])
            print(url)
            date, data = financial_collection(
                url, '2016', '-12-31', f, id[0])
            # 此处的日期可以随意填写，都会返回最新的报表数据的日期date
            dateYear = date[:4]
            dateMonth = date[4:]
            dateYear, dateMonth = date_Change(dateYear, dateMonth)
            # date_Change返回的值均为字符串，因此在进行移除时，需要把dateYear转成数值格式
            d = alldate
            print(dateYear, dateMonth)
            print("-" * 100)
            try:
                d.remove((int(dateYear), dateMonth))
            except:
                dd = []
                for j in d:
                    if j[0] != datetime.date.today().year - 3:
                        dd.append(j)
                d = dd
            print(d)
            print("-" * 100)
            url = 'http://www.cninfo.com.cn/information/stock/{0}_.jsp?stockCode={1}'.format(
                f, id[0])
            for i in d:
                jud = True
                while jud:
                    date, data = financial_collection(
                        url, i[0], i[1], f, id[0])
                    dateYear, dateMonth = date_Change(date[:4], date[4:])
                    print(id[0], (int(dateYear), dateMonth), i)
                    if i == (int(dateYear), dateMonth):
                        break
                insert(data)
                print("-" * 100)
            print("=" * 100)
        print("*" * 100)


if __name__ == "__main__":
    run()
