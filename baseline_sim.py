import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

"""Get data on SPY from Yahoo Finance"""
ticker = "SPY"   # S&P 500 ETF
data = yf.download(
    ticker,
    start="2015-01-01",
    end="2024-01-01",
    interval="1d"
)

#Clean up the data
data = data.dropna()
data = data.sort_index()

prices = data["Close"]

cash = 100_000
position = 0

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
        return 1
    else:
        return -1

equity_curve = []

for t in range(0, len(data)):
    price = data["Close"].iloc[t]

    signal = strategy(data.iloc[:t])
    
    if signal == 1 and float(cash) >= float(price):
        position += 1
        cash -= price

    elif signal == -1 and position > 0:
        position -= 1
        cash += price

    equity = cash + position * price
    equity_curve.append(equity)

equity_series = pd.Series(equity_curve, index=prices.index)

fig, axes = plt.subplots(nrows=1, ncols=2,)

axes[0].plot(prices, label="SPY Prices", color='blue')
axes[0].set_xlabel("Date")
axes[0].set_title('SPY Prices')

axes[1].plot(equity_series, label="Equity Curve", color='red',linestyle='--')
axes[1].set_xlabel("Date")
axes[1].set_title('Equity')

plt.show()
