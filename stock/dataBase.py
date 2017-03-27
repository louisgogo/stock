import pymysql


def connection():
    conn = pymysql.connect(host='127.0.0.1', port=3306,
                           user='root', passwd='888888', db='mysql', charset='utf8')
    cur = conn.cursor()
    try:
        cur.execute("USE stock")
    except Exception as e:
        pass
    return conn


def build():
    conn = connection()
    cur = conn.cursor()
    try:
        cur.execute("DROP DATABASE stock")
        cur.execute('CREATE DATABASE stock')
        print("删除旧数据库并建立新数据库")
    except Exception as e:
        cur.execute('CREATE DATABASE stock')
        print("新建立数据库")
    # 建立数据库表格
    cur.execute("USE stock")
    # 建立数据表格：公司列表（股票代码，公司名称，行业类别），资产负债表（股票代码，科目名称，金额<借方正数，贷方负数>，单位，所属年份，所属报告期），利润表（股#票代码，科目名称，金额<贷方正数，借方负数>，单位，所属年份，所属报告期），现金流量表（股票代码，项目名称，金额<借方正数，贷方负数>，单位，所属年份，所属报告期），公司综合能力指标（股票代码，项目名称，数值，单位，所属年份，所属报告期）
    try:
        cur.execute('CREATE TABLE company (row_Id BIGINT(10) NOT NULL AUTO_INCREMENT,company_Id VARCHAR(200) NOT NULL,company_Name VARCHAR(200),company_Place VARCHAR(100),company_Industry VARCHAR(600),created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY (row_Id,company_Id))')
        cur.execute("CREATE TABLE financialsheet (row_Id BIGINT(10) NOT NULL AUTO_INCREMENT,company_Family VARCHAR(200),company_Id VARCHAR(200) NOT NULL,accounting VARCHAR(600),amount DECIMAL(15,2),unit VARCHAR(10),year VARCHAR(20),period VARCHAR(20),created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY (row_Id,company_Id))")
        print("数据库建立完毕")
    except (AttributeError):
        print('TABLE已经存在')
    cur.close()
    conn.close()

if __name__ == '__main__':
    build()
