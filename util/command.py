
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains #按键操作链
from selenium.webdriver.support import expected_conditions as EC #核心模块 期望场景是否存在
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
import os,time,sys
from util.Base import Base
from config.setting import Setting
set =Setting() #常量类不合适继承

"""
pytest新版的webdriver工具类
2019年
"""

class Command(Base):

    path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    stuite_path = path + os.sep + "test_case_pytest"

    def start_brower(self,base_url):
        chromedriver = self.get_ini_date("config", "Drivers", "chrome")
        self.driver = webdriver.Chrome(chromedriver)
        self.driver.get(base_url) #"http://www.ctrip.com/"
        self.driver.implicitly_wait(10)
        return self.driver

    def if_enabled(self,loated):
        """
        判断能否操作（操作包含:待填）
        :param loated:
        :return:
        """
        element =self.find_element_wait(loated)
        if element.is_enabled():
            return True
        else:
            return False


    def set_wins_size(self, wide, high):
        """
        设置窗体大小
        :param wide:宽
        :param high:高
        :return:
        """
        self.driver.set_window_size(wide, high)

    def click_element(self, located):
        """
        单击按钮
        组合用也可以拆开用
        :param located:定位器
        :return:
        """
        find_ele = self.find_element_wait(located)
        if find_ele:
            for i in range(2):
                find_ele.click()


    def double_click_element(self, located):
        """
        双击按钮
        组合用也可以拆开用
        :param located:定位器
        :return:
        """
        find_ele = self.find_element_wait(located)
        ActionChains(self.driver).double_click(find_ele).perform()

    def right_click_element(self, located):
        """
        对元素右键点击操作
        :param located:
        :return:
        """
        find_ele = self.find_element_wait(located)
        ActionChains(self.driver).context_click(find_ele).perform()

    def click_linktext(self, text):
        """
        单击link带链接属性的
        定位器选择用partial包含模糊模式
        :param text:
        :return:
        """
        self.driver.find_element_by_partial_link_text(text).click()

    def F5(self):
        """
        当前页面进行刷新
        :return:
        """

        self.driver.refresh()

    def get_attribute(self, located, attribute):
        """
        获取元素的属性
        :param located:
        :param attribute:
        :return:
        """
        element =self.find_element_wait(located)
        return element.get_attribute(attribute)

    def get_element_text(self, located):
        """
        获取元素的文本
        :param located:定位器 tuple=>str
        :return:
        """
        element = self.find_element_wait(located)
        return element.text

    def switch_to_handler(self,src_handle):
        """
        切换wins句柄
        use:前面需要获取一次句柄src_handle 才能套用这个函数
        :param src_handle:最终要切换句柄
        :return:
        """
        all_handle =self.driver.window_handles
        for handle in all_handle:
            if handle != src_handle: #如果不等于它
                self.driver.switch_to.window(src_handle) #切换


    def get_url_cookies(self,index,cookie_key):
        """
        获取网页的cookies list对象，返回对应下标后，获取内层字典的属性
        :param index:int   0...-1
        :param cookie_key: str 内层属性
        :return:str
        """
        url_cookies =self.driver.get_cookies()
        assert isinstance(url_cookies, list)
        return url_cookies[0].get(cookie_key)

    def switch_to_frame(self, located):
        """
        切换到frame
        :param located:
        :return:
        """
        iframe_element = self.find_element_wait(located)
        self.driver.switch_to.frame(iframe_element)

    def switch_to_frame_out(self):
        """
        返回上一个层级
        等于上面switch_to_frame的返回
        :return:
        """
        self.driver.switch_to.default_content()

    def get_element_display(self, located):
        """
        获取要显示的元素
        :param located:
        :return:boolean
        """
        element = self.find_element_wait(located)
        return element.is_displayed()


    def submit(self,located):
        """
        提交表单时,行为是元素.submit()
        :param located:
        :return:
        """
        element = self.find_element_wait(located)
        element.submit()

    def get_current_title(self):
        """
        获取当前网页的title
        :return:
        """
        return self.driver.title


    def get_current_url(self):
        """
        获取当前的网页
        :return:
        """
        return self.driver.current_url

    def find_wait_alert(self):
        """
        寻找等待alert事件出现
        self.find_wait_alert().text
        :return:alert element
        """
        alert =WebDriverWait(self.driver,10).until(EC.alert_is_present())
        return alert

    def find_wait_alert_text(self):
        """
        寻找等待alert事件出现的子方法
        :return:
        """
        alert =WebDriverWait(self.driver,10).until(EC.alert_is_present())
        return alert.text

    def find_wait_alert_accept(self):
        """
        寻找等待alert事件出现的子方法
        :return:
        """
        alert =WebDriverWait(self.driver,10).until(EC.alert_is_present())
        if alert: #内存是否消失
            return alert.accept

    def is_element_selected(self,located,element=None,mode=True):
        """
        *不佳的封装  判断元素是否可以被选中
        user:
        is_element_selected('css=>#c_ph_login') 方式一
        is_element_selected('',with上文的元素对象,mode=False) 方式二 located ='' 反正走不到上面分支
        :param located: 定位到的元素
        :return:boolean
        """
        #原型是_find_element(driver, self.locator).is_selected()
        if mode:
            return WebDriverWait(self.driver, 10).until(
                EC.element_located_to_be_selected(self.find_element_wait(located)))
        else:
            return WebDriverWait(self.driver, 10).until(
                EC.element_located_to_be_selected(element))

    def is_selected_located(self,located):
        """
        判断元素是否可以被选中,直接嵌套元素对象
        :param located:元组=>字符串对象
        :return:boolean
        """
        return WebDriverWait(self.driver, 10).until(
            EC.element_located_to_be_selected(self.find_element_wait(located)))

    def is_selected_element(self,element):
        """
        判断元素是否可以被选中 嵌套上文元素对象
        :param element:with上文的元素对象
        :return:booleanboolean
        """
        return WebDriverWait(self.driver, 10).until(
            EC.element_located_to_be_selected(element))

    def is_clickable_element(self,element):
        """
        判断元素可见并且能被单击
        :param element:
        :return:
        """
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(element))


    def get_alert_text(self):
        """
        获取弹出框的内容
        :return:
        """
        return self.driver.switch_to.alert.text

    def accept_alert(self):
        """
        JS弹窗左键同意 new method
        :return:
        """
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self):
        """
        JS弹窗右键拒绝 new method
        :return:
        """
        self.driver.switch_to.alert.dismiss()

    def impl_wait(self, time=15):
        """
        隐式等待
        :param time:
        :return:
        """
        self.driver.implicitly_wait(time)


    def select_value(self, located, mode,args):
        """
        通过mode填入的值 选择一个下拉框选项
        :param located:
        :param value:
        :return:
        """
        element = self.find_element_wait(located)
        if mode =="value":#通过value值定位
            Select(element).select_by_value(args)
        elif mode =="text":#通过文本值定位
            Select(element).select_by_visible_text(args)
        elif mode =="index":
            Select(element).select_by_index(args)

    def deselect_value(self, located):
        """
        取消已选择的下拉框
        比如当默认有选择时，或者取消选择下拉框项目操作时
        :param located:
        :return:
        """
        element = self.find_element_wait(located)
        Select(element).deselect_all()

    def find_element_wait(self,located,timeout=set.timeout,poll=set.poll_time):
        """
        隐式等待12秒 self.driver.定位器
        :param located:
        :param timeout:
        :param poll:
        :return:
        """
        if "=>" not in located:
            raise NameError("located errors")
        by =located.split("=>")[0]
        value =located.split("=>")[1]
        if by == "id" or by =="ID":
            element =WebDriverWait(self.driver,timeout, poll).until(EC.presence_of_element_located((By.ID, value)))
        elif by == "name" or by =="NAME":
            element =WebDriverWait(self.driver,timeout, poll).until(EC.presence_of_element_located((By.NAME, value)))
        elif by == "class"or by =="CLASS":
            element =WebDriverWait(self.driver,timeout, poll).until(EC.presence_of_element_located((By.CLASS_NAME, value)))
        elif by == "link_text" or by=="LINK_TEXT":
            element =WebDriverWait(self.driver,timeout, poll).until(EC.presence_of_element_located((By.LINK_TEXT, value)))
        elif by == "xpath" or by=="XPATH":
            element =WebDriverWait(self.driver,timeout, poll).until(EC.presence_of_element_located((By.XPATH, value)))
        elif by == "css" or by=="CSS":
            element =WebDriverWait(self.driver,timeout, poll).until(EC.presence_of_element_located((By.CSS_SELECTOR, value)))
        else:
            raise NameError(
                "Please enter the correct targeting elements,'id','name','class','link_text','xpaht','css'.")
        return element

    def clear_element_text(self,located):
        """
        选中元素清除元素上的信息，让焦点到确保在顶头位置
        :param located:
        :return:
        """
        try:
            element =self.find_element_wait(located)
            if element.text: #如果有文本获取焦点后删除
                element.click()
                element.clear()
            else:
                element.click() #获取焦点
            return element
        except Exception as error:
            print(format(error))

    def element_send_keys(self,located, context):
        """
        定位元素后根据状态清除后send_keys(文本)
        :param located: 元素定位方法，id，name "定位器=>value"
        :param context: 要输入的内容
        :return:
        """
        try:
            element = self.clear_element_text(located)
            if element:
                element.send_keys(context)
            return element
        except Exception as error:
            print(error)

    def get_web_cookies(self):
        """
        获得cookies
        :return:
        """
        cookies =self.driver.get_cookies()
        for cookie in cookies:
            return cookie
            #['domain'],cookie['name'],cookie['value'],cookie['expiry'],cookie['path']

    def screen_error(self, param, *args, **kwargs):
        def decorate(func):
            def wrapper(self, *args, **kwargs):
                try:
                    func(self, *args, **kwargs)
                    result = True
                except Exception as e:
                    self.driver.get_screenshot_as_file(set.Pic_DIR+sys._getframe().f_code.co_name+ "error.png")
                    print(e)
                    result = False
                assert result
                return wrapper
        return decorate


    def capture_screen(self,scene):
        """
        捕获截图
        :return:
        """
        try:
            screen_dir =self.path+os.sep+"ScreenShot"+os.sep
            result =self.driver.get_screenshot_as_file(screen_dir+scene)
            return result
        except IOError as error:
            print(format(error))

    def check_title(self,checkData):
        """
        检查网页title
        :param checkData:
        :return:
        """
        assert checkData in self.driver.title

    def check_element_text(self,located,checkData):
        """
        如果断言对象文本成功则返回对象
        :param located:
        :param data:
        :return: element用于增加颜色
        """
        element =self.find_element_wait(located)
        assert checkData in element.text
        return element


    def colour_element(self,element):
        """
        使用JS的增色功能
        :param element:
        :return:
        """
        self.driver.execute_script("arguments[0].setAttribute('style',\
        arguments[1]);",element,"background:green;border:2px solid red;")


    def press_move_element(self,able_move_ele,x,y):
        """
        长按元素按需求偏移移动位置
        :param able_move_ele:
        :param x:x轴
        :param y:y轴
        :return:
        """
        action = ActionChains(self.driver)
        action.drag_and_drop_by_offset(able_move_ele,x,y).perform()

    def scroll_to_end(self):
        """
        scrollTo函数滚动到最下方
        :return:
        """
        self.driver.execute_script("window.scrollTo(100,document.body.scrollHeight);")
        time.sleep(set.wait)

    def add_atribute(self,eleobj,attrName,value):
        """
        向页面标签添加新属性<临时修改>
        :param eleobj:
        :param attrName:
        :param value:
        :return:
        """
        self.driver.execute_script("arguments[0]. %s =arguments[1]",eleobj,attrName,value)

    def get_atribute(self,eleobj,attrName):
        """
        获取页面标签属性<临时修改>
        :param eleobj:
        :param attrName:
        :return:
        """
        return eleobj.get_attribute(attrName)

    def set_atribute(self,eleobj,attrName,value):
        """
        设置页面标签属性<临时修改>
        :param eleobj:
        :param attrName:
        :param value:
        :return:
        """
        self.driver.execute_async_script("arguments[0].setAttribute\
                                         (arguments[1],arguments[2])",eleobj,attrName,value)  #异步方法，不会阻塞主线程执行

    def del_attribute(self,eleobj,attrName):

        self.driver.execute_script("arguments[0].removeAttribute")
