import json
import math

from swamp import models


def diagnosis(device):
    first = models.CheckInfo.get_all_by_device(
        device.id).first()
    first_data = json.loads(first.data)

    last = models.CheckInfo.get_all_by_device(
        device.id).order_by(
        models.CheckInfo.created_at.desc()).first()
    last_data = json.loads(last.data)

    compare_time = device.get_setting(models.COMPARE_TIME, default=0,
                                      _type=int)
    max_time = device.get_setting(models.MAX_TIME, default=0, _type=int)

    index = compare_time * len(first_data) / max_time
    standard = first_data[index][1]
    new = last_data[index][1]
    
    deviation = math.fabs(standard - new) / standard
    if deviation > 0.04:
        return False
    return True
