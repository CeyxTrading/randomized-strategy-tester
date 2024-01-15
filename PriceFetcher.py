import os
import pandas as pd
import requests
from log_utils import *
from PriceData import *
from datetime import timedelta, datetime

#  todo Get API key
TIINGO_API_KEY = os.environ['TIINGO_API_KEY']


class PriceFetcher:
    def __init__(self):
        pass

    def fetch_tiingo_prices(self, symbol, interval, start_date_str, end_date_str):
        logi(f"Fetching prices for {symbol}, interval: {interval}")

        # Function to load or fetch data
        file_name = f"{symbol}-{interval}-{start_date_str}-{end_date_str}-prices.csv"
        path = os.path.join(CACHE_DIR, file_name)
        if os.path.exists(path):
            prices_df = pd.read_csv(path, parse_dates=['Date'])
            prices_df = prices_df.loc[:, ~prices_df.columns.str.contains('^Unnamed')]
            return prices_df
        else:
            fetch_url = f"https://api.tiingo.com/iex/{symbol}/prices?startDate={start_date_str}&endDate={end_date_str}&resampleFreq={interval}&columns=date,open,high,low,close,volume&token={TIINGO_API_KEY}"
            response = requests.get(fetch_url)
            data = response.json()
            df = pd.DataFrame(data).rename(
                columns={"date": "Date", "open": "Open", "high": "High", "low": "Low", "close": "Close",
                         "volume": "Volume"})
            if len(df) == 0:
                return None
            df['Date'] = pd.to_datetime(df['Date'])
            df.to_csv(path)
            return df

    def fetch_minute_prices_by_month(self, symbol, start_date_str, end_date_str):
        logi(f"Fetching minute prices for {symbol}...")
        # Work around Tiingo API limit of not being able to fetch multiple years of minute data
        file_name = f"{symbol}-1min-{start_date_str}-{end_date_str}-prices.csv"
        path = os.path.join(CACHE_DIR, file_name)
        if os.path.exists(path):
            df = pd.read_csv(path, parse_dates=['Date'])
            return df
        else:
            # Fetch data from Tiingo
            all_minute_prices_df = pd.DataFrame()

            # Convert string dates to datetime objects
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            current_month_start = start_date

            # Fetch minute prices for each month
            interval = Interval.ONE_MIN.value
            while current_month_start <= end_date:
                next_month_start = (current_month_start + timedelta(days=32)).replace(day=1)
                month_end_date = next_month_start - timedelta(days=1)

                # Fetch minute prices for the month
                minute_prices_df = self.fetch_tiingo_prices(symbol,
                                                         interval,
                                                         current_month_start.strftime("%Y-%m-%d"),
                                                         month_end_date.strftime("%Y-%m-%d"))

                # Append to the all_minute_prices_df DataFrame
                all_minute_prices_df = pd.concat([all_minute_prices_df, minute_prices_df])

                # Move to the next month
                current_month_start = next_month_start
            # Store minute prices for caching
            all_minute_prices_df.to_csv(path)
            return all_minute_prices_df

    def fetch_prices(self, symbol, interval, start_date_str, end_date_str):
        # Fetch price data
        prices_df = self.fetch_tiingo_prices(symbol, interval.value, start_date_str, end_date_str)

        # Fetch minute data for intra-bar analysis
        minute_prices_df = self.fetch_minute_prices_by_month(symbol, start_date_str, end_date_str)

        # Create price data and minute map
        price_data = PriceData(interval, prices_df, minute_prices_df)
        logi(f"Creating minute map for {symbol}...")
        price_data.create_minute_maps()
        return price_data

    def fetch_all_prices(self, symbols, start_date_str, end_date_str, interval):
        logi("Fetching prices for all symbols...")

        #  Fetch all prices
        prices_dict = {}
        for symbol in symbols:
            logd(f"Fetching prices for {symbol}...")

            #  Fetch prices
            price_data = self.fetch_prices(symbol, interval, start_date_str, end_date_str)
            if price_data.prices_df is None or len(price_data.prices_df) < 200:
                logw(f"Not enough prices for {symbol}")
                continue

            prices_dict[symbol] = price_data
        return prices_dict