import time,sys,pytest
from selenium import webdriver
from Conf.setting import Setting
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
set =Setting()



# class Screen(object):
#     def __init__(self, driver):
#         self.driver = driver
#     def __call__(self, f):
#         def inner(*args,**kwargs):
#             try:
#                 return f(*args,**kwargs)
#             except:
#                 #nowTime = time.strftime("%Y_%m_%d_%H_%M_%S")
#                 self.driver.get_screenshot_as_file(set.Pic_DIR+sys._getframe().f_code.co_name+"error.png")
#                 res =False
#             assert bool(res)==True
#         return inner


class TestCookies():

    def setup_class(self):
        self.driver = webdriver.Chrome(executable_path="D:\selenium_uses\driver\chromedriver.exe") #可执行路径
        bd_url = "https://www.baidu.com/"
        self.driver.get(bd_url)
        self.driver.maximize_window()
        time.sleep(2)

    def teardown_class(self):
        self.driver.quit()

    def test_cookies(self):
        try:
            bd_cookies =self.driver.get_cookies()
            print("\n 百度cookies:", bd_cookies)
            assert isinstance(bd_cookies,list)
            assert bd_cookies[0].get('domain') == '.1baidu.com'
            assert bd_cookies[-1].get('domain') =='www.baidu.com'
            print(bd_cookies[-1].get('name1')==None) #推荐用get(key)的写法
            print(bd_cookies[-1].get('value'))
            #self.driver.add_cookie({'name':'chendamao','value':'222333'})
            self.driver.get("https://www.taobao.com/")
            Tmao_cookies = self.driver.get_cookies()
            print("天猫的作用域",Tmao_cookies[-1].get('domain'))
            print("\n 天猫cookies:", Tmao_cookies)
            self.driver.add_cookie({'name':"chendmao","value":"BOjoQ99tIPrbDQx-V2GmuZlgudY6uU1-PZy8d6IZNGNW_YhnSiEcq34_8ZQNTQTz"})
            print(Tmao_cookies[-1].get('value'))
            add_name =self.driver.get_cookie("chendmao")
            print("追加的信息",add_name)
            self.driver.delete_all_cookies()
            add_name1 = self.driver.get_cookie("chendmao")
            print("追加的信息", add_name1)
            res = True
        except Exception as err:
            res =False
            print(err)
        assert res ==True

# if __name__ == '__main__':
#     pytest.main([r'D:\selenium_uses\test_case_pytest\test_cookies', '-v', r'--html=D:\selenium_uses\test_case_pytest\1.html'])

