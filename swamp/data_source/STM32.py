#!/usr/bin/python
# -*- coding:utf-8 -*-
import serial
import json
import time

# 定义全局变量
from swamp.data_source.base import ADSourceBase
import swamp.log

logger = swamp.log.get_logger()


ERROR = '\x65'
NULL = '\x00'
CHECK = '\x63'
OK = '\x6f'

ISOTIMEFORMAT = '%Y%m%d%H%M%S'


# 声明一个类，和stm32交互。
class ADSource(ADSourceBase):
    ser = None

    # 初始化类的函数
    def __init__(self):
        logger.info("STM32 driver init.")
        self.ser = serial.Serial("COM3", 9600)

    # 检测stm32的状态
    def test(self):
        logger.info("test check.")
        ser = self.ser
        ser.write(OK)
        c = ser.read()
        if c != OK:
            logger.info("data source error.")
            return False
        c = ser.read()
        if c != CHECK:
            logger.info("data source error.")
            return False
        logger.info("data source online.")
        return True

    # 定义转换函数，把数字值转换成相应的电流值
    def digital(self, x):
        return x * 153.6 / 32768 - 62.5 - 0.145

    # 获取数据
    def get_data(self):
        logger.info("data source get begin.")
        ser = self.ser
        ser.write(b'c')
        c = ser.read()
        if c != OK:
            raise Exception("Data format error")
        results = []
        for i in xrange(500):
            high_data = ser.read()
            low_data = ser.read()
            c = ser.read()
            if c != NULL:
                raise Exception("Data format error")
            r = ord(high_data)
            r *= 256
            r |= ord(low_data)
            r = self.digital(r)
            results.append(r)
        return results


def main():
    adsys = ADSource()
    print(adsys.test())
    results = adsys.get_data()
    filename = str(time.strftime(ISOTIMEFORMAT)) + ".txt"
    dat = open(filename, 'w')
    dat.write(json.dumps(results))
    dat.close()
    for r in results:
        print "%.2f" % r, '\t',
    input()


# 如果直接执行当前文件，__name__变量即为字符串"__main__"
if __name__ == "__main__":
    main()
