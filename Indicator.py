from enum import Enum
import random
import numpy as np
from talib_utils import *
from enums import *


operator_type_list = [OperatorType.LOWER_THAN,
                      OperatorType.GREATER_THAN,
                      OperatorType.CROSS_FROM_BELOW,
                      OperatorType.CROSS_FROM_ABOVE]


class Indicator:
    def __init__(self,
                 id,
                 name,
                 category,
                 item_type,
                 side=None,
                 window1=None,
                 window1_min=None,
                 window1_max=None,
                 window2=None,
                 window2_min=None,
                 window2_max=None,
                 window3=None,
                 window3_min=None,
                 window3_max=None,
                 entry_threshold=None,
                 entry_threshold_min=None,
                 entry_threshold_max=None,
                 exit_threshold=None,
                 exit_threshold_min=None,
                 exit_threshold_max=None,
                 threshold_operator=None,
                 is_exit_indicator=True):
        self.id = id
        self.name = name
        self.category = category
        self.item_type = item_type
        self.side = side
        self.window1 = window1
        self.window1_min = window1_min
        self.window1_max = window1_max
        self.window2 = window2
        self.window2_min = window2_min
        self.window2_max = window2_max
        self.window3 = window3
        self.window3_min = window3_min
        self.window3_max = window3_max
        self.entry_threshold = entry_threshold
        self.exit_threshold = exit_threshold
        self.entry_threshold_min = entry_threshold_min
        self.entry_threshold_max = entry_threshold_max
        self.exit_threshold_min = exit_threshold_min
        self.exit_threshold_max = exit_threshold_max
        self.threshold_operator = threshold_operator
        self.is_exit_indicator = is_exit_indicator
        self.indicator_column = self.get_indicator_column()
        self.signal_column = self.get_signal_column()
        self.signal_threshold = None

    def setup(self, side):
        #  Create random parameters
        if self.window1_min is not None and self.window1_max is not None:
            self.window1 = random.randint(self.window1_min, self.window1_max)
        if self.window2_min is not None and self.window2_max is not None:
            self.window2 = random.randint(self.window2_min, self.window2_max)
        if self.window3_min is not None and self.window3_max is not None:
            self.window3 = random.randint(self.window3_min, self.window3_max)
        if self.entry_threshold_min is not None and self.entry_threshold_max is not None:
            self.entry_threshold = random.randint(self.entry_threshold_min, self.entry_threshold_max)
            #  Handle decimal threshold values
            if self.item_type == IndicatorType.CMF:
                self.entry_threshold = self.entry_threshold / 10
        if self.exit_threshold_min is not None and self.exit_threshold_min is not None:
            self.exit_threshold = random.randint(self.exit_threshold_min, self.exit_threshold_min)
            #  Handle decimal threshold values
            if self.item_type == IndicatorType.CMF:
                self.exit_threshold = self.exit_threshold / 10

        self.threshold_operator = operator_type_list[random.randint(0, len(operator_type_list)) - 1]
        self.side = side

        #  Set column names
        self.indicator_column = self.get_indicator_column()
        self.signal_column = self.get_signal_column()

    def get_indicator_column(self):
        return f"{self.item_type.lower()}_{self.side}_w1_{self.window1}_w2_{self.window2}_w3_{self.window3}_ent_{self.entry_threshold}_ext_{self.exit_threshold}"

    def get_signal_column(self):
        return f"signal_{self.indicator_column}"

    def generate_long_signals(self, prices_df):
        open_series = prices_df['Open']
        high_series = prices_df['High']
        low_series = prices_df['Low']
        close_series = prices_df['Close']
        volume_series = prices_df['Volume']

        # AO
        if self.item_type == IndicatorType.AO:
            prices_df[self.indicator_column] = ao_calculation(high_series, low_series, window1=self.window1, window2=self.window2)

        # RSI
        elif self.item_type == IndicatorType.RSI:
            prices_df[self.indicator_column] = rsi_calculation(close_series, window=self.window1)

        # BOP
        elif self.item_type == IndicatorType.BOP:
            prices_df[self.indicator_column] = bop_calculation(open_series, high_series, low_series, close_series)

        # CCI
        elif self.item_type == IndicatorType.CCI:
            prices_df[self.indicator_column] = cci_calculation(high_series, low_series, close_series, window=self.window1)

        # CMO
        elif self.item_type == IndicatorType.CMO:
            prices_df[self.indicator_column] = cmo_calculation(close_series, window=self.window1)

        # DM
        elif self.item_type == IndicatorType.DM:
            prices_df[self.indicator_column] = dm_calculation(high_series, low_series, window=self.window1)

        # MACD
        elif self.item_type == IndicatorType.MACD:
            prices_df[self.indicator_column] = macd_calculation(close_series, fastperiod=self.window1, slowperiod=self.window2, signalperiod=9)

        # MOM
        elif self.item_type == IndicatorType.MOM:
            prices_df[self.indicator_column] = mom_calculation(close_series, window=self.window1)

        # PPO
        elif self.item_type == IndicatorType.PPO:
            prices_df[self.indicator_column] = ppo_calculation(close_series, fastperiod=self.window1, slowperiod=self.window2, matype=0)

        # ROC
        elif self.item_type == IndicatorType.ROC:
            prices_df[self.indicator_column] = roc_calculation(close_series, window=self.window1)

        # TRIX
        elif self.item_type == IndicatorType.TRIX:
            prices_df[self.indicator_column] = trix_calculation(close_series, timeperiod=self.window1)

        # UO
        elif self.item_type == IndicatorType.UO:
            prices_df[self.indicator_column] = uo_calculation(high_series,
                                                              low_series,
                                                              close_series,
                                                              timeperiod1=self.window1,
                                                              timeperiod2=self.window2,
                                                              timeperiod3=self.window3)

        # Williams %R
        elif self.item_type == IndicatorType.WILLIAMSR:
            prices_df[self.indicator_column] = williams_r_calculation(high_series, low_series, close_series, timeperiod=self.window1)

        # ADX
        elif self.item_type == IndicatorType.ADX:
            prices_df[self.indicator_column] = adx_calculation(high_series, low_series, close_series, timeperiod=self.window1)

        # AARON
        elif self.item_type == IndicatorType.AROON:
            prices_df[self.indicator_column] = aroon_oscillator_calculation(high_series, low_series, timeperiod=self.window1)

        # PSAR
        elif self.item_type == IndicatorType.PSAR:
            prices_df[self.indicator_column] = psar_calculation(high_series, low_series, acceleration=0.02, maximum=0.2)

        # Low Bollinger Band
        elif self.item_type == IndicatorType.LOW_BBAND:
            prices_df[self.indicator_column] = low_bollinger_band(close_series, timeperiod=self.window1, nbdevdn=2, matype=0)

        # High Bollinger Band
        elif self.item_type == IndicatorType.HIGH_BBAND:
            prices_df[self.indicator_column] = high_bollinger_band(close_series, timeperiod=self.window1, nbdevup=2, matype=0)

        # Low Donchian
        elif self.item_type == IndicatorType.LOW_DONCHIAN:
            prices_df[self.indicator_column] = low_donchian_channel(low_series, timeperiod=self.window1)

        # High Donchian
        elif self.item_type == IndicatorType.HIGH_DONCHIAN:
            prices_df[self.indicator_column] = high_donchian_channel(high_series, timeperiod=self.window1)

        # Low Keltner Channel
        elif self.item_type == IndicatorType.LOW_KC:
            prices_df[self.indicator_column] = low_keltner_channel(high_series, low_series, close_series, timeperiod=self.window1, atr_timeperiod=10, multiplier=2)

        # High Keltner Channel
        elif self.item_type == IndicatorType.HIGH_KC:
            prices_df[self.indicator_column] = high_keltner_channel(high_series, low_series, close_series, timeperiod=self.window1, atr_timeperiod=10, multiplier=2)

        # Chaikin Money Flow (CMF)
        elif self.item_type == IndicatorType.CMF:
            prices_df[self.indicator_column] = cmf_calculation(high_series, low_series, close_series, volume_series, timeperiod=self.window1)

        # Money Flow Index (MFI)
        elif self.item_type == IndicatorType.MFI:
            prices_df[self.indicator_column] = mfi_calculation(high_series, low_series, close_series, volume_series, timeperiod=self.window1)

        # Simple Moving Average
        elif self.item_type == IndicatorType.SMA:
            prices_df[self.indicator_column] = sma_calculation(close_series, timeperiod=self.window1)

        # Exponential Moving Average (EMA)
        elif self.item_type == IndicatorType.EMA:
            prices_df[self.indicator_column] = ema_calculation(close_series, timeperiod=self.window1)

        #  Add signal column
        if self.side == Side.ENTRY:
            threshold = self.entry_threshold
        else:
            threshold = self.exit_threshold

        #  Create signals based on threshold operator
        if self.item_type == IndicatorType.SMA or self.item_type == IndicatorType.EMA or \
            self.item_type == IndicatorType.TRIX or self.item_type == IndicatorType.PSAR or \
            self.item_type == IndicatorType.LOW_BBAND or self.item_type == IndicatorType.HIGH_BBAND or \
            self.item_type == IndicatorType.LOW_KC or self.item_type == IndicatorType.HIGH_KC or \
            self.item_type == IndicatorType.LOW_DONCHIAN or self.item_type == IndicatorType.HIGH_DONCHIAN:
            #  No threshold values -> use price values
            if self.threshold_operator == OperatorType.LOWER_THAN:
                prices_df[self.signal_column] = np.where((prices_df['Close'] < prices_df[self.indicator_column]), 1, 0)
            elif self.threshold_operator == OperatorType.GREATER_THAN:
                prices_df[self.signal_column] = np.where((prices_df['Close'] > prices_df[self.indicator_column]), 1, 0)
            elif self.threshold_operator == OperatorType.CROSS_FROM_BELOW:
                prices_df[self.signal_column] = np.where((prices_df['Close'] <= prices_df[self.indicator_column].shift()) &
                                                         (prices_df['Close'] > prices_df[self.indicator_column]), 1, 0)
            elif self.threshold_operator == OperatorType.CROSS_FROM_ABOVE:
                prices_df[self.signal_column] = np.where((prices_df['Close'] >= prices_df[self.indicator_column].shift()) &
                                                         (prices_df['Close'] < prices_df[self.indicator_column]), 1, 0)
        else:
            #  Use threshold values
            if self.threshold_operator == OperatorType.LOWER_THAN:
                prices_df[self.signal_column] = np.where((prices_df[self.indicator_column] < threshold), 1, 0)
            elif self.threshold_operator == OperatorType.GREATER_THAN:
                prices_df[self.signal_column] = np.where((prices_df[self.indicator_column] > threshold), 1, 0)
            elif self.threshold_operator == OperatorType.CROSS_FROM_BELOW:
                prices_df[self.signal_column] = np.where((prices_df[self.indicator_column].shift() <= threshold) &
                                                         (prices_df[self.indicator_column] > threshold), 1, 0)
            elif self.threshold_operator == OperatorType.CROSS_FROM_ABOVE:
                prices_df[self.signal_column] = np.where((prices_df[self.indicator_column].shift() >= threshold) &
                                                         (prices_df[self.indicator_column] < threshold), 1, 0)
        return prices_df
