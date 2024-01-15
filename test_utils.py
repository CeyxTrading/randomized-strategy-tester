import talib
import json
from Indicator import Indicator
from RiskMgtMethod import RiskMgtMethod
from Strategy import Strategy
from config import *
from scipy.stats import zscore
from scipy.stats.mstats import winsorize
from enum import Enum
import pandas as pd
import numpy as np
import yfinance as yf
from log_utils import *
import os


def create_output_directories():
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    if not os.path.exists(STRATEGY_DIR):
        os.makedirs(STRATEGY_DIR)
    if not os.path.exists(STRATEGY_PLOTS_DIR):
        os.makedirs(STRATEGY_PLOTS_DIR)
    if not os.path.exists(STRATEGY_CANDIDATES_DIR):
        os.makedirs(STRATEGY_CANDIDATES_DIR)
    if not os.path.exists(PLOT_DIR):
        os.makedirs(PLOT_DIR)


def calculate_buy_hold_return(prices_df, initial_balance, position_size_pct):
    initial_price = prices_df.iloc[0]['Close']
    final_price = prices_df.iloc[-1]['Close']

    # Calculate position size
    position_size = initial_balance * position_size_pct / 100

    # Calculate the return based on the position size
    position_return = position_size * ((final_price - initial_price) / initial_price)
    total_return = position_return + (initial_balance - position_size)

    buy_hold_return = ((total_return - initial_balance) / initial_balance) * 100
    return buy_hold_return

def build_result_file_name():
    return f"results-market-{MARKET}-samples-{SAMPLE_SIZE}-balance-{INITIAL_BALANCE}-pos_size-{POSITION_SIZE_PCT}-commission-{COMMISSION}-v{VERSION}.csv"


def filter_out_outliers(results_df, zscore_value=3):
    # Calculate z-scores for total_return
    results_df['z_score_total_return'] = zscore(results_df['total_return'])

    # Filter out rows where the absolute z-score is greater than x
    results_df = results_df[results_df['z_score_total_return'].abs() <= zscore_value]
    results_df.drop(columns=['z_score_total_return'], inplace=True)
    return results_df


def create_strategy_results(strategy, backtest_results):
    # Convert backtest results to DataFrame
    results_df = pd.DataFrame([result.to_dict() for result in backtest_results])

    # Optional - Winsorize the results
    results_df = results_df.apply(lambda x: winsorize(x, limits=[0.05, 0.05]))

    # Calculate averages
    avg_metrics = results_df.mean()

    #  Build a strategy results dataframe
    strategy_results_df = pd.DataFrame(avg_metrics).transpose()

    #  Calculate median returns
    median_total_returns = results_df['total_return'].median()
    strategy_results_df['median_returns'] = median_total_returns

    #  Calculate standard deviation of returns
    std_total_returns = results_df['total_return'].std()
    strategy_results_df['std_total_returns'] = std_total_returns

    #  Add the strategy info
    strategy_results_df['strategy_id'] = strategy.id
    strategy_results_df['strategy_details'] = strategy.get_details()

    return strategy_results_df


def save_strategy_to_json(strategy, file_path):
    def custom_converter(o):
        if isinstance(o, Strategy):
            return {
                'id': o.id,
                'entry_indicators': [custom_converter(ind) for ind in o.entry_indicators],
                'exit_indicators': [custom_converter(ind) for ind in o.exit_indicators],
                'risk_mgt_methods': [custom_converter(rm) for rm in o.risk_mgt_methods]
            }
        elif isinstance(o, Indicator):
            return {
                'id': o.id,
                'name': o.name,
                'category': o.category.value,
                'item_type': o.item_type.value,
                'side': o.side.value if o.side else None,
                'window1': o.window1,
                'window1_min': o.window1_min,
                'window1_max': o.window1_max,
                'window2': o.window2,
                'window2_min': o.window2_min,
                'window2_max': o.window2_max,
                'window3': o.window3,
                'window3_min': o.window3_min,
                'window3_max': o.window3_max,
                'entry_threshold': o.entry_threshold,
                'entry_threshold_min': o.entry_threshold_min,
                'entry_threshold_max': o.entry_threshold_max,
                'exit_threshold': o.exit_threshold,
                'exit_threshold_min': o.exit_threshold_min,
                'exit_threshold_max': o.exit_threshold_max,
                'threshold_operator': o.threshold_operator.value if o.threshold_operator else None,
                'is_exit_indicator': o.is_exit_indicator
            }
        elif isinstance(o, RiskMgtMethod):
            return {
                'id': o.id,
                'name': o.name,
                'item_type': o.item_type.value,
                'rm_threshold': o.rm_threshold,
                'rm_threshold_min': o.rm_threshold_min,
                'rm_threshold_max': o.rm_threshold_max
            }
        elif isinstance(o, Enum):
            return o.value

    with open(file_path, 'w') as file:
        json.dump(strategy, file, default=custom_converter, indent=4)


def load_strategy_from_json(file_path):
    if not os.path.exists(file_path):
        return None
    def decode_indicator(dct):
        if 'category' in dct:
            return Indicator(id=dct['id'],
                             name=dct['name'],
                             category=dct['category'],
                             item_type=dct['item_type'],
                             side=dct['side'],
                             window1=dct['window1'],
                             window1_min=dct['window1_min'],
                             window1_max=dct['window1_max'],
                             window2=dct['window2'],
                             window2_min=dct['window2_min'],
                             window2_max=dct['window2_max'],
                             window3=dct['window3'],
                             window3_min=dct['window3_min'],
                             window3_max=dct['window3_max'],
                             entry_threshold=dct['entry_threshold'],
                             entry_threshold_min=dct['entry_threshold_min'],
                             entry_threshold_max=dct['entry_threshold_max'],
                             exit_threshold=dct['exit_threshold'],
                             exit_threshold_min=dct['exit_threshold_min'],
                             exit_threshold_max=dct['exit_threshold_max'],
                             threshold_operator=dct['threshold_operator'],
                             is_exit_indicator=dct['is_exit_indicator'])
        return dct

    def decode_risk_mgt_method(dct):
        if 'item_type' in dct:
            return RiskMgtMethod(id=dct['id'],
                                 name=dct['name'],
                                 item_type=dct['item_type'],
                                 rm_threshold=dct['rm_threshold'],
                                 rm_threshold_min=dct['rm_threshold_min'],
                                 rm_threshold_max=dct['rm_threshold_max'])
        return dct

    try:
        with open(file_path, 'r') as file:
            strategy_dict = json.load(file)
            strategy_id = strategy_dict['id']
            entry_indicators = [decode_indicator(ind) for ind in strategy_dict['entry_indicators']]
            exit_indicators = [decode_indicator(ind) for ind in strategy_dict['exit_indicators']]
            risk_mgt_methods = [decode_risk_mgt_method(rm) for rm in strategy_dict['risk_mgt_methods']]
            return Strategy(strategy_id, entry_indicators, exit_indicators, risk_mgt_methods)
    except Exception as ex:
        print(f"Failed to load strategy file : {file_path}, ex: {ex}")
        return None


def calculate_sharpe_ratio(trade_returns, risk_free_rate, trading_days=252):
    # Convert trade returns from percentage to decimal
    trade_returns = [x / 100 for x in trade_returns]

    mean_trade_return = np.mean(trade_returns) if trade_returns else 0
    std_trade_return = np.std(trade_returns) if trade_returns else 0

    # Annualize the mean return and standard deviation
    mean_trade_return_annualized = (1 + mean_trade_return) ** trading_days - 1
    std_trade_return_annualized = std_trade_return * np.sqrt(trading_days)

    # Calculate Sharpe Ratio
    sharpe_ratio = ((mean_trade_return_annualized - risk_free_rate) /
                    std_trade_return_annualized) if std_trade_return_annualized != 0 else 0

    return sharpe_ratio


def fetch_risk_free_rate(tbill_ticker='BIL'):
    # Fetch data
    tbill = yf.Ticker(tbill_ticker)

    # Fetch the most recent dividend yield
    try:
        hist = tbill.history(period="1mo")
        latest_close = hist['Close'].iloc[-1]
        latest_dividend = tbill.dividends.iloc[-1]

        # Annualize the latest dividend
        annualized_yield = (latest_dividend / latest_close) * 12  # Assuming monthly dividends
        return annualized_yield
    except Exception as e:
        print(f"Error fetching risk-free rate: {e}")
        return None


def get_rm_method(rm_methods, rm_type):
    for rm_method in rm_methods:
        if rm_method.item_type == rm_type:
            return rm_method
    return None

def print_backtest_metrics(strategy_id, results_df):
    #  Optional - winsorize results
    # results_df = results_df.apply(lambda x: winsorize(x, limits=[0.05, 0.05]))

    #  Calculate standard deviation of returns
    std_total_returns = results_df['total_return'].std()

    #  Calculate median returns
    median_total_returns = results_df['total_return'].median()

    # Calculate averages
    avg_metrics = results_df.mean()

    # Print stats
    logi(f"Results for strategy '{strategy_id}':")
    logi(f"Average total return: {round(avg_metrics[0],2)}")
    logi(f"Median total return: {round(median_total_returns, 2)}")
    logi(f"Standard deviation total return: {round(std_total_returns, 2)}")
    logi(f"Average buy/hold return: {round(avg_metrics[1], 2)}")
    logi(f"Average number of trades: {round(avg_metrics[2], 2)}")
    logi(f"Average max drawdown: {round(avg_metrics[3], 2)}")
    logi(f"Average number of wins: {round(avg_metrics[4], 2)}")
    logi(f"Average number of losses: {round(avg_metrics[5], 2)}")
    logi(f"Average win rate: {round(avg_metrics[6], 2)}")
    logi(f"Average win percent per trade: {round(avg_metrics[7], 2)}")
    logi(f"Average loss percent per trade: {round(avg_metrics[8], 2)}")
    logi(f"Average Sharpe Ratio: {round(avg_metrics[9], 2)}")