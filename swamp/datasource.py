import math
import random

import log

logger = log.get_logger()

class ADSourceBase(object):
    def test(self):
        return False

    def get_data(self):
        return []


class FakeADSource(ADSourceBase):
    def test(self):
        logger.info("FakeADSource test pass")
        return True

    def get_data(self):
        logger.info("FakeADSource get data")
        high = random.randrange(25, 50)
        return [math.sin(math.pi / 500) * i * high for i in xrange(5000)]


def get_ad_source():
    return FakeADSource()