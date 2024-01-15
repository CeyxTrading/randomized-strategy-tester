from enum import Enum


class Interval(str, Enum):
    ONE_MIN = '1min'
    FIFTEEN_MINS = '15min'
    ONE_HOUR = '1hour'
    FOUR_HOURS = '4hour'
    ONE_DAY = '1Day'


class IndicatorCategory(str, Enum):
    MOMENTUM = 'MOMENTUM'
    VOLATILITY = 'VOLATILITY'
    TREND = 'TREND'
    VOLUME = 'VOLUME'


class IndicatorType(str, Enum):
    AO = 'AO'
    APO = 'APO'
    MACD = 'MACD'
    RSI = 'RSI'
    BOP = 'BOP'
    CCI = 'CCI'
    CMO = 'CMO'
    DM = 'DM'
    MOM = 'MOM'
    PPO = 'PPO'
    ROC = 'ROC'
    TRIX = 'TRIX'
    UO = 'UO'
    WILLIAMSR = 'WILLIAMSR'
    ADX = 'ADX'
    AROON = 'AROON'
    PSAR = 'PSAR'
    LOW_BBAND = 'LOW_BBAND'
    HIGH_BBAND = 'HIGH_BBAND'
    LOW_DONCHIAN = 'LOW_DONCHIAN'
    HIGH_DONCHIAN = 'HIGH_DONCHIAN'
    LOW_KC = 'LOW_KC'
    HIGH_KC = 'HIGH_KC'
    AD = 'AD'
    OBV = 'OBV'
    CMF = 'CMF'
    MFI = 'MFI'
    SMA = 'SMA'
    EMA = 'EMA'


class Side(str, Enum):
    ENTRY = 'ENTRY'
    EXIT = 'EXIT'


class OperatorType(str, Enum):
    LOWER_THAN = 'LOWER_THAN'
    GREATER_THAN = 'GREATER_THAN'
    CROSS_FROM_BELOW = 'CROSS_FROM_BELOW'
    CROSS_FROM_ABOVE = 'CROSS_FROM_ABOVE'
