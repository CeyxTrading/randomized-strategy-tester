from log_utils import *
from test_utils import *
from MarketSymbolFetcher import MarketSymbolFetcher
from PriceFetcher import PriceFetcher
from Backtester import Backtester
from config import *
from enums import *
from plot_utils import *
from datetime import datetime, timedelta
import pandas as pd
pd.options.mode.chained_assignment = None


if __name__ == "__main__":
    create_output_directories()

    # Set up logging
    setup_logger("strategy_validation1.txt", log_level="INFO")

    # Load strategy - todo
    #strategy_id = "<Your strategy id here>"
    strategy_id = "0ecc5baf-6e2a-4419-b8f7-5861cf722ec3"
    file_path = os.path.join(STRATEGY_DIR, strategy_id + ".json")
    strategy = load_strategy_from_json(file_path)
    if strategy is None:
        loge(f"Strategy {strategy_id} failed to load ({file_path})")
        exit(0)
    logi(f"Validating strategy {strategy_id}...")

    #  Fetch NASDAQ 100 tickers
    market_symbol_fetcher = MarketSymbolFetcher()
    nasdaq_symbols_df = market_symbol_fetcher.fetch_symbols()
    symbols = nasdaq_symbols_df['Ticker'].tolist()

    # Set start- and end dates
    num_years = 5
    end_date_str = datetime.today().strftime('%Y-%m-%d')
    start_date_str = (datetime.today() - timedelta(days=num_years * 365)).strftime('%Y-%m-%d')

    #  Fetch all prices
    price_fetcher = PriceFetcher()
    prices_dict = price_fetcher.fetch_all_prices(symbols, start_date_str, end_date_str, Interval.ONE_HOUR)

    #  Get risk-free rate
    risk_free_rate = fetch_risk_free_rate()

    # list of stocks to plot
    plot_list = ['ADBE', 'ABNB', 'GOOG', 'TEAM', 'COST']

    # Run backtest
    backtester = Backtester(prices_dict, INITIAL_BALANCE, POSITION_SIZE_PCT, risk_free_rate, COMMISSION, plot_list)
    backtest_results = backtester.execute_backtest(strategy)

    # Convert to dataframe
    results_dict_list = [result.to_dict() for result in backtest_results]
    combined_results_df = pd.DataFrame(results_dict_list)

    # Print final stats
    print_backtest_metrics(strategy_id, combined_results_df)

    # Plot results
    plot_strategy_results_scatter(strategy_id, combined_results_df)
    plot_strategy_results_decile_bar_charts(strategy_id, combined_results_df)
