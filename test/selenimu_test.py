import  time

from selenium import webdriver
import  requests
# broswer = webdriver.Chrome(executable_path= r"D:/Python/Python35/Scripts/chromedriver.exe")
# broswer.get('http://www.baidu.com')
# print(broswer.page_source)
#
# time.sleep(10)
#
# res = requests.get('https://bbs.csdn.net/forums/ios')
# print(res.text)
import datetime
# str转时间格式：
dd = '2019-03-17 11:00:00'
dd = datetime.datetime.strptime(dd, "%Y-%m-%d %H:%M:%S")
print(dd,type(dd))