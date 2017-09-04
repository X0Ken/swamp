import swamp.log

logger = swamp.log.get_logger()


def get_ad_source():
    # swamp.data_source.STM32.ADSource
    # swamp.data_source.fake.ADSource
    from swamp.data_source.STM32 import ADSource
    return ADSource()
