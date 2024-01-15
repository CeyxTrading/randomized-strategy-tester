from StrategyBuilder import StrategyBuilder
from Backtester import Backtester
from log_utils import *
from config import *
from IndicatorGenerator import IndicatorGenerator
import time
from test_utils import *


class StrategySeeker:
    def __init__(self, name, prices_dict, risk_free_rate, plot_list, result_tracker):
        self.name = name
        self.is_running = False
        self.prices_dict = prices_dict
        self.risk_free_rate = risk_free_rate
        self.plot_list = plot_list
        self.result_tracker = result_tracker
        self.num_tests = 0
        self.strategy_builder = None
        self.setup()

    def setup(self):
        # Create indicators and risk management methods
        indicator_generator = IndicatorGenerator()
        indicators = indicator_generator.generate_indicators()
        rm_methods = indicator_generator.generate_risk_mgt_methods()

        # Create Strategy Builder
        self.strategy_builder = StrategyBuilder(indicators=indicators, risk_mgt_methods=rm_methods)

    def seek(self):
        logi(f"Starting seeker {self.name}")
        self.is_running = True
        while self.is_running:
            # Start the timer
            start_time = time.time()

            # Build strategy
            strategy = self.strategy_builder.build_strategy()

            #  Create Backtester
            backtester = Backtester(
                prices_dict=self.prices_dict,
                initial_balance=INITIAL_BALANCE,
                position_size_pct=POSITION_SIZE_PCT,
                commission=COMMISSION,
                risk_free_rate=self.risk_free_rate,
                plot_list=self.plot_list
            )

            # Test strategy
            backtest_results = backtester.execute_backtest(strategy)

            # Calculate strategy results
            strategy_results_df = create_strategy_results(strategy, backtest_results)

            # Thread-safe update of the combined dataframe
            self.result_tracker.add_strategy_results(strategy_results_df)

            #  Store strategies with promising results
            return_threshold = 10
            if strategy_results_df['median_returns'].iloc[-1] >= return_threshold:
                self.store_strategy(strategy)

            # Log run
            self.num_tests += 1
            end_time = time.time()
            execution_time = end_time - start_time
            logi(f"Seeker {self.name} completed run {self.num_tests} in {execution_time:.2f} seconds")


    def store_strategy(self, strategy):
        # Store strategy as a JSON file
        file_path = os.path.join(STRATEGY_DIR, strategy.id + ".json")
        save_strategy_to_json(strategy, file_path)

    def stop(self):
        self.is_running = False
