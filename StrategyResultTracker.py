import threading

from log_utils import *
from sklearn.preprocessing import MinMaxScaler
import pandas as pd


class StrategyResultTracker:
    def __init__(self, result_file_name):
        self.combined_results_df = pd.DataFrame()
        self.lock = threading.Lock()
        self.num_results = 0
        self.results_file_path = os.path.join(RESULTS_DIR, result_file_name)
        #  Load results from last run
        self.load_strategy_results()

    def track_results(self, results):
        self.results.append(results)
        self.num_results += 1

    def get_results(self):
        with self.lock:
            return self.combined_results_df

    def add_strategy_results(self, results_df):
        with self.lock:
            self.combined_results_df = pd.concat([self.combined_results_df, results_df], ignore_index=True, axis=0)
        self.num_results += 1

        #  Store results every once in a while
        if self.num_results % 10 == 0:
            with self.lock:
                df = self.combined_results_df.copy()
            self.process_combined_result_updates(df)

    def process_combined_result_updates(self, df):
        #  Calculate strategy score for all strategies
        df = self.calculate_strategy_score(df)
        # Sort by strategy score
        df = df.sort_values(by=["strategy_score"], ascending=[False])
        # Keep the top results
        df = df.head(1000)
        self.save_strategy_results(df)

    def calculate_strategy_score(self, df):
        #  Handle nans
        df['median_returns'].fillna(0, inplace=True)

        # Filter out unprofitable strategies
        df = df[df['total_return'] > 0]
        
        # Initialize MinMaxScaler
        scaler = MinMaxScaler()

        # Scale the relevant columns
        df['norm_median_returns'] = scaler.fit_transform(df[['median_returns']])
        df['norm_num_trades'] = scaler.fit_transform(df[['num_trades']])
        df['norm_max_drawdown'] = scaler.fit_transform(df[['max_drawdown']])
        df['diff_average_win_loss_percent'] = df['average_win_percent'] - abs(df['average_loss_percent'])

        # Calculate the strategy score
        df['strategy_score'] = df['norm_median_returns'] * 0.8 +\
                               df['norm_max_drawdown'] * 0.1 - \
                               df['norm_num_trades'] * 0.1

        # Cleanup
        df.drop(columns=[
            'norm_median_returns',
            'norm_num_trades',
            'norm_max_drawdown'], inplace=True)

        return df

    def load_strategy_results(self):
        logd("Loading strategy results...")
        if os.path.exists(self.results_file_path):
            try:
                combined_results_df = pd.read_csv(self.results_file_path)
                # Drop 'Unnamed' columns
                combined_results_df = combined_results_df.loc[:, ~combined_results_df.columns.str.contains('^Unnamed')]
                self.combined_results_df = combined_results_df
            except Exception as ex:
                loge(f"Failed to load strategy file: {ex}")

    def save_strategy_results(self, df):
        logd("Saving strategy results...")
        if len(df) == 0:
            return

        df.to_csv(self.results_file_path)

