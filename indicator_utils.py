import uuid
from Indicator import IndicatorType, IndicatorCategory, Indicator
from RiskMgtMethod import RiskMgtMethod, RiskMgtMethodType


# Functions to instantiate the indicators
def create_rsi():
    return Indicator(
    id=str(uuid.uuid4()),
    name="RSI",
    category=IndicatorCategory.MOMENTUM,
    item_type=IndicatorType.RSI,
    window1_min=10, window1_max=30,  # RSI typical window
    window2_min=None, window2_max=None,  # Not applicable for RSI
    window3_min=None, window3_max=None,
    entry_threshold_min=20, entry_threshold_max=40,  # Oversold threshold
    exit_threshold_min=60, exit_threshold_max=80,  # Overbought threshold
    is_exit_indicator=True,
)


# Awesome Oscillator Indicator
ao_indicator = Indicator(
    id=str(uuid.uuid4()),
    name="Awesome Oscillator",
    category=IndicatorCategory.MOMENTUM,
    item_type=IndicatorType.AO,
    window1_min=3, window1_max=10,
    window2_min=30, window2_max=40,
    window3_min=None, window3_max=None,
    entry_threshold_min=-1000, entry_threshold_max=0,
    exit_threshold_min=0, exit_threshold_max=1000,
    is_exit_indicator=True,
)


# Balance of Power Indicator
def create_bop_indicator():
    return Indicator(
    id=str(uuid.uuid4()),
    name="Balance of Power",
    category=IndicatorCategory.MOMENTUM,
    item_type=IndicatorType.BOP,
    window1_min=None, window1_max=None,
    window2_min=None, window2_max=None,
    window3_min=None, window3_max=None,
    entry_threshold_min=0, entry_threshold_max=100,
    exit_threshold_min=-100, exit_threshold_max=0,
    is_exit_indicator=True,
)


# Commodity Channel Index Indicator
def create_cci_indicator():
    return Indicator(
    id=str(uuid.uuid4()),
    name="Commodity Channel Index",
    category=IndicatorCategory.MOMENTUM,
    item_type=IndicatorType.CCI,
    window1_min=10, window1_max=20,
    window2_min=None, window2_max=None,
    window3_min=None, window3_max=None,
    entry_threshold_min=0, entry_threshold_max=100,
    exit_threshold_min=-100, exit_threshold_max=0,
    is_exit_indicator=True,
)


# Chande Momentum Oscillator Indicator
def create_cmo_indicator():
    return Indicator(
    id=str(uuid.uuid4()),
    name="Chande Momentum Oscillator",
    category=IndicatorCategory.MOMENTUM,
    item_type=IndicatorType.CMO,
    window1_min=10, window1_max=20,
    window2_min=None, window2_max=None,
    window3_min=None, window3_max=None,
    entry_threshold_min=0, entry_threshold_max=100,
    exit_threshold_min=-100, exit_threshold_max=0,
    is_exit_indicator=True,
)


def create_ao_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Awesome Oscillator",
        category=IndicatorCategory.MOMENTUM,
        item_type=IndicatorType.AO,
        window1_min=3, window1_max=10,
        window2_min=30, window2_max=40,
        window3_min=None, window3_max=None,
        entry_threshold_min=-100, entry_threshold_max=0,
        exit_threshold_min=0, exit_threshold_max=100,
        is_exit_indicator=True,
    )


def create_dm_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Directional Movement",
        category=IndicatorCategory.TREND,
        item_type=IndicatorType.DM,
        window1_min=10, window1_max=30,
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=20, entry_threshold_max=40,
        exit_threshold_min=10, exit_threshold_max=20,
        is_exit_indicator=True,
    )


def create_macd_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Moving Average Convergence Divergence",
        category=IndicatorCategory.MOMENTUM,
        item_type=IndicatorType.MACD,
        window1_min=12, window1_max=26,
        window2_min=9, window2_max=9,
        window3_min=None, window3_max=None,
        entry_threshold_min=0, entry_threshold_max=None,
        exit_threshold_min=None, exit_threshold_max=0,
        is_exit_indicator=True,
    )


def create_mom_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Momentum Indicator",
        category=IndicatorCategory.MOMENTUM,
        item_type=IndicatorType.MOM,
        window1_min=5, window1_max=15,
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=0, entry_threshold_max=10,
        exit_threshold_min=-10, exit_threshold_max=0,
        is_exit_indicator=True,
    )


def create_ppo_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Percentage Price Oscillator",
        category=IndicatorCategory.MOMENTUM,
        item_type=IndicatorType.PPO,
        window1_min=10, window1_max=20,  # Fast period range
        window2_min=20, window2_max=40,  # Slow period range
        window3_min=None, window3_max=None,
        entry_threshold_min=None, entry_threshold_max=None,
        exit_threshold_min=None, exit_threshold_max=None,
        is_exit_indicator=True,
    )


def create_roc_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Rate of Change",
        category=IndicatorCategory.MOMENTUM,
        item_type=IndicatorType.ROC,
        window1_min=5, window1_max=15,  # Period range for ROC
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=0, entry_threshold_max=30,
        exit_threshold_min=-30, exit_threshold_max=0,
        is_exit_indicator=True,
    )


def create_trix_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Triple Exponential Average",
        category=IndicatorCategory.TREND,
        item_type=IndicatorType.TRIX,
        window1_min=20, window1_max=40,
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=None, entry_threshold_max=None,
        exit_threshold_min=None, exit_threshold_max=None,
        is_exit_indicator=True,
    )


def create_tsi_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="True Strength Index",
        category=IndicatorCategory.MOMENTUM,
        item_type=IndicatorType.TSI,
        window1_min=20, window1_max=30,
        window2_min=10, window2_max=20,
        window3_min=None, window3_max=None,
        entry_threshold_min=-25, entry_threshold_max=-10,
        exit_threshold_min=10, exit_threshold_max=25,
        is_exit_indicator=True,
    )


def create_uo_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Ultimate Oscillator",
        category=IndicatorCategory.MOMENTUM,
        item_type=IndicatorType.UO,
        window1_min=6, window1_max=8,
        window2_min=13, window2_max=15,
        window3_min=27, window3_max=29,
        entry_threshold_min=30, entry_threshold_max=40,
        exit_threshold_min=60, exit_threshold_max=70,
        is_exit_indicator=True,
    )


def create_williams_r_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Williams %R",
        category=IndicatorCategory.MOMENTUM,
        item_type=IndicatorType.WILLIAMSR,
        window1_min=10, window1_max=20,
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=-80, entry_threshold_max=-50,
        exit_threshold_min=-20, exit_threshold_max=-50,
        is_exit_indicator=True,
    )


def create_adx_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Average Directional Movement Index",
        category=IndicatorCategory.TREND,
        item_type=IndicatorType.ADX,
        window1_min=10, window1_max=30,
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=20, entry_threshold_max=25,
        exit_threshold_min=None, exit_threshold_max=None,
        is_exit_indicator=False,
    )


def create_aroon_oscillator_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Aroon Oscillator",
        category=IndicatorCategory.TREND,
        item_type=IndicatorType.AROON,
        window1_min=10, window1_max=30,
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=-50, entry_threshold_max=50,
        exit_threshold_min=-50, exit_threshold_max=50,
        is_exit_indicator=True,
    )


def create_psar_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Parabolic SAR",
        category=IndicatorCategory.TREND,
        item_type=IndicatorType.PSAR,
        window1_min=None, window1_max=None,
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=None, entry_threshold_max=None,
        exit_threshold_min=None, exit_threshold_max=None,
        is_exit_indicator=True,
    )


def create_low_bollinger_band_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Low Bollinger Band",
        category=IndicatorCategory.VOLATILITY,
        item_type=IndicatorType.LOW_BBAND,
        window1_min=15, window1_max=25,
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=None, entry_threshold_max=None,
        exit_threshold_min=None, exit_threshold_max=None,
        is_exit_indicator=False,
    )


def create_high_bollinger_band_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="High Bollinger Band",
        category=IndicatorCategory.VOLATILITY,
        item_type=IndicatorType.HIGH_BBAND,
        window1_min=15, window1_max=25,
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=None, entry_threshold_max=None,
        exit_threshold_min=None, exit_threshold_max=None,
        is_exit_indicator=True,
    )


def create_low_donchian_channel_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Low Donchian Channel",
        category=IndicatorCategory.TREND,
        item_type=IndicatorType.LOW_DONCHIAN,
        window1_min=15, window1_max=25,
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=None, entry_threshold_max=None,
        exit_threshold_min=None, exit_threshold_max=None,
        is_exit_indicator=False,
    )


def create_high_donchian_channel_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="High Donchian Channel",
        category=IndicatorCategory.TREND,
        item_type=IndicatorType.HIGH_DONCHIAN,
        window1_min=15, window1_max=25,
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=None, entry_threshold_max=None,
        exit_threshold_min=None, exit_threshold_max=None,
        is_exit_indicator=True,
    )


def create_low_keltner_channel_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Low Keltner Channel",
        category=IndicatorCategory.VOLATILITY,
        item_type=IndicatorType.LOW_KC,
        window1_min=15, window1_max=25,
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=None, entry_threshold_max=None,
        exit_threshold_min=None, exit_threshold_max=None,
        is_exit_indicator=False,
    )


def create_high_keltner_channel_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="High Keltner Channel",
        category=IndicatorCategory.VOLATILITY,
        item_type=IndicatorType.HIGH_KC,
        window1_min=15, window1_max=25,
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=None, entry_threshold_max=None,
        exit_threshold_min=None, exit_threshold_max=None,
        is_exit_indicator=True,
    )


def create_ad_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Accumulation/Distribution Index",
        category=IndicatorCategory.VOLUME,
        item_type=IndicatorType.AD,
        window1_min=None, window1_max=None,
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=None, entry_threshold_max=None,
        exit_threshold_min=None, exit_threshold_max=None,
        is_exit_indicator=True,
    )


def create_obv_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="On-Balance Volume",
        category=IndicatorCategory.VOLUME,
        item_type=IndicatorType.OBV,
        window1_min=None, window1_max=None,
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=None, entry_threshold_max=None,
        exit_threshold_min=None, exit_threshold_max=None,
        is_exit_indicator=True,
    )


def create_cmf_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Chaikin Money Flow",
        category=IndicatorCategory.VOLUME,
        item_type=IndicatorType.CMF,
        window1_min=15, window1_max=25,
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=0, entry_threshold_max=10,
        exit_threshold_min=-10, exit_threshold_max=0,
        is_exit_indicator=True,
    )


def create_efi_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Elder’s Force Index",
        category=IndicatorCategory.MOMENTUM,
        item_type=IndicatorType.EFI,
        window1_min=10, window1_max=20,
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=0, entry_threshold_max=100,
        exit_threshold_min=-100, exit_threshold_max=0,
        is_exit_indicator=True,
    )


def create_eom_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Ease of Movement",
        category=IndicatorCategory.MOMENTUM,
        item_type=IndicatorType.EOM,
        window1_min=10, window1_max=20,
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=0, entry_threshold_max=100,
        exit_threshold_min=-100, exit_threshold_max=0,
        is_exit_indicator=True,
    )


def create_mfi_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Money Flow Index",
        category=IndicatorCategory.VOLUME,
        item_type=IndicatorType.MFI,
        window1_min=10, window1_max=20,
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=20, entry_threshold_max=30,
        exit_threshold_min=70, exit_threshold_max=80,
        is_exit_indicator=True,
    )


def create_sma_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Simple Moving Average",
        category=IndicatorCategory.TREND,
        item_type=IndicatorType.SMA,
        window1_min=20, window1_max=50,
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=None, entry_threshold_max=None,
        exit_threshold_min=None, exit_threshold_max=None,
        is_exit_indicator=True,
    )


def create_ema_indicator():
    return Indicator(
        id=str(uuid.uuid4()),
        name="Exponential Moving Average",
        category=IndicatorCategory.TREND,
        item_type=IndicatorType.EMA,
        window1_min=20, window1_max=50,
        window2_min=None, window2_max=None,
        window3_min=None, window3_max=None,
        entry_threshold_min=None, entry_threshold_max=None,
        exit_threshold_min=None, exit_threshold_max=None,
        is_exit_indicator=True,
    )


#  Risk Management Methods
def create_stop_loss_method():
    return RiskMgtMethod(
            id=str(uuid.uuid4()),
            name="Stop Loss",
            item_type=RiskMgtMethodType.STOP_LOSS,
            rm_threshold=None,
            rm_threshold_min=1, rm_threshold_max=100
        )


def create_trailing_stop_method():
    return RiskMgtMethod(
        id=str(uuid.uuid4()),
        name="Trailing Stop",
        item_type=RiskMgtMethodType.TRAILING_STOP,
        rm_threshold=None,
        rm_threshold_min=1, rm_threshold_max=100
    )


def create_take_profit_method():
    return RiskMgtMethod(
        id=str(uuid.uuid4()),
        name="Take Profit",
        item_type=RiskMgtMethodType.TAKE_PROFIT,
        rm_threshold=None,
        rm_threshold_min=1, rm_threshold_max=100
    )
