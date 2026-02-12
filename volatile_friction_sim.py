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
K_SPREAD = 0.5
K_SLIP = 0.5
CAP_PERCENT = 0.01
LATENCY = 1

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

def market_sim(cash,spread,slip_var,k_slip,k_spread,cap_percent,latency):

    equity_curve = []
    equity_curve.append(cash)
    position = 0
    slippage = np.random.normal(0, slip_var)

    for t in range(0, len(data)-latency):
        price = data["Close"].iloc[t]
        exec_price = data["Close"].iloc[t+latency]
        current_vol = rolling_vol.iloc[t]
        spread_pct = k_spread*current_vol

        signal = strategy(data.iloc[:t])
        position_size = cap_percent * cash / price

        if signal == 1 and float(cash) >= float(price):
            buy_price = (exec_price + spread/2)*(1+slippage) 
            position += position_size
            cash -= buy_price

        elif signal == -1 and float(position) > 0:
            sell_price = (exec_price - spread/2)*(1+slippage)
            position -= position_size
            cash += sell_price
 
        equity = cash + position * price
        equity_curve.append(equity)

    equity_series = pd.Series(equity_curve, index=prices.index)
    return equity_series

results = market_sim(CASH,SPREAD,SLIP_VAR,CAP_PERCENT,LATENCY)

fig, axes = plt.subplots(nrows=1, ncols=2,)

axes[0].plot(prices, label="SPY Prices", color='blue')
axes[0].set_xlabel("Date")
axes[0].set_title('SPY Prices')

axes[1].plot(results, label="Equity Curve", color='red',linestyle='--')
axes[1].set_xlabel("Date")
axes[1].set_title('Equity')

plt.show()
