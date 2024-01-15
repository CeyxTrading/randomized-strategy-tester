from BacktestResult import BacktestResult
from RiskMgtMethod import *
from test_utils import *
from plot_utils import *


class Backtester:
    def __init__(self, prices_dict, initial_balance, position_size_pct, commission, risk_free_rate, plot_list=[]):
        self.prices_dict = prices_dict
        self.initial_balance = initial_balance
        self.position_size_pct = position_size_pct
        self.commission = commission
        self.risk_free_rate = risk_free_rate
        self.plot_list = plot_list

    def execute_strategy(self, symbol, strategy, prices_df, high_minute_price_map, low_minute_price_map):
        balance = self.initial_balance
        peak_balance = self.initial_balance
        max_drawdown = 0
        num_trades = 0
        num_wins = 0
        num_losses = 0
        in_trade = False
        trade_returns = []
        sum_win_percent = 0
        sum_loss_percent = 0

        # Lists to track long entry and exit trades
        long_entry_trade_info = []
        long_exit_trade_info = []

        # Variables for risk management
        sl_method = get_rm_method(strategy.risk_mgt_methods, RiskMgtMethodType.STOP_LOSS)
        tp_method = get_rm_method(strategy.risk_mgt_methods, RiskMgtMethodType.TAKE_PROFIT)
        trailing_stop_method = get_rm_method(strategy.risk_mgt_methods, RiskMgtMethodType.TRAILING_STOP)

        tp_price = None
        sl_price = None
        long_max_price = None
        trailing_stop_price = None

        # Calculate buy-hold return
        buy_hold_return = calculate_buy_hold_return(prices_df, self.initial_balance, self.position_size_pct)

        # Iterate over the DataFrame
        prices_df.reset_index(inplace=True)
        for index, row in prices_df.iterrows():
            current_date = row['Date']
            current_price = row['Close']
            trade_exit_price = current_price

            # Check for entry and exit signals
            long_entry = sum(row[indicator.signal_column] for indicator in strategy.entry_indicators) == len(strategy.entry_indicators)
            long_exit = False
            if in_trade:
                long_exit = sum(row[indicator.signal_column] for indicator in strategy.exit_indicators) == len(strategy.exit_indicators)
                if long_exit:
                    logd(f"{str(current_date)}: Long exit for {symbol} @ {current_price}")

            # Set trailing stop prices
            if in_trade and trailing_stop_method is not None:
                # Track max price for trailing stop
                if current_price > long_max_price:
                    long_max_price = current_price

                #  Set trailing stop price
                trailing_stop_price = long_max_price * (1 - trailing_stop_method.rm_threshold/1000)

            # Check risk management methods
            rm_exit = False
            if in_trade:
                #  Get minute prices for this hour
                if current_date in high_minute_price_map:
                    high_minute_prices = high_minute_price_map[current_date]
                if current_date in low_minute_price_map:
                    low_minute_prices = low_minute_price_map[current_date]

                # Check if risk management was triggered
                rm_method_type, rm_price = self.check_risk_management(strategy.risk_mgt_methods, high_minute_prices, low_minute_prices, tp_price, sl_price, trailing_stop_price)
                if rm_method_type is not None:
                    rm_exit = True
                    trade_exit_price = rm_price
                    logd(f"{str(current_date)}: {rm_method_type} for {symbol} @ {trade_exit_price}")

            # Apply entry strategy
            if not in_trade and long_entry:
                logd(f"{str(current_date)}: Long entry for {symbol} @ {current_price}")
                in_trade = True
                num_trades += 1
                trade_entry_price = current_price

                # Calculate stock quantity (no fractional shares)
                position_size = balance * self.position_size_pct / 100
                stock_quantity = int(position_size / current_price)

                # Update balance
                balance = balance - (stock_quantity * current_price)

                # Track trade entry
                entry_info = {
                    'EntryBar': index,
                    'EntryPrice': trade_entry_price,
                    'Size': stock_quantity
                }
                long_entry_trade_info.append(entry_info)

                # Set risk management prices
                if sl_method is not None:
                    sl_price = current_price * (1 - sl_method.rm_threshold / 1000)
                if tp_method is not None:
                    tp_price = current_price * (1 + tp_method.rm_threshold / 1000)
                if trailing_stop_method is not None:
                    long_max_price = current_price

            # Apply exit strategy and risk management
            if in_trade and (long_exit or rm_exit):
                in_trade = False
                trade_return = (trade_exit_price - trade_entry_price) / trade_entry_price * 100
                trade_returns.append(trade_return)
                logd(f"{str(current_date)}: Trade return for {symbol} @ {round(trade_return, 2)}")

                # Update balance based on the trade outcome
                balance = balance + (stock_quantity * trade_exit_price)
                stock_quantity = 0
                peak_balance = max(peak_balance, balance)
                long_max_price = None
                tp_price = None
                stop_price = None
                trailing_stop_price = None

                # Track exit info
                exit_info = {
                    'ExitBar': index,
                    'ExitPrice': trade_exit_price,
                    'Size': stock_quantity,
                    'ReturnPct': trade_return
                }
                long_exit_trade_info.append(exit_info)

                # Track win/loss performance
                if trade_return > 0:
                    num_wins += 1
                    sum_win_percent += trade_return
                else:
                    num_losses += 1
                    sum_loss_percent += trade_return

            # Update maximum drawdown
            current_drawdown = (peak_balance - balance) / peak_balance if peak_balance != 0 else 0
            max_drawdown = max(max_drawdown, current_drawdown)

        # After the loop ends
        if in_trade:
            # Close the position at the last price
            trade_exit_price = prices_df.iloc[-1]['Close']
            trade_return = (trade_exit_price - trade_entry_price) / trade_entry_price * 100
            trade_returns.append(trade_return)
            logd(f"Trade closed at end of data for {symbol} @ {trade_exit_price}")

            # Update balance for the final trade
            balance = balance + (stock_quantity * trade_exit_price)
            stock_quantity = 0
            peak_balance = max(peak_balance, balance)

            # Track win/loss performance for the final trade
            if trade_return > 0:
                num_wins += 1
                sum_win_percent += trade_return
            else:
                num_losses += 1
                sum_loss_percent += trade_return

        # Close any open trades automatically
        if in_trade:
            # Close the position at the last price
            trade_exit_price = prices_df.iloc[-1]['Close']
            trade_return = (trade_exit_price - trade_entry_price) / trade_entry_price * 100
            trade_returns.append(trade_return)
            logd(f"Trade closed at end of data for {symbol} @ {trade_exit_price}")

            # Update balance for the final trade
            balance = balance + (stock_quantity * trade_exit_price)

            # Track win/loss performance for the final trade
            if trade_return > 0:
                num_wins += 1
                sum_win_percent += trade_return
            else:
                num_losses += 1
                sum_loss_percent += trade_return

            # track trades
            trade_info = {
                'ExitBar': index,
                'ExitPrice': trade_exit_price,
                'Size': stock_quantity,
                'ReturnPct': trade_return
            }
            long_exit_trade_info.append(trade_info)


        # Calculate final metrics
        total_return = ((balance - self.initial_balance) / self.initial_balance) * 100
        win_rate = (num_wins / num_trades) if num_trades > 0 else 0
        average_win_percent = (sum_win_percent / num_wins) if num_wins > 0 else 0
        average_loss_percent = (sum_loss_percent / num_losses) if num_losses > 0 else 0
        sharpe_ratio = calculate_sharpe_ratio(trade_returns, self.risk_free_rate)
        logd(f"total return: {round(total_return, 2)}")

        # Create a DataFrame from the trades information
        long_entry_trades_info_df = pd.DataFrame(long_entry_trade_info)
        long_exit_trades_info_df = pd.DataFrame(long_exit_trade_info)

        # Compile results
        result = BacktestResult(
            symbol=symbol,
            total_return=total_return,
            buy_hold_return=buy_hold_return,
            num_trades=num_trades,
            max_drawdown=max_drawdown,
            num_wins=num_wins,
            num_losses=num_losses,
            win_rate=win_rate,
            average_win_percent=average_win_percent,
            average_loss_percent=average_loss_percent,
            sharpe_ratio=sharpe_ratio,
            long_entry_trades_info_df=long_entry_trades_info_df,
            long_exit_trades_info_df=long_exit_trades_info_df
        )

        return result

    def check_risk_management(self, rm_methods, high_minute_prices, low_minute_prices, tp_price, stop_price, trailing_stop_price):
        if high_minute_prices is None or low_minute_prices is None:
            return None, None
        risk_methods = []
        for rm_method in rm_methods:
            risk_methods.append(rm_method.item_type)

        # Shuffle to avoid bias regarding which exit method is checked first
        random.shuffle(risk_methods)

        # Iterate through each minute and check for stop loss/trailing stop and take profit
        for i in range(max(len(low_minute_prices), len(high_minute_prices))):
            low_price = low_minute_prices[i] if i < len(low_minute_prices) else None
            high_price = high_minute_prices[i] if i < len(high_minute_prices) else None

            for rm_type in risk_methods:
                if low_price is not None:
                    if rm_type == RiskMgtMethodType.STOP_LOSS and low_price <= stop_price:
                        return rm_type, stop_price
                    elif rm_type == RiskMgtMethodType.TRAILING_STOP and low_price <= trailing_stop_price:
                        return rm_type, trailing_stop_price

                if high_price is not None:
                    if rm_type == RiskMgtMethodType.TAKE_PROFIT and high_price >= tp_price:
                        return rm_type, tp_price

        return None, None

    def execute_backtest(self, strategy):
        logd(f"Backtesting strategy '{strategy.id}'...")
        backtest_results = []
        for symbol in self.prices_dict:
            logd(f"Running backtest for {symbol}, strategy '{strategy.id}'...")
            price_data = self.prices_dict[symbol]
            high_minute_price_map = price_data.high_price_map
            low_minute_price_map = price_data.low_price_map
            test_prices_df = price_data.prices_df.copy()

            # Calculate signals for entry and exit indicators
            for indicator in strategy.entry_indicators:
                test_prices_df = indicator.generate_long_signals(test_prices_df)
            for indicator in strategy.exit_indicators:
                test_prices_df = indicator.generate_long_signals(test_prices_df)

            # Execute strategy
            results = self.execute_strategy(symbol, strategy, test_prices_df, high_minute_price_map, low_minute_price_map)
            backtest_results.append(results)

            # Plot results
            if symbol in self.plot_list:
                plot_bokeh_chart(symbol,
                                 strategy,
                                 test_prices_df,
                                 results,
                                 results.long_entry_trades_info_df,
                                 results.long_exit_trades_info_df)

        return backtest_results
