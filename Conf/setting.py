import unittest,time,datetime
from selenium import webdriver
import unittest

import os,sys

class Setting():
    path =os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    currentPath = os.path.abspath(os.path.dirname(__file__)) #当前文件夹目录
    ProjectPath = os.path.split(currentPath)[0] #项目那个层级的目录
    TopPath = os.path.split(ProjectPath)[0] #更上一层目录 假设存在就添加

    sys.path.append(ProjectPath) #第一层目录
    sys.path.append(TopPath)  #最顶层目录

    #second_level = os.path.dirname(os.path.abspath("."))
    project_level =os.path.abspath(os.path.dirname(__file__))

    TestDir =path+os.sep+"test_case"+os.sep
    Pic_DIR =path+os.sep+"Pic"+os.sep
    Debug =False

