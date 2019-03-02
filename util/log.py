#! python3
# -*- coding: utf-8 -*-
'a practice of ...'

from config.setting import Setting
import logging
import os,time
set =Setting()

def create_file(name='WebTest', timestamp=True):
    """
    创建文件，并且返回路径和时间
    :param name: 文件名前缀
    :param timestamp: 格式化时间
    :return: 文件路径
    """
    path = os.path.abspath(os.path.dirname(__file__))
    if timestamp:
        time_stamp = time.strftime("%Y%m%d_%H%M", time.localtime())
        # 返回类似于'{name}_{年月日}_{日期}.log'的文件名称
        name = '%s_%s.log' % (name, time_stamp)
        # 返回路径的格式拼接
        full_path = os.path.join(set.log_path, name)
        # exists判断full_path是否存在，如果没有就写入
        if not os.path.exists(full_path):
            f = open(full_path, 'w+',encoding="utf-8")# 创建一个空的文件
            f.close()
        return full_path


def logger(name, level=logging.DEBUG):
    '''
    获取一个操作日志的记录器
    :param name: 记录器文件名
    :param level: debug等级
    :return: 记录器
    '''
    # 获得一个记录器
    _logger = logging.getLogger(str(name))
    # 设置等级
    _logger.setLevel(logging.DEBUG)
    # 文件输出在文件上
    fh = logging.FileHandler(create_file())
    fh.setLevel(level)
    # 创建一个格式化对象，用于将日志记录转化为指定格式的字符串
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(lineno)s - %(message)s')
    # 为指定程序设置格式化
    fh.setFormatter(formatter)
    # 分别和status按位与运算，将指定的处理程序添加到记录器_logger中
    _logger.addHandler(fh)
    return _logger

_logger = logger('WebTest')


def close_logger():
    h_list = _logger.handlers
    for h in h_list:
        _logger.removeHandler(h)

def debug_func(func):
    return _logger.info("Executing case: [%s]" %func.__name__)

def insert_log(fn):
    def wrap(*args,**kwargs): #都接收下来然后在函数内解构
        #before
        debug_func(fn) #日志增强把执行函数名添加进去
        ret =fn(*args,**kwargs)
        #after
        return ret
    return wrap






