import math
import random

from swamp.data_source.base import ADSourceBase
from swamp.data_source.factory import logger


class ADSource(ADSourceBase):
    def test(self):
        logger.info("FakeADSource test pass")
        return True

    def get_data(self):
        logger.info("FakeADSource get data")
        high = random.randrange(80, 150)
        return [math.sin(math.pi / 1000 * i) * high for i in xrange(500)]