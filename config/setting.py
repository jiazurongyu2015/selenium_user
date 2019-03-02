import os,openpyxl

class Setting():

    path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    TestDir = path + os.sep + "test_case" + os.sep
    Pic_DIR = path + os.sep + "Pic" + os.sep
    _xlsx_path = path + os.sep + "test_data" + os.sep + "data.xlsx"
    mail_path = path + os.sep + "test_data" + os.sep + "mail_group.xlsx"
    map_txt = path + os.sep + "test_data" + os.sep + "mmap.txt"
    log_path = path + os.sep + "logs" + os.sep
    debug =True
    wait =3
    poll_time =0.4
    timeout =15
    wb = openpyxl.load_workbook(_xlsx_path)
    ws = wb[wb.sheetnames[0]]