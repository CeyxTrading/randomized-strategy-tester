class BacktestResult:
    def __init__(self,
                 symbol,
                 total_return,
                 buy_hold_return,
                 num_trades,
                 max_drawdown,
                 num_wins,
                 num_losses,
                 win_rate,
                 average_win_percent,
                 average_loss_percent,
                 sharpe_ratio,
                 long_entry_trades_info_df,
                 long_exit_trades_info_df):
        self.symbol = symbol
        self.total_return = total_return
        self.buy_hold_return = buy_hold_return
        self.num_trades = num_trades
        self.max_drawdown = max_drawdown
        self.num_wins = num_wins
        self.num_losses = num_losses
        self.win_rate = win_rate
        self.average_win_percent = average_win_percent
        self.average_loss_percent = average_loss_percent
        self.sharpe_ratio = sharpe_ratio
        self.long_entry_trades_info_df = long_entry_trades_info_df
        self.long_exit_trades_info_df = long_exit_trades_info_df

    def to_dict(self):
        return {
            'total_return': self.total_return,
            'buy_hold_return': self.buy_hold_return,
            'num_trades': self.num_trades,
            'max_drawdown': self.max_drawdown,
            'num_wins': self.num_wins,
            'num_losses': self.num_losses,
            'win_rate': self.win_rate,
            'average_win_percent': self.average_win_percent,
            'average_loss_percent': self.average_loss_percent,
            'sharpe_ratio': self.sharpe_ratio
        }
