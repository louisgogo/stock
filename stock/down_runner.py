from dataBase import connection, build, insert
from dataCollection import company_Collection, data_Down
from itools import file_Del, vpn_List
import sys
import socket
import time

timeout = 20
socket.setdefaulttimeout(timeout)


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
    # 此处count用于统计使用的代理的序号
    count = -1
    for id in companyid_List:
        for f in family:
            if (id[0], f) not in idFamily:
                print("=" * 50)
                print(f, id[0])
                while data_Down(f, id[0], proxy, ip[count]):
                    count += 1
                    print("-" * 50)
                    print("启用代理服务器，继续采集")
                    proxy = 1
                    if len(ip) == count:
                        print("重新获取代理地址，继续执行程序")
                        return True
                    print(ip[count])
    print("所有数据采集完毕，程序自动退出")
    return False


if __name__ == "__main__":
    ip = vpn_List()
    while run(ip):
        time.sleep(1800)
        ip = vpn_List()
