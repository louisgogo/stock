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
                        count = -1
                        proxy = 0
                        print("重新循环各个代理地址")
                        # sys.exit("代理服务地址用完，退出程序")
                    print(ip[count])


if __name__ == "__main__":
    ip = ['216.56.48.245:80',
          '216.56.48.247:80',
          '216.56.48.243:80',
          '216.56.48.248:80',
          '63.150.152.151:3128',
          '63.150.152.151:8080',
          '210.35.171.5:80',
          '58.97.81.11:80'
          ]
    run(ip)
