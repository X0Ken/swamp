import swamp.log
from swamp.utils import CONF
from swamp.utils import import_object

logger = swamp.log.get_logger()


def get_ad_source():
    # swamp.data_source.STM32.ADSource
    # swamp.data_source.fake.ADSource
    return import_object(CONF.data_source)
