#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
经测算，测量系统测量20000个点所需要的时间为4:05.3。
平均每个点的测量时间为0.0049s。
1s能测量204个点。
"""
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
        logger.info("data source online.")
        return True

    # 定义转换函数，把数字值转换成相应的电流值
    def digital(self, x):
        return x * 153.6 / 32768 - 62.5 - 0.145

    def to_digital(self, x):
        return int((x + 0.145 + 62.5) * 32768 / 153.6)

    def to_times(self, x):
        return int(x * 204 / 1000)

    def int_2_bytes(self, i):
        return chr(i >> 8) + chr(i & 255)

    # 获取数据
    def get_data(self, max_i=100, max_t=200):
        logger.info("data source get begin.")
        ser = self.ser
        max_t = self.to_times(max_t)
        ser.write('\x63' +
                  self.int_2_bytes(self.to_digital(max_i)) +
                  self.int_2_bytes(max_t))
        c = ser.read()
        if c != OK:
            raise Exception("Data format error")
        logger.info("Command send success.")
        results = []
        for i in xrange(max_t):
            r = self._get_one_data(ser)
            results.append(r)
        c = ser.read()
        if c != OK:
            raise Exception("Data format error")
        return results

    def get_one_data(self):
        logger.info("data source get begin.")
        ser = self.ser
        ser.write(b'1')
        c = ser.read()
        if c != OK:
            raise Exception("Data format error")
        logger.info("Command send success.")
        r = self._get_one_data(ser)
        c = ser.read()
        if c != OK:
            raise Exception("Data format error")
        return r

    def _get_one_data(self, ser):
        high_data = ser.read()
        low_data = ser.read()
        c = ser.read()
        if c != NULL:
            raise Exception("Data format error")
        r = ord(high_data)
        r *= 256
        r |= ord(low_data)
        r = self.digital(r)
        return r


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


def test():
    adsys = ADSource()
    print(adsys.test())
    while True:
        print(adsys.get_one_data())
        time.sleep(0.5)


# 如果直接执行当前文件，__name__变量即为字符串"__main__"
if __name__ == "__main__":
    test()
