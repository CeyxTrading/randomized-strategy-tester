from config import *
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import row, column
from bokeh.plotting import output_file, save
from bokeh.models import Scatter
from bokeh.models import Legend, LegendItem
from bokeh.models import ColumnDataSource, LabelSet, Range1d
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import sys
import warnings
from colorsys import hls_to_rgb, rgb_to_hls
from itertools import cycle, combinations
from functools import partial
from typing import Callable, List, Union
from Strategy import Strategy

import numpy as np
import pandas as pd

from bokeh.colors import RGB
from bokeh.colors.named import (
    lime as BULL_COLOR,
    tomato as BEAR_COLOR
)
from bokeh.plotting import figure as _figure
from bokeh.models import (
    CrosshairTool,
    CustomJS,
    ColumnDataSource,
    NumeralTickFormatter,
    Span,
    HoverTool,
    Range1d,
    DatetimeTickFormatter,
    WheelZoomTool,
    LinearColorMapper,
)
try:
    from bokeh.models import CustomJSTickFormatter
except ImportError:  # Bokeh < 3.0
    from bokeh.models import FuncTickFormatter as CustomJSTickFormatter
from bokeh.io import output_notebook, output_file, show
from bokeh.io.state import curstate
from bokeh.layouts import gridplot
from bokeh.palettes import Category10
from bokeh.io import output_file
from bokeh.transform import factor_cmap
from collections import OrderedDict

from backtesting._util import _data_period, _as_list, _Indicator


# Function to create bar chart
def create_bar_chart(ax, data, title, xlabel, ylabel, color):
    bars = ax.bar(range(len(data)), data, color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels([f"{i * 10}%-{(i + 1) * 10}%" for i in range(len(data))])
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

    # Add values above bars
    for bar in bars:
        y_val = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, y_val, round(y_val, 2),
                verticalalignment='bottom', horizontalalignment='center',
                color='black', fontsize=8)


# Function to create scatter plots
def create_scatter(ax, x_data, y_data, title, xlabel, ylabel, color):
    ax.scatter(x_data, y_data, color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    # Add grid lines
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)


def plot_strategy_results_scatter(strategy_id, results_df):
    # Extract metrics from results_df
    total_returns = results_df['total_return']
    buy_hold_returns = results_df['buy_hold_return']
    num_trades = results_df['num_trades']
    max_drawdowns = results_df['max_drawdown']
    num_wins = results_df['num_wins']
    num_losses = results_df['num_losses']
    win_rates = results_df['win_rate']
    average_win_percents = results_df['average_win_percent']
    average_loss_percents = results_df['average_loss_percent']
    sharpe_ratios = results_df['sharpe_ratio']

    # Sort by total returns
    results_df = results_df.sort_values(by=['total_return'], ascending=[True])

    # Scatter plot for each metric
    fig, axs = plt.subplots(5, 2, figsize=(20, 40))

    # Scatter plots
    num_backtests = len(results_df)
    create_scatter(axs[0, 0], range(num_backtests), total_returns, 'Total Return', 'Stocks', '% Return', 'purple')
    create_scatter(axs[0, 1], range(num_backtests), buy_hold_returns, 'Buy & Hold Returns', 'Stocks', '% Return', 'purple')

    create_scatter(axs[1, 0], range(num_backtests), num_trades, 'Number of Trades', 'Stocks', 'Trades', 'purple')
    create_scatter(axs[1, 1], range(num_backtests), win_rates, 'Win Rate', 'Stocks', '% Win Rate', 'purple')

    create_scatter(axs[2, 0], range(num_backtests), num_wins, 'Number of Wins', 'Stocks', 'Wins', 'purple')
    create_scatter(axs[2, 1], range(num_backtests), num_losses, 'Number of Losses', 'Stocks', 'Losses', 'purple')

    create_scatter(axs[3, 0], range(num_backtests), average_win_percents, 'Average Win Percent per Trade', 'Stocks', '% Win', 'purple')
    create_scatter(axs[3, 1], range(num_backtests), average_loss_percents, 'Average Loss Percent per Trade', 'Stocks', '% Loss', 'purple')

    create_scatter(axs[4, 0], range(num_backtests), max_drawdowns, 'Max Drawdown', 'Stocks', '% Drawdown', 'purple')
    create_scatter(axs[4, 1], range(num_backtests), sharpe_ratios, 'Sharpe Ratio', 'Stocks', 'Ratio', 'purple')

    plt.tight_layout()

    # Store image
    file_name = f"{strategy_id}-metrics.png"
    path = os.path.join(STRATEGY_PLOTS_DIR, file_name)
    plt.savefig(path, format="png")


# Define the function to calculate decile averages
def calculate_decile_averages(results_df, column):
    column_sorted = results_df[column].sort_values()
    deciles = np.array_split(column_sorted, 10)
    return [decile.mean() for decile in deciles]


def plot_strategy_results_decile_bar_charts(strategy_id, results_df):
    # Calculate decile averages for each metric
    decile_averages_total_returns = calculate_decile_averages(results_df, 'total_return')
    decile_averages_buy_hold_returns = calculate_decile_averages(results_df, 'buy_hold_return')
    decile_averages_num_trades = calculate_decile_averages(results_df, 'num_trades')
    decile_averages_win_rates = calculate_decile_averages(results_df, 'win_rate')
    decile_averages_num_wins = calculate_decile_averages(results_df, 'num_wins')
    decile_averages_num_losses = calculate_decile_averages(results_df, 'num_losses')
    decile_averages_average_win_percents = calculate_decile_averages(results_df, 'average_win_percent')
    decile_averages_average_loss_percents = calculate_decile_averages(results_df, 'average_loss_percent')
    decile_averages_max_drawdowns = calculate_decile_averages(results_df, 'max_drawdown')
    decile_averages_sharpe_ratios = calculate_decile_averages(results_df, 'sharpe_ratio')

    # Create bar charts for each metric
    fig, axs = plt.subplots(5, 2, figsize=(20, 40))

    create_bar_chart(axs[0, 0], decile_averages_total_returns, 'Average Total Returns by Decile', 'Deciles',
                     'Average % Return', 'purple')
    create_bar_chart(axs[0, 1], decile_averages_buy_hold_returns, 'Average Buy & Hold Returns by Decile', 'Deciles',
                     'Average % Return', 'purple')
    create_bar_chart(axs[1, 0], decile_averages_num_trades, 'Average Number of Trades by Decile', 'Deciles',
                     'Trades', 'purple')
    create_bar_chart(axs[1, 1], decile_averages_win_rates, 'Average Win Rate by Decile', 'Deciles', '% Win Rate',
                     'purple')
    create_bar_chart(axs[2, 0], decile_averages_num_wins, 'Average Number of Wins by Decile', 'Deciles', 'Wins',
                     'purple')
    create_bar_chart(axs[2, 1], decile_averages_num_losses, 'Average Number of Losses by Decile', 'Deciles',
                     'Losses', 'purple')
    create_bar_chart(axs[3, 0], decile_averages_average_win_percents, 'Average Win Percent by Decile', 'Deciles',
                     '% Win', 'purple')
    create_bar_chart(axs[3, 1], decile_averages_average_loss_percents, 'Average Loss Percent by Decile', 'Deciles',
                     '% Loss', 'purple')
    create_bar_chart(axs[4, 0], decile_averages_max_drawdowns, 'Average Max Drawdown by Decile', 'Deciles',
                     '% Drawdown', 'purple')
    create_bar_chart(axs[4, 1], decile_averages_sharpe_ratios, 'Average Sharpe Ratio by Decile', 'Deciles', 'Ratio',
                     'purple')

    plt.tight_layout()

    # Store image
    file_name = f"{strategy_id}-metrics-deciles.png"
    path = os.path.join(STRATEGY_PLOTS_DIR, file_name)
    plt.savefig(path, format="png")


def create_legend_items(p, result):
    # Create a dummy invisible renderer for legend items
    dummy_renderer = [p.circle([], [], visible=False)]

    # Create LegendItems for each metric
    legend_items = [
        LegendItem(label=f'Total Return: {result.total_return:.2f}%', renderers=dummy_renderer),
        LegendItem(label=f'Buy & Hold Return: {result.buy_hold_return:.2f}%', renderers=dummy_renderer),
        LegendItem(label=f'Number of Trades: {result.num_trades}', renderers=dummy_renderer),
        LegendItem(label=f'Max Drawdown: {result.max_drawdown:.2f}%', renderers=dummy_renderer),
        LegendItem(label=f'Number of Wins: {result.num_wins}', renderers=dummy_renderer),
        LegendItem(label=f'Number of Losses: {result.num_losses}', renderers=dummy_renderer),
        LegendItem(label=f'Win Rate: {result.win_rate:.2f}%', renderers=dummy_renderer),
        LegendItem(label=f'Average Win Percent: {result.average_win_percent:.2f}%', renderers=dummy_renderer),
        LegendItem(label=f'Average Loss Percent: {result.average_loss_percent:.2f}%', renderers=dummy_renderer),
        LegendItem(label=f'Sharpe Ratio: {result.sharpe_ratio:.2f}', renderers=dummy_renderer)
    ]

    return legend_items


def plot_results(symbol, strategy_id, df, result):
    # Ensure the date index is of type datetime if it's not already
    if not pd.api.types.is_datetime64_any_dtype(df['Date']):
        df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    inc = df.Close > df.Open
    dec = df.Open > df.Close

    w = 60 * 60 * 1000 * 0.8 # 80% for houly period

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(tools=TOOLS, title="Candlestick Chart", sizing_mode="stretch_width", plot_width=1000)

    # map dataframe indices to date strings and use as label overrides
    p.xaxis.major_label_overrides = {
        i: date.strftime('%b %d') for i, date in enumerate(df.index)
    }
    p.xaxis.bounds = (0, df.index[-1])
    p.xaxis.major_label_orientation = 1.2  # Optional: change orientation of labels

    # Use the ColumnDataSource to pass data to Bokeh glyphs
    source_inc = ColumnDataSource(data=dict(
        Date=df.index[inc],
        Open=df.Open[inc],
        Close=df.Close[inc],
        High=df.High[inc],
        Low=df.Low[inc]
    ))

    source_dec = ColumnDataSource(data=dict(
        Date=df.index[dec],
        Open=df.Open[dec],
        Close=df.Close[dec],
        High=df.High[dec],
        Low=df.Low[dec]
    ))

    # Add the green bars for days closing higher than their open
    p.vbar(x='Date', width=w, top='Close', bottom='Open', fill_color="green", line_color="black", source=source_inc)

    # Add the red bars for days closing lower than their open
    p.vbar(x='Date', width=w, top='Open', bottom='Close', fill_color="red", line_color="black", source=source_dec)

    p.segment('Date', 'High', 'Date', 'Low', color="black", source=source_inc)
    p.segment('Date', 'High', 'Date', 'Low', color="black", source=source_dec)

    # Add hover tool
    p.add_tools(HoverTool(
        tooltips=[
            ("Date", "@Date{%Y-%m-%d}"),
            ("Open", "@Open"),
            ("Close", "@Close"),
            ("High", "@High"),
            ("Low", "@Low")
        ],
        formatters={'@Date': 'datetime'}
    ))

    # Convert integer indices to datetime
    if len(result.long_entry_indices) > 0 and len(result.long_exit_indices) > 0:
        entry_dates = df.index[result.long_entry_indices]
        exit_dates = df.index[result.long_exit_indices]

        # Add long entry markers using Scatter
        entry_source = ColumnDataSource(data=dict(Date=entry_dates, Close=df.loc[entry_dates].Close))
        entry_marker = Scatter(x='Date', y='Close', size=8, fill_color="green", line_color="green", marker="triangle")
        p.add_glyph(entry_source, entry_marker)

        # Add long exit markers using Scatter
        exit_source = ColumnDataSource(data=dict(Date=exit_dates, Close=df.loc[exit_dates].Close))
        exit_marker = Scatter(x='Date', y='Close', size=8, fill_color="red", line_color="red",
                              marker="inverted_triangle")
        p.add_glyph(exit_source, exit_marker)

        # Plot lines between entry and exit points
        for i in range(len(entry_dates)):
            entry_index = entry_dates[i]
            exit_index = exit_dates[i]

            # Get entry and exit prices
            entry_price = df.loc[entry_index]['Close']
            exit_price = df.loc[exit_index]['Close']

            # Determine the color of the line based on trade result
            line_color = "green" if exit_price > entry_price else "red"

            # Draw the line
            p.line(
                [entry_index, exit_index],
                [entry_price, exit_price],
                line_width=1,
                color=line_color
            )

    # Combine plots
    p.add_tools(HoverTool(
        tooltips=[("Date", "@index{%F}"), ("Open", "@Open"), ("Close", "@Close"), ("High", "@High"), ("Low", "@Low")],
        formatters={"@index": "datetime"}))

    # Create a new plot for volume
    p_volume = figure(x_axis_type="datetime", tools=TOOLS, title="Volume", sizing_mode="stretch_width")
    p_volume.vbar(df.index, w, df.Volume, fill_color="blue", line_color="blue")

    p_volume.add_tools(
        HoverTool(tooltips=[("Date", "@index{%F}"), ("Volume", "@Volume")], formatters={"@index": "datetime"}))

    # Create an empty legend
    legend_items = create_legend_items(p, result)
    legend = Legend(items=legend_items, location="center")

    # Add the legend to your plot
    p.add_layout(legend, 'right')

    # show(column(p, p_volume))
    file_name = f"{symbol}-{strategy_id}.html"
    file_path = os.path.join(PLOT_DIR, file_name)
    output_file(file_path, title=f"Backtest for {symbol}")
    save(p)





OHLCV_AGG = OrderedDict((
    ('Open', 'first'),
    ('High', 'max'),
    ('Low', 'min'),
    ('Close', 'last'),
    ('Volume', 'sum'),
))


def plot_bokeh_chart(symbol,
                     strategy: Strategy,
                     df: pd.DataFrame,
                     results,
                     long_entry_trades_info_df,
                     long_exit_trades_info_df,
                     plot_width=None,
                     plot_volume=True,
                     open_browser=True):
    """
    Plot the candlestick chart, volume chart and trades.
    """
    df.set_index('Date', inplace=True)
    df_org = df.copy()
    df_org.reset_index(inplace=True)
    plot_volume = plot_volume and not df.Volume.isnull().all()
    #is_datetime_index = isinstance(df.index, pd.DatetimeIndex)

    df = df[list(OHLCV_AGG.keys())].copy(deep=False)

    df.index.name = None
    df['datetime'] = df.index
    df = df.reset_index(drop=True)

    new_bokeh_figure = partial(
        _figure,
        x_axis_type='datetime',
        width=plot_width,
        height=400,
        tools="xpan,xwheel_zoom,box_zoom,undo,redo,reset,save",
        active_drag='xpan',
        active_scroll='xwheel_zoom')

    fig_ohlc = new_bokeh_figure()

    original_datetime_index = df.index.copy()

    # Reset the index without dropping to keep the datetime column
    df.reset_index(inplace=True)

    # For the main OHLCV chart, it should look something like this:
    source = ColumnDataSource(data=dict(
        index=df.index,
        Open=df['Open'],
        High=df['High'],
        Low=df['Low'],
        Close=df['Close'],
        Volume=df['Volume'],
        datetime=df['datetime']
    ))
    source.add((df.Close >= df.Open).values.astype(np.uint8).astype(str), 'inc')

    inc_cmap = factor_cmap('inc', [BEAR_COLOR, BULL_COLOR], ['0', '1'])

    fig_ohlc.segment('index', 'High', 'index', 'Low', source=source, color="black")
    fig_ohlc.vbar('index', .8, 'Open', 'Close', source=source,
                  line_color="black", fill_color=inc_cmap)

    # Create an x_range for linking panning/zooming between plots
    #linked_x_range = fig_ohlc.x_range  # Link x-axis range to the main OHLCV chart
    # Create an x_range for linking panning/zooming between plots
    # This should be based on the numerical index range
    linked_x_range = Range1d(start=df.index[0], end=df.index[-1])

    plots = [fig_ohlc]

    if plot_volume:
        fig_volume = figure(x_axis_type='linear', width=plot_width, height=150,
                            x_range=linked_x_range, tools="", toolbar_location=None)
        fig_volume.vbar('index', .8, 'Volume', source=source, color=inc_cmap)
        fig_ohlc.xaxis.visible = False  # Hide the x-axis for the OHLC chart
        plots.append(fig_volume)


    # Define an offset value for the trade triangles
    y_offset = 0.005 * df['Close'].mean()

    # Convert trade entry/exit bar indices to datetime
    #long_entry_trades_info_df['EntryDateTime'] = df_org.iloc[long_entry_trades_info_df['EntryBar']].index
    #long_exit_trades_info_df['ExitDateTime'] = df_org.iloc[long_exit_trades_info_df['ExitBar']].index

    # Plot trades on OHLC chart
    if len(long_entry_trades_info_df) > 0:
        trade_entry_source = ColumnDataSource({
            'index': long_entry_trades_info_df['EntryBar'],
            'entry_price': long_entry_trades_info_df['EntryPrice'] + y_offset,
            'size': long_entry_trades_info_df['Size']
        })
        fig_ohlc.triangle(x='index', y='entry_price', source=trade_entry_source, color='green', size=10)

    if len(long_exit_trades_info_df) > 0:
        trade_exit_source = ColumnDataSource({
            'index': long_exit_trades_info_df['ExitBar'],
            'exit_price': long_exit_trades_info_df['ExitPrice'] + y_offset,
            'size': long_exit_trades_info_df['Size']
        })
        fig_ohlc.triangle(x='index', y='exit_price', source=trade_exit_source, color='red', size=10)

    #  Add lines between the trade entry and exits
    if len(long_entry_trades_info_df) > 0 and len(long_exit_trades_info_df) > 0:
        # Ensure that the number of entries and exits are equal
        min_length = min(len(long_entry_trades_info_df), len(long_exit_trades_info_df))
        line_xs = []
        line_ys = []
        line_colors = []

        for i in range(min_length):
            entry_bar = long_entry_trades_info_df['EntryBar'].iloc[i]
            exit_bar = long_exit_trades_info_df['ExitBar'].iloc[i]
            entry_price = long_entry_trades_info_df['EntryPrice'].iloc[i] + y_offset  # Applying offset
            exit_price = long_exit_trades_info_df['ExitPrice'].iloc[i] + y_offset  # Applying offset
            trade_return = (exit_price - entry_price) / entry_price

            # Start and end of line (entry and exit trade)
            line_xs.append([entry_bar, exit_bar])
            line_ys.append([entry_price, exit_price])

            # Determine line color based on trade return
            line_color = "green" if trade_return > 0 else "red"
            line_colors.append(line_color)

        # Create a ColumnDataSource for lines
        lines_source = ColumnDataSource({
            'xs': line_xs,
            'ys': line_ys,
            'colors': line_colors
        })

        # Draw dashed lines with color based on return
        fig_ohlc.multi_line(xs='xs', ys='ys', source=lines_source, line_color='colors', line_dash="dashed",line_width=1)

    # Add the indicator charts
    for indicator in strategy.entry_indicators + strategy.exit_indicators:
        fig_indicator = figure(x_axis_type='linear', width=plot_width, height=150,
                               x_range=linked_x_range, tools="", toolbar_location=None, title=indicator.name)

        # Add lines for the indicator and signal columns
        fig_indicator.line(df_org.index, df_org[indicator.indicator_column], line_width=1, color="blue")

        # Add a plot for the signal
        fig_signal = figure(x_axis_type='linear', width=plot_width, height=150,
                            x_range=linked_x_range, tools="", toolbar_location=None, title=indicator.name + " Signal")
        fig_signal.line(df_org.index, df_org[indicator.signal_column], line_width=1, color="orange")

        # Append the figure to the list of indicator plots
        plots.append(fig_indicator)
        plots.append(fig_signal)

    #  Create the layout
    layout = column(*plots, sizing_mode='scale_width')

    # Add the legend
    dummy_renderer = [fig_ohlc.circle(x=[], y=[], visible=False)]

    # Concatenate metrics into a single string
    metrics_str1 = (
        f"Symbol: {symbol}, "
        f"Strategy: {strategy.id}"
    )

    metrics_str2 = (
        f"Total Return: {results.total_return:.2f}%, "
        f"Buy & Hold Return: {results.buy_hold_return:.2f}%, "
        f"Number of Trades: {results.num_trades}, "
        f"Max Drawdown: {results.max_drawdown:.2f}%"
    )

    metrics_str3 = (
        f"Number of Wins: {results.num_wins}, "
        f"Number of Losses: {results.num_losses}, "
        f"Win Rate: {results.win_rate:.2f}%, "
        f"Average Win Percent: {results.average_win_percent:.2f}%, "
        f"Average Loss Percent: {results.average_loss_percent:.2f}%, "
        f"Sharpe Ratio: {results.sharpe_ratio:.2f}"
    )

    # Create a single LegendItem with the concatenated metrics
    legend_item1 = LegendItem(label=metrics_str1, renderers=dummy_renderer)
    legend_item2 = LegendItem(label=metrics_str2, renderers=dummy_renderer)
    legend_item3 = LegendItem(label=metrics_str3, renderers=dummy_renderer)

    # Create a Legend with these items
    legend = Legend(items=[legend_item1, legend_item2, legend_item3], location="top_left")

    # Style the legend
    legend.background_fill_alpha = 0.7  # Slightly transparent background
    legend.border_line_color = None
    legend.label_text_font_size = "8pt"  # Adjust font size

    # Add the Legend to the figure
    fig_ohlc.add_layout(legend, 'above')

    #  Create output file name
    file_name = f"{symbol}-{strategy.id}.html"
    path = os.path.join(PLOT_DIR, file_name)
    output_file(path)

    show(layout, browser=None if open_browser else 'none')

