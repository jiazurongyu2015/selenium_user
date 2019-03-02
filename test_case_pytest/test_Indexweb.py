
import pytest
import time
from util.command import Command
from util.Base import Base
from config.setting import Setting #文件路径类
from util.log import logger,insert_log
#https://coding.net/u/tsbc/p/PySelenium_PO
import sys

set =Setting()
cmd =Command()
log =logger("TestIndexWeb")

class TestIndexWeb(Base): #大量用到所以用继承

    """
    pageobject 首个页面
    """
    flag = 3 #状态机
    base_url ="https://www.ctrip.com/"

    def setup_class(self):
        if not self.excel_close():
            log.info("Excel数据未关闭")
            raise Exception("Excel数据未关闭")
        try:
            self.driver = cmd.start_brower(self.base_url)
        except Exception as err:
            print(format(err))

    def teardown_class(self):

        self.driver.quit()

    @insert_log
    def test_step_start(self,msg=Base().read_dict_data(1,"期望结果")):
        """
        检查 "携程旅行网官网" in self.driver.title
        :param msg:
        :return:
        """
        try:
            set.ws["E2"] =self.load_time()
            start = time.clock()
            cmd.check_title(self.read_dict_data(1,"checkData"))
            set.ws["F2"] = self.response_ms(start)
            set.ws["H2"] =msg[-4:]
            res =True
        except Exception as err:
            msg =msg.replace("pass","fail")
            set.ws["H2"] = msg[-4:]
            res = False
            log.info(err)
        finally:
            set.wb.save(set._xlsx_path)
            set.wb.close()
        assert res ==True


    @insert_log
    @pytest.mark.skipif(flag>5,reason=Base().read_dict_data(1,"期望结果"))#条件满足就不跳过
    def test_step_check(self,msg=Base().read_dict_data(2,"期望结果")):
        try:
            set.ws["E3"] = self.load_time()
            start = time.clock()
            if set.debug:print("解析cookies里面的domain",cmd.get_web_cookies()['domain'])
            assert cmd.get_web_cookies()['domain'] == "www.ctrip.com"
            set.ws["F3"] = self.response_ms(start)
            set.ws["H3"] = msg[-4:]
            #assert cmd.get_web_cookies()['value'] == "/" #存下来对象
            res = True
        except Exception as err:
            msg =msg.replace("pass","fail")
            set.ws["H3"] = msg[-4:]
            log.info(err)
            res = False
        finally:
            set.wb.save(set._xlsx_path)
            set.wb.close()
        assert res == True

    @insert_log
    @pytest.mark.xfail(sys.version_info<=(3,3),reason="当前页面信息不相符") #实际上肯定是大于的 #预设条件，函数返回在xfail的第一个区域里
    def test_index_checkInfo(self,msg=Base().read_dict_data(3,"期望结果")):
        """
        s3 验证当前网页是否和目标一致
        :param msg:
        :return:
        """
        client = self.driver
        try:
            set.ws["E4"] = self.load_time()
            start = time.clock()
            if set.debug:print("当前网页",client.current_url)
            assert self.base_url ==client.current_url #self.base_url用的类变量没用数据驱动
            set.ws["F4"] = self.response_ms(start)
            set.ws["H4"] = msg[-4:]
            res = True
        except Exception as err:
            msg =msg.replace("pass","fail")
            set.ws["H4"] = msg[-4:]
            log.info(err)
            res = False
        finally:
            set.wb.save(set._xlsx_path)
            set.wb.close()
        assert res == True

    @insert_log
    def test_index_checklogin(self,msg=Base().read_dict_data(4,"期望结果")):
        """
        s4 主页上找到登录按钮的元素
        :return:
        """
        try:
            set.ws["E5"] = self.load_time()
            start = time.clock()
            element =cmd.check_element_text(self.read_dict_data(4,"located"),self.read_dict_data(4,"checkData")) #先定位在断言
            cmd.colour_element(element)
            set.ws["F5"] = self.response_ms(start)
            set.ws["H5"] = msg[-4:]
            res = True
        except Exception as err:
            msg =msg.replace("pass","fail")
            set.ws["H5"] = msg[-4:]
            log.info(err)
            res = False
        finally:
            set.wb.save(set._xlsx_path)
            set.wb.close()
        assert res == True

    @insert_log
    def test_login_step1(self,msg=Base().read_dict_data(5,"期望结果")):
        """
        s5 主页 检查切换到登陆页面
        :return:
        """
        try:
            set.ws["E6"] = self.load_time()
            start = time.clock()
            elelogin = cmd.find_element_wait(self.read_dict_data(5,"located")) #
            cmd.colour_element(elelogin)
            if elelogin:
                elelogin.click()
                time.sleep(1)
                assert self.read_dict_data(5,"checkData") in self.driver.current_url
                log.info("切换到登录页面成功")
                assert cmd.get_web_cookies()['httpOnly'] ==False
                set.ws["F6"] = self.response_ms(start)
                set.ws["H6"] = msg[-4:]
            res = True
        except Exception as err:
            msg =msg.replace("pass","fail")
            set.ws["H6"] = msg[-4:]
            log.info(err)
            res = False
        finally:
            set.wb.save(set._xlsx_path)
            set.wb.close()
        assert res == True

    @insert_log
    def test_login_input_pwd(self,msg=Base().read_dict_data(6,"期望结果")):
        """
        s6 输入合法账号密码,检查登录页面元素
        :return:
        """
        try:
            set.ws["E7"] = self.load_time()
            start = time.clock()
            login_title =cmd.find_element_wait(self.read_dict_data(6,"located"))
            log.info(login_title.text)
            assert self.get_tuple_data(6,"checkData",0) in login_title.text #check1
            assert self.get_tuple_data(6,"checkData",1) in login_title.text #check2
            userfield =cmd.element_send_keys(self.get_tuple_data(6,"output_data",0),self.get_tuple_data(6,"output_data",1)) #验证输入账号
            time.sleep(1)
            pwdfield =cmd.element_send_keys(self.get_tuple_data(6,"output_data",2),self.get_tuple_data(6,"output_data",3))
            time.sleep(1)
            if userfield and pwdfield:
                pass #都存在往下走
            set.ws["F7"] = self.response_ms(start)
            set.ws["H7"] = msg[-4:]
            res = True
        except Exception as err:
            msg =msg.replace("pass","fail")
            set.ws["H7"] = msg[-4:]
            log.info(err)
            res = False
        finally:
            set.wb.save(set._xlsx_path)
            set.wb.close()
        assert res == True

    @insert_log
    def test_login_draft(self, msg=Base().read_dict_data(7, "期望结果")):
        """
        s7 账号界面，确认验证码
        :return:
        """
        try:
            set.ws["E8"] = self.load_time()
            start = time.clock()
            draft_element =cmd.find_element_wait(self.get_tuple_data(7,"located",0))
            if not draft_element:
                raise Exception("找不到draft_element元素")
            move_element =cmd.find_element_wait(self.get_tuple_data(7,"located",1))
            cmd.press_move_element(move_element,300,0)#press_move_element封装方法讲解
            orc_element =cmd.find_element_wait(self.get_tuple_data(7,"located",2))
            if orc_element:#等待输入验证码 万能验证码
                time.sleep(15)
                enter = cmd.find_element_wait(self.get_tuple_data(7,"located",3))
                set.ws["F8"] = self.response_ms(start)
                set.ws["H8"] = msg[-4:]
                log.info("页面元素", enter.text)
                log.info("end")
                res=True
            else:
                enter =cmd.find_element_wait(self.get_tuple_data(7,"located",3))
                set.ws["F8"] = self.response_ms(start)
                set.ws["H8"] = msg[-4:]
                log.info("页面元素",enter.value)
                res = True
        except Exception as err:
            msg = msg.replace("pass", "fail")
            set.ws["H8"] = msg[-4:]
            log.info(err)
            res = False
        finally:
            set.wb.save(set._xlsx_path)
            set.wb.close()
        assert res == True



# t = IndexWeb()
# print(base.get_ini_date("config","Drivers","chrome"))
# if __name__ == '__main__':
#     pytest.main("pytest")
#     #--durations=10
#     import os
#     #py.test test_conf2bin.py --junit-xml=test_conf2bin_report.xml --cov-report=html --cov-config=.coveragerc --cov=./
#     pytest.main(["-durations=2", cmd.stuite_path+os.sep+"test_Indexweb.py"])