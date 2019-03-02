
class RunTimeError(Exception):
    "运行失败"
    pass

class ElementNotFoundException(Exception):
    "元素找不到"
    pass

class TimeOutException(Exception):
    "超时"
    pass

class ArithmeticException(Exception):
    "运算错误"
    pass
