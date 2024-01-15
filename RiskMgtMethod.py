from enum import Enum
import random


class RiskMgtMethodType(str, Enum):
    STOP_LOSS = 'STOP_LOSS'
    TRAILING_STOP = 'TRAILING_STOP'
    TAKE_PROFIT = 'TAKE_PROFIT'


class RiskMgtMethod:
    def __init__(self, id, name, item_type, rm_threshold, rm_threshold_min, rm_threshold_max):
        self.id = id
        self.name = name
        self.item_type = item_type
        self.rm_threshold = rm_threshold
        self.rm_threshold_min = rm_threshold_min
        self.rm_threshold_max = rm_threshold_max

    def randomize_parameters(self):
        self.rm_threshold = random.randint(self.rm_threshold_min, self.rm_threshold_max)
