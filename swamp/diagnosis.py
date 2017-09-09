import json
import math

from swamp import models


def diagnosis(device):
    first = device.check_infos.first()
    first_data = json.loads(first.data)

    last = device.check_infos.order_by(
        models.CheckInfo.created_at.desc()).first()
    last_data = json.loads(last.data)

    compare_time = device.get_compare_time(default=0)
    max_time = device.get_max_time(default=0)

    index = compare_time * len(first_data) / max_time
    standard = first_data[index][1]
    new = last_data[index][1]
    
    deviation = math.fabs(standard - new) / standard
    if deviation > 0.04:
        return False
    return True
