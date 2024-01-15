from indicator_utils import *


class IndicatorGenerator:
    def __init__(self):
        pass

    def generate_indicators(self):
        indicators = []

        # RSI Indicator
        rsi_indicator = create_rsi()
        indicators.append(rsi_indicator)

        # Awesome Oscillator Indicator
        ao_indicator = create_ao_indicator()
        indicators.append(ao_indicator)

        # Balance of Power Indicator
        bop_indicator = create_bop_indicator()
        indicators.append(bop_indicator)

        # Commodity Channel Index Indicator
        cci_indicator = create_cci_indicator()
        indicators.append(cci_indicator)

        # Chande Momentum Oscillator Indicator
        cmo_indicator = create_cmo_indicator()
        indicators.append(cmo_indicator)

        # Directional Movement
        dm_indicator = create_dm_indicator()
        indicators.append(dm_indicator)

        # MACD
        macd_indicator = create_macd_indicator()
        indicators.append(macd_indicator)

        # Momentum Indicator
        mom_indicator = create_mom_indicator()
        indicators.append(mom_indicator)

        # Percentage Price Oscillator (PPO)
        ppo_indicator = create_ppo_indicator()
        indicators.append(ppo_indicator)

        # Percentage Price Oscillator (PPO)
        ppo_indicator = create_ppo_indicator()
        indicators.append(ppo_indicator)

        # Rate of Change (ROC)
        roc_indicator = create_roc_indicator()
        indicators.append(roc_indicator)

        # Triple Exponential Average
        trix_indicator = create_trix_indicator()
        indicators.append(trix_indicator)

        # Ultimate Oscillator (UO)
        uo_indicator = create_uo_indicator()
        indicators.append(uo_indicator)

        # Williams %R
        williamsr_indicator = create_williams_r_indicator()
        indicators.append(williamsr_indicator)

        # Average Directional Movement Index
        adx_indicator = create_adx_indicator()
        indicators.append(adx_indicator)

        # AARON
        aaron_indicator = create_aroon_oscillator_indicator()
        indicators.append(aaron_indicator)

        # Parabolic Stop and Reverse (PSAR)
        psar_indicator = create_psar_indicator()
        indicators.append(psar_indicator)

        # Low Bollinger Band
        low_bb_indicator = create_low_bollinger_band_indicator()
        indicators.append(low_bb_indicator)

        # High Bolinger Band
        high_bb_indicator = create_high_bollinger_band_indicator()
        indicators.append(high_bb_indicator)

        # Low Donchian Channel
        low_dc_indicator = create_low_donchian_channel_indicator()
        indicators.append(low_dc_indicator)

        # High Donchian
        high_dc_indicator = create_high_donchian_channel_indicator()
        indicators.append(high_dc_indicator)

        # Low Keltner Channel
        low_kc_indicator = create_low_keltner_channel_indicator()
        indicators.append(low_kc_indicator)

        # High Keltner Channel
        high_kc_indicator = create_high_keltner_channel_indicator()
        indicators.append(high_kc_indicator)

        # Accumulation/Distribution Index - revisit thresholds
        #ad_indicator = create_ad_indicator()
        #indicators.append(ad_indicator)

        # On-Balance Volume - revisit thresholds
        #obv_indicator = create_obv_indicator()
        #indicators.append(obv_indicator)

        # Chaikin Money Flow (CMF)
        cmf_indicator = create_cmf_indicator()
        indicators.append(cmf_indicator)

        # Money Flow Index (MFI)
        mfi_indicator = create_mfi_indicator()
        indicators.append(mfi_indicator)

        # Simple Moving Average
        sma_indicator = create_sma_indicator()
        indicators.append(sma_indicator)

        # Exponential Moving Average (EMA)
        ema_indicator = create_ema_indicator()
        indicators.append(ema_indicator)

        return indicators

    def generate_risk_mgt_methods(self):
        risk_mgt_methods = []

        # Stop Loss Method
        stop_method = create_stop_loss_method()
        risk_mgt_methods.append(stop_method)

        # Trailing Stop Method
        trailing_stop_method = create_trailing_stop_method()
        risk_mgt_methods.append(trailing_stop_method)

        # Take Profit Method
        take_profit_method = create_take_profit_method()
        risk_mgt_methods.append(take_profit_method)

        return risk_mgt_methods
