from enums import *


class PriceData:
    def __init__(self, interval, prices_df, minute_prices_df):
        self.interval = interval
        self.prices_df = prices_df
        self.minute_prices_df = minute_prices_df
        self.high_price_map = []
        self.low_price_map = []

    def create_minute_maps(self):
        high_price_map = {}
        low_price_map = {}
        if self.interval == Interval.ONE_HOUR:
            # Group minute data by date and hour
            grouped_minute_data = self.minute_prices_df.groupby([self.minute_prices_df['Date'].dt.date, self.minute_prices_df['Date'].dt.hour])

            # Iterate over the hourly data
            for hour_index, hour_row in self.prices_df.iterrows():
                hour_time = hour_row['Date']

                # Check if group exists and get minute data for the hour
                group_key = (hour_time.date(), hour_time.hour)
                if group_key in grouped_minute_data.groups:
                    minute_data = grouped_minute_data.get_group(group_key)
                    high_price_map[hour_time] = minute_data['High'].tolist()
                    low_price_map[hour_time] = minute_data['Low'].tolist()
                else:
                    high_price_map[hour_time] = []
                    low_price_map[hour_time] = []

            self.high_price_map = high_price_map
            self.low_price_map = low_price_map
        # todo: implement other intervals
