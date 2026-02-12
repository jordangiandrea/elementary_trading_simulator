import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

"""Get data on SPY from Yahoo Finance"""
ticker = "SPY"   # S&P 500 ETF
data = yf.download(
    ticker,
    start="2015-1-01",
    end="2026-01-01",
    interval="1d"
)
#Clean up the data
data = data.dropna()
data = data.sort_index()

prices = data["Close"]
returns = prices.pct_change()
rolling_vol = returns.rolling(window=20).std().shift(1)

CASH = 100_000
CAP_PERCENT = 0.01
LATENCY = 1
K_SLIP = 0.5
K_SPREAD = 0.5

def strategy(hist):
    """
    If the ten-day average is greater than fifty-day average, returns buy. If not, returns sell.
    
    :param hist: data frame of historical close prices
    """
    if len(hist) < 50:
        return 0
    short = hist["Close"].iloc[-10:].mean()
    long = hist["Close"].iloc[-50:].mean()

    if float(short) > float(long):
        return 1 #buy
    else:
        return -1 #sell

def execute_trade(price, vol, side,
                  k_spread,
                  k_slip):

    if np.isnan(vol):
        vol = 0  # early periods

    spread_pct = k_spread * vol
    slip = np.random.normal(0, k_slip * vol)

    exec_price = 0

    if side == 1:
        exec_price = price * (1 + spread_pct / 2)
        exec_price *= (1 + slip)

    elif side == -1:
        exec_price = price * (1 - spread_pct / 2)
        exec_price *= (1 + slip)

    return exec_price

def market_sim(cash,cap_percent,latency):

    equity_curve = []
    equity_curve.append(cash)
    position = 0

    for t in range(0, len(data)-latency):
        price = data["Close"].iloc[t]
        exec_price = data["Close"].iloc[t+latency]
        current_vol = rolling_vol.iloc[t][0]

        signal = strategy(data.iloc[:t])
        fill = execute_trade(exec_price,current_vol,signal, K_SPREAD,K_SLIP)
        
        position_size = cap_percent * cash / price

        if signal == 1 and float(cash) >= float(price):
            position += position_size
            cash -= fill

        elif signal == -1 and float(position) > 0:
            position -= position_size
            cash += fill
 
        equity = cash + position * price
        equity_curve.append(equity)

    equity_series = pd.Series(equity_curve, index=prices.index)
    return equity_series

results = market_sim(CASH,CAP_PERCENT,LATENCY)

fig, axes = plt.subplots(nrows=2, ncols=2,)

axes[0,0].plot(prices, label="SPY Prices", color='blue')
axes[0,0].set_xlabel("Date")
axes[0,0].set_title('SPY Prices')

axes[0,1].plot(results, label="Equity Curve", color='red')
axes[0,1].set_xlabel("Date")
axes[0,1].set_title('Equity')

axes[1,0].plot(rolling_vol, label="20-Day Rolling SPY Volatility", color='green')
axes[1,0].set_xlabel("Date")
axes[1,0].set_title('20-Day Rolling SPY Volatility')

plt.show()
