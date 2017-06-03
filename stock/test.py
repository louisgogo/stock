from selenium import webdriver
from lxml import etree
import re

with open('vpn.txt', 'r') as f:
    ip = f.readlines
print(ip)

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get("http://www.gatherproxy.com/en/proxylist/anonymity/?t=Anonymous")
js = "var q=document.body.scrollTop=500"
driver.execute_script(js)
driver.find_element_by_tag_name("input").click()
# 读取具体的页码
count = len(driver.find_elements_by_xpath("//div[@class='pagenavi']/a")) + 1
ipList = []
for a in range(2, count + 1):
    js = "var q=document.body.scrollTop=100000"
    driver.execute_script(js)
    driver.find_element_by_link_text(str(a)).click()
    html = etree.HTML(driver.page_source)
    content = html.xpath(
        '//div[@class="proxy-list"]/table//tr')
    for tr in content:
        try:
            td = tr.xpath('./td//text()')
            if int(re.search('(.*)ms', td[10]).group(1)) <= 350:
                ip = td[2] + ':' + td[4]
                ipList.append(ip)
        except:
            pass
print(ipList)
with open('vpn.txt', 'w') as f:
    for i in ipList:
        f.write(i + '\n')
