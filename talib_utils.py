import talib


def ao_calculation(high, low, window1=5, window2=34):
    median_price = (high + low) / 2
    sma1 = talib.SMA(median_price, timeperiod=window1)
    sma2 = talib.SMA(median_price, timeperiod=window2)
    return sma1 - sma2


def rsi_calculation(data, window):
    return talib.RSI(data, timeperiod=window)


def bop_calculation(open, high, low, close):
    return talib.BOP(open, high, low, close)


def cci_calculation(high, low, close, window=14):
    return talib.CCI(high, low, close, timeperiod=window)


def cmo_calculation(close, window=14):
    return talib.CMO(close, timeperiod=window)


def dm_calculation(high, low, window=14):
    return talib.PLUS_DM(high, low, timeperiod=window)


def macd_calculation(close_series, fastperiod=12, slowperiod=26, signalperiod=9):
    macd, signal, hist = talib.MACD(close_series, fastperiod, slowperiod, signalperiod)
    return macd


def mom_calculation(close_series, window=10):
    return talib.MOM(close_series, timeperiod=window)


# Percentage Price Oscillator (PPO)
def ppo_calculation(close_series, fastperiod=12, slowperiod=26, matype=0):
    return talib.PPO(close_series, fastperiod, slowperiod, matype)


def roc_calculation(close_series, window=10):
    return talib.ROC(close_series, timeperiod=window)


def trix_calculation(close, timeperiod=30):
    return talib.TRIX(close, timeperiod=timeperiod)


def uo_calculation(high_series, low_series, close_series, timeperiod1=7, timeperiod2=14, timeperiod3=28):
    return talib.ULTOSC(high_series, low_series, close_series, timeperiod1, timeperiod2, timeperiod3)


def williams_r_calculation(high, low, close, timeperiod=14):
    return talib.WILLR(high, low, close, timeperiod=timeperiod)


def adx_calculation(high, low, close, timeperiod=14):
    return talib.ADX(high, low, close, timeperiod=timeperiod)


def aroon_oscillator_calculation(high, low, timeperiod=14):
    aroon_down, aroon_up = talib.AROON(high, low, timeperiod)
    return aroon_up - aroon_down


# Parabolic Stop and Reverse (PSAR)
def psar_calculation(high, low, acceleration=0.02, maximum=0.2):
    return talib.SAR(high, low, acceleration, maximum)

# Low Bollinger
def low_bollinger_band(close, timeperiod=20, nbdevdn=2, matype=0):
    upperband, middleband, lowerband = talib.BBANDS(close, timeperiod, nbdevdn, nbdevdn, matype)
    return lowerband


def high_bollinger_band(close, timeperiod=20, nbdevup=2, matype=0):
    upperband, middleband, lowerband = talib.BBANDS(close, timeperiod, nbdevup, nbdevup, matype)
    return upperband


def low_donchian_channel(low, timeperiod=20):
    return low.rolling(timeperiod).min()


def high_donchian_channel(high, timeperiod=20):
    return high.rolling(timeperiod).max()


def low_keltner_channel(high, low, close, timeperiod=20, atr_timeperiod=10, multiplier=2):
    middleband = talib.SMA(close, timeperiod)
    atr = talib.ATR(high, low, close, atr_timeperiod)
    return middleband - (multiplier * atr)


def high_keltner_channel(high, low, close, timeperiod=20, atr_timeperiod=10, multiplier=2):
    middleband = talib.SMA(close, timeperiod)
    atr = talib.ATR(high, low, close, atr_timeperiod)
    return middleband + (multiplier * atr)


# Accumulation/Distribution Index
def ad_calculation(high, low, close, volume):
    return talib.AD(high, low, close, volume)


# On-Balance Volume
def obv_calculation(close, volume):
    return talib.OBV(close, volume)


# Chaikin Money Flow (CMF)
def cmf_calculation(high, low, close, volume, timeperiod=20):
    return talib.ADOSC(high, low, close, volume, fastperiod=timeperiod, slowperiod=timeperiod)


# Money Flow Index (MFI)
def mfi_calculation(high, low, close, volume, timeperiod=14):
    return talib.MFI(high, low, close, volume, timeperiod)


# Simple Moving Average
def sma_calculation(close_series, timeperiod=30):
    return talib.SMA(close_series, timeperiod)


# Exponential Moving Average (EMA)
def ema_calculation(close_series, timeperiod=30):
    return talib.EMA(close_series, timeperiod)

