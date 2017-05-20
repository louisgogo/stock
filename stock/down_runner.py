from dataBase import connection, build, insert
from dataCollection import company_Collection, dataDown


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
    family = ('fzb', 'lrb', 'llb')
    for id in companyid_List:
        for f in family:
            print(f, id[0])
            dataDown(f, id[0])


if __name__ == "__main__":
    run()
