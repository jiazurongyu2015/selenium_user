import pytest
import os,sys
from util.Base import Base

testdir =os.path.abspath(os.path.dirname(__file__)+os.sep+"test_case_pytest")
resultdir =os.path.abspath(os.path.dirname(__file__)+os.sep+"allure-result")
reportdir =os.path.abspath(os.path.dirname(__file__)+os.sep+"Report")

def gen_report(resultdir,reportdir):
    res =os.system("allure generate "+resultdir+os.sep+" -o "+ reportdir) #需要配置环境变量
    if res ==0:return True

if __name__ == '__main__':
    if Base().excel_close(): #自动化条件判断
        pytest.main([testdir,'-s', '-q', '--alluredir',"./allure-result"])
    if gen_report(resultdir,reportdir):
        print("等待几秒后，发送邮件")
    #os.popen("allure generate"+ resultdir+os.sep+"-o "+reportdir+os.sep)
    #allure generate F:\selenium_uses\allure-result\ -o F:\selenium_uses\Report\