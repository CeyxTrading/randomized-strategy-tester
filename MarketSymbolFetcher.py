from config import *
import pandas as pd
import os


class MarketSymbolFetcher:
    def __init__(self):
        pass

    def fetch_symbols(self):
        try:
            file_name = f"market_symbols.csv"
            path = os.path.join(CACHE_DIR, file_name)
            if os.path.exists(path):
                symbols_df = pd.read_csv(path)
                return symbols_df
            else:
                table = pd.read_html(
                    'https://en.wikipedia.org/wiki/Nasdaq-100#:~:text=It%20created%20two%20indices%3A%20the,firms%2C%20and%20Mortgage%20loan%20companies.')
                symbols_df = table[4]
                symbols_df.to_csv(path)
                return symbols_df
        except Exception as e:
            print(f"Failed to fetch market symbols, error: {str(e)}")
            return None