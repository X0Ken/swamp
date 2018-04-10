import math
import random

from swamp.data_source.base import ADSourceBase
from swamp.data_source.factory import logger


class ADSource(ADSourceBase):
    def test(self):
        logger.info("FakeADSource test pass")
        return True

    def get_data(self, max_i=100, max_t=200):
        logger.info("FakeADSource get data")
        high = random.randrange(int(max_i * 3 / 4), max_i)
        return [(i, math.sin(math.pi / max_t * i / 2) * high)
                for i in range(0, max_t, 5)]
