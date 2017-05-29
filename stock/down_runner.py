from dataBase import connection, build, insert
from dataCollection import company_Collection, data_Down
from itools import file_Del
import sys


def run(ip):
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
    idFamily = file_Del()
    # 删除空的压缩包，并生成已下载的列表
    proxy = 0
    # 不启动代理服务器
    family = ('fzb', 'lrb', 'llb')
    for id in companyid_List:
        for f in family:
            if (id[0], f) not in idFamily:
                print(f, id[0])
                if data_Down(f, id[0], proxy, ip[0]) == 14203:
                    if len(ip) == 0:
                        sys.exit("代理服务地址用完，退出程序")
                    print("启用代理服务器，继续采集")
                    proxy = 1
                    data_Down(f, id[0], proxy, ip[0])
                    print(ip[0])
                    ip.remove(ip[0])
                    idFamily = file_Del()


if __name__ == "__main__":
    ip = ['201.236.222.231:8080', '109.169.6.152:8080', '5.135.195.166:3128']
    run(ip)
