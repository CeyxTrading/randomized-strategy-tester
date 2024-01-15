###################################################################
#
#  Name: Random Strategy Tester 1
#  Description: Randomly tests strategy combinations and keeps track of the best results
#  Author: B/O Trading Blog
#
###################################################################
from log_utils import *
from MarketSymbolFetcher import MarketSymbolFetcher
from PriceFetcher import PriceFetcher
from config import *
from StrategySeeker import StrategySeeker
from StrategyResultTracker import StrategyResultTracker
import threading
from datetime import datetime, timedelta
import schedule
import time
from enums import *
from test_utils import *
pd.options.mode.chained_assignment = None


if __name__ == "__main__":
    # Shared DataFrame and Lock for thread safety
    combined_strategy_results_df = pd.DataFrame()
    lock = threading.Lock()

    #  Create output directories
    create_output_directories()

    # Set up logging
    setup_logger("strategy_seeker1.txt", log_level="INFO")
    logi("Starting Strategy Seeker 1")

    # Fetch risk-free rate
    risk_free_rate = fetch_risk_free_rate()

    #  Fetch NASDAQ 100 tickers
    market_symbol_fetcher = MarketSymbolFetcher()
    nasdaq_symbols_df = market_symbol_fetcher.fetch_symbols()
    symbols = nasdaq_symbols_df['Ticker'].tolist()

    # Set start- and end dates
    num_years = 3
    end_date_str = datetime.today().strftime('%Y-%m-%d')
    start_date_str = (datetime.today() - timedelta(days=num_years * 365)).strftime('%Y-%m-%d')

    #  Fetch all prices
    price_fetcher = PriceFetcher()
    interval = Interval.ONE_HOUR
    prices_dict = price_fetcher.fetch_all_prices(symbols, start_date_str, end_date_str, interval)

    # Init result tracker
    result_file_name = build_result_file_name()
    strategy_result_tracker = StrategyResultTracker(result_file_name)

    # Create StrategySeeker threads
    seekers = []
    seeker_threads = []
    num_seekers = NUM_SEEKERS
    plot_list = []  # stocks to plot
    for i in range(num_seekers):  # Define num_seekers
        seeker = StrategySeeker(name=f"seeker{i + 1}",
                                prices_dict=prices_dict,
                                risk_free_rate=risk_free_rate,
                                plot_list=plot_list,
                                result_tracker=strategy_result_tracker)
        seekers.append(seeker)

        # Create a new thread for each seeker
        seeker_thread = threading.Thread(target=seeker.seek)
        seeker_threads.append(seeker_thread)

        # Start the thread
        seeker_thread.start()

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logi("Keyboard interrupt received, stopping seekers...")

        # Stop all seekers
        for seeker in seekers:
            seeker.stop()

        logi("Waiting for threads to finish...")

        # Join all threads
        for thread in seeker_threads:
            thread.join()

        logi("All threads stopped.")
