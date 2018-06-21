#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
经测算，测量系统测量20000个点所需要的时间为4:05.3。
平均每个点的测量时间为0.0049s。
1s能测量204个点。
"""
import json
import sys
import time

import serial
# import scipy.signal

from swamp.data_source.base import ADSourceBase
import swamp.log

logger = swamp.log.get_logger()

# 定义全局变量
ERROR = '\x65'
NULL = '\x00'
CHECK = '\x63'
OK = '\x6f'
SUM = '\x73'
DATA = '\x64'

ISOTIMEFORMAT = '%Y%m%d%H%M%S'


# 声明一个类，和stm32交互。
class ADSource(ADSourceBase):
    ser = None

    # 初始化类的函数
    def __init__(self):
        logger.info("STM32 driver init.")
        if sys.platform.find("linux2") > -1:
            serial_port = "/dev/ttyUSB0"
        else:
            serial_port = "COM6"
        self.ser = serial.Serial(serial_port, 9600)

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

    def get_error(self):
        ser = self.ser
        c = ser.read()
        e = ''
        while c != '_':
            e = e + c
            c = ser.read()
        return e

    def _get_sum(self):
        ser = self.ser
        c = ser.read()
        if c == SUM:
            high_data = ser.read()
            r = ord(high_data)
            r *= 256
            low_data = ser.read()
            r |= ord(low_data)
        else:
            raise Exception("Sum error")
        return r


    # 获取数据
    def get_data(self, max_i=100, max_t=200):
        logger.info("data source get begin.")
        ser = self.ser
        self._check_input(max_i, max_t)
        self._send_cmd(max_i, max_t, ser)
        count = self._get_sum()
        results = self._get_datas(ser, count)
        # filter
        # results = list(scipy.signal.medfilt(results, 5))
        res = []
        for i in range(len(results)):
            res.append((i * 1000 / 204, results[i]))
        return res

    def _check_input(self, max_i, max_t):
        if max_i > 50 or max_i < 1:
            raise Exception("current mast more then 1 and less then 50")
        if max_t > 4000 or max_t < 300:
            raise Exception("current mast more then 300 and less then 4000")

    def _send_cmd(self, max_i, max_t, ser):
        max_t = self.to_times(max_t)
        ser.write('\x63' +
                  self.int_2_bytes(self.to_digital(max_i)) +
                  self.int_2_bytes(max_t))
        c = ser.read()
        if c != OK:
            if c == 'e':
                c = ser.read()
                if c == '_':
                    s = self.get_error()
                    if s == 'maxt':
                        raise Exception("Time too long")
            raise Exception("Data format error")
        logger.info("Command send success.")

    def _get_datas(self, ser, count):
        c = ser.read()
        if c != DATA:
            raise Exception("Data format error")
        results = []
        for i in xrange(count):
            r = self._get_one_data(ser)
            #results.append((i * 1000 / 204, r))
            results.append(r)
        c = ser.read()
        if c != OK:
            raise Exception("Data format error")
        logger.info("data source get success.")
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
        r -= 0.075
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


def test_one():
    adsys = ADSource()
    print(adsys.test())
    while True:
        print(adsys.get_one_data())
        time.sleep(0.5)


def test_get():
    adsys = ADSource()
    print(adsys.test())
    print(adsys.get_data(100, 200))
    print(adsys.get_data(100, 300))
    print(adsys.get_data(100, 500))
    print(adsys.get_data(100, 1000))
    print(adsys.get_data(100, 2000))
    print(adsys.get_data(10, 2000))
    print(adsys.get_data(1, 2000))
    print(adsys.get_data(0, 2000))
    print(adsys.get_data(100, 3000))
    print(adsys.get_data(100, 4000))
    print(adsys.get_data(100, 5000))


# 如果直接执行当前文件，__name__变量即为字符串"__main__"
if __name__ == "__main__":
    test_get()
