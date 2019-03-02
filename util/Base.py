import os,datetime
import time
import configparser
import openpyxl,xlrd #操作excel读和写
from config.setting import Setting as set #文件路径类


class MyConf(configparser.ConfigParser):
    '''
    因为configparser读取的数据会自动转换为小写字母，自己抽取出来修改configparser
    作用是不影响源码
    '''

    def __init__(self):
        configparser.ConfigParser.__init__(self,defaults=None)
    def optionxform(self, optionstr):
        return optionstr

conf =MyConf()

class Base(object):

    path = set.path #其他类导入
    BaseDir = path+os.sep+"Report"
    iniDir = path+os.sep+"config" #预防linux和wins / \
    xlsx_path = set._xlsx_path


    def get_format_date(self):
        now = datetime.datetime.now()
        return "{0}-{1}-{2}".format(now.year, now.month, now.day)

    def get_format_time(self,flag=False):
        """
        根据falg布尔值切换显示时间
        :param flag: True获得年月日
        :return:
        """
        if flag:
            return time.strftime("%Y%m%d")
        else:
            return time.strftime("%H%M%S")

    def get_report_path(self,get_ini_date):
        """
        创建Report-年月日文件夹 Report-20180706
        :return: 返回文件夹下面的 Report_小时分钟.html
        """
        "格式月日/单位时间格式的.html，只用到time"
        nowtime = time.localtime()
        dir_date = time.strftime('-%Y%m%d', nowtime) #Report-年月日
        if not os.path.exists(self.BaseDir + dir_date):
            os.mkdir(self.BaseDir + dir_date)
            print("路径===》",self.BaseDir + dir_date)
        day_file = time.strftime('%H%M', nowtime)
        return self.BaseDir + dir_date + os.sep + 'Report_' + day_file + '.html'

    def chrome_path(self):
        "谷歌的浏览器驱动"
        return self.get_ini_date("config","Driver", "chrome")

    def firefox_path(self):
        "火狐的浏览器驱动"
        return self.get_ini_date("config","Driver", "firefox")

    def get_ini_date(self,ininame,sections, item):
        """
        关键字驱动
        :param sections: ini类型文件.sections
        :param item: get.item =>value
        :return: str字符串
        """
        try:
            iniconf = self.iniDir+os.sep+str(ininame)+".ini"  # .read()特性问题不接收拼接
            conf.read(iniconf, encoding="utf-8")
        except Exception as error:
            raise (error)
        return conf.get(sections, item)

    def load_time(self):
        """
        写入时间
        :return:
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    def _get_cols_index(self, table, columnName):
        """
        读取列数据 不直接使用
        :param table:
        :param columnName:
        :return:
        """
        columnIndex = None  # 初始值
        for i in range(table.ncols):
            if (table.cell_value(0, i) == columnName):
                columnIndex = i
                break
        return columnIndex

    def _read_data_byName(self, fileName, sheetName):
        """
        读取excel的sheet数据 不直接使用
        :param fileName:
        :param sheetName:
        :return:
        """
        table = None
        errorMsg = ""
        try:
            data = xlrd.open_workbook(fileName)
            table = data.sheet_by_name(sheetName)
        except Exception as msg:
            errorMsg = msg
        return table, errorMsg

    def read_data_byIndex(self, fileName, sheetIndex):
        table = None
        errorMsg = ""
        try:
            data = xlrd.open_workbook(fileName)
            table = data.sheet_by_index(sheetIndex)
        except Exception as msg:
            errorMsg = msg
        return table, errorMsg

    def read_row_data(self, rowNum):
        """
        直接excel数据 按行row读取对应列数据
        :return:
        """
        table = self._read_data_byName(self.xlsx_path, 'Sheet1')[0]
        if rowNum < table.nrows:
            caseId = table.cell_value(rowNum, self._get_cols_index(table, "caseID"))  # 根据列读取行的内容
            start_time = table.cell_value(rowNum, self._get_cols_index(table, "startTime"))
            response = table.cell_value(rowNum, self._get_cols_index(table, "response"))
            result = table.cell_value(rowNum, self._get_cols_index(table, "最终结果"))
            return int(caseId), int(start_time), response, result
        else:
            return "row越界，请检查"


    def read_dict_data(self, rowNum,value):
        """
        * 读取行数据拿到对应列的value
        :param rowNum: 行数据
        :param key:对应列
        :return: str
        """
        col_dict = {}
        dictdata = {"caseID": 0, "located": 1, "output_data": 2, "checkData": 3, "期望结果": 6}
        try:
            wb = xlrd.open_workbook(self.xlsx_path)
            table = wb.sheet_by_index(0)
            for i in range(table.ncols):  # table.ncols列表
                col_dict[i] = table.cell_value(rowNum, i)  # 1,0
                res =col_dict.get(dictdata.get(value)) #变量拦截
                if type(res) is float: #type(res).__name__ is "float"
                    return int(res) #float浮点数转int
            return res
        except Exception as error:
            print(format(error))

    def get_tuple_data(self,rowNum,value,index):
        """
        允许Excel里面多个数据读取,做了全角和换行的容错
        excel：id=>nloginname,13817293484
        get_tuple_data(6,"output_data")[0] 取出id=>nloginname字符串
        :param rowNum:同read_dict_data
        :param value:同read_dict_data
        :param index:取下标
        :return:
        """
        res =self.read_dict_data(rowNum, value)
        if "，" in res:
            res = res.replace("，", ",") #包含则替换
        if index<len(res.split(',')):
            return res.split(',')[index].strip()
        else:
            return "数据越界"

    def response_ms(self,start):
        """
        返回时间
        :param start:
        :return:
        """
        end =time.clock() -start
        return str(int(end*1000))+" ms"

    def if_condition(self):
        """
        验证excel是否支持回写，验证拦截条件
        :return:
        """
        if os.access(self.xlsx_path,os.X_OK): #X_OK可执行权限
            try:
                wb = openpyxl.load_workbook(set._xlsx_path)
                wb.save(self.xlsx_path)
                closed =True
            except PermissionError:
                closed =False
            return closed

    def excel_close(self):
        """
        准出条件：检查excel物理是否关闭,然后关闭掉
        :return:
        """
        if not self.if_condition():
            work =os.popen('tasklist /FI "IMAGENAME eq EXCEL.exe"').read()
            print(work)
            res =os.system('TASKKILL /F /IM EXCEL.exe')
            if res ==0:print("ok")
        if self.if_condition():#再次验证
            return True

    def get_yaml_data(self): #获取yaml的数据
        pass

    def read_mmap(self,path):
        """
        读取txt描述文件内的下标 传出做列表
        :param path: set.map_txt
        :return:
        """
        with open(path, "r", encoding="utf-8") as f:
            res = f.readline()
            slist = []
            if "，" in res:
                res = res.replace("，", ",")
            for i in range(len(res.split(","))):
                flag = res.split(",")[i]
                slist.append(flag)
            return slist

    def read_mmap_index(self,path, index):
        """
        读取txt描述文件内的下标0，1 用0，1做状态机
        :param path: set.map_txt
        :return:
        """
        with open(path, "r", encoding="utf-8") as f:
            res = f.readline()
            slist = []
            if "，" in res:
                res = res.replace("，", ",")
            for i in range(len(res.split(","))):
                flag = res.split(",")[i]
                slist.append(flag)
            if index < len(res.split(",")):
                return slist[index]
            else:
                return "数据越界"


    def write_txt_seek(self,path, a="0", b="0", c="0", d="0", e="0"):
        """
        读取txt描述文件内的下标0，1 用0，1做状态机
        1可用，0不可用
        write_txt_seek(set.map_txt) 还原
        :param path: set.map_txt
        :return:
        """
        with open(path, "r+", encoding="utf-8") as f:
            if f.tell() != 0:
                return None
            if f.tell() == 0:
                f.write(a)
            f.seek(2)
            f.write(b)
            f.seek(2 * 2)
            f.write(c)
            f.seek(2 * 3)
            f.write(d)
            f.seek(2 * 4)
            f.write(e)
        return self.read_mmap(path)


    def clean_keep_log(self,log_path=set.log_path):
        """
        清理自动化一定日期内的日志 日志格式需要实际业务一样
        :param log_path:
        :return:
        """
        if os.path.exists(log_path) and os.path.isdir(log_path):#判断文件存在是文件夹
            today = datetime.date.today().strftime('%Y%m%d')#和业务保持一致
            yesterday = (datetime.date.today() + datetime.timedelta(-1)).strftime('%Y%m%d')#昨天 datetime.timedelta(-2)前天
            before_yesterday =str(int(yesterday)-1)
            file_name_list = [today, yesterday,before_yesterday]
            for file in os.listdir(log_path):
                file_name_sp = file.split('.')
                if len(file_name_sp) >= 2:
                    file_date = file_name_sp[0].split("_")[1] #和业务保持一致
                    if file_date not in file_name_list:
                        del_path = os.path.join(log_path, file)
                        print("本次删除文件是 %s" % del_path)
                        os.remove(del_path)
                    else:
                        print('合法时间文件是%s' % file)
        else:
            print('路径不存在或者不是目录')

    def sortfile(self,path):
        """
        获取path目录下，最后更新的文件名称
        """
        fl = os.listdir(path)  # 获取path目录文件列表
        # 时间戳进行倒序排序
        fl.sort(key=lambda fn: os.path.getmtime(path + fn) if not os.path.isdir(path + fn) else 0)
        # date.fromtimestamp(timestamp)：根据给定的时间戮，返回一个date对象
        dt = datetime.datetime.fromtimestamp(os.path.getmtime(path + fl[-1]))
        # dt.strftime("%Y年%m月%d日 %H时%M分%S秒" 将date对象格式化显示
        print('最后改动的文件是: ' + fl[-1] + "，时间：" + dt.strftime("%Y年%m月%d日 %H时%M分%S秒"))
        msg = "自动化测试完成，点击下面链接查看测试结果：\n " + "http://192.168.200.8/result/" + day + "/" + fl[-1]
        return msg


