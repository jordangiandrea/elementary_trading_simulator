# elementary_trading_simulator

Single asset (SPY stock) market simulation with increasing realism for backtesing moving average trading strategy

## Architecture

The simulator is structured into three logical layers:

- Strategy Layer — generates trading signals and risk rules
- Execution Layer — models market frictions (spread, slippage)
- Portfolio Layer — updates capital and position accounting

## Features by Version

### v0.1 baseline_sim
- Market orders execute at closing price
- Can only buy or sell one share per trade or hold
- No transaction costs
- No market friction

### v0.2 constant_friction_sim
- Added constant spread, the difference between lowest ask and highest bid
- Added constant slippage noise
- Either buy or sell a constant percent of cash worth of shares
- Added a next-bar rule so orders based on signal from the day's close price are made at the next day's close price

### v0.3 volatile_friction_sim
- Made spread and slippage noise proportional to 20-day rolling volatility

### v0.4 riskadj_sim
- _Coming soon..._

### v0.5 portfolio_acct_sim
- _Coming soon..._
