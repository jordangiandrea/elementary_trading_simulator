# elementary_trading_simulator

Single asset (SPY stock) market simulation with increasing realism for backtesing moving average trading strategy

## Architecture

The simulator is structured into three logical layers:

- Strategy Layer — generates trading signals and risk rules
- Execution Layer — models market frictions (spread, slippage)
- Portfolio Layer — updates capital and position accounting

## Features by Version

### baseline_sim
- Market orders execute at closing price
- Either buy or sell only one share per day
- No transaction costs
- No market friction

### constant_friction_sim
- Stop-loss support
- Fixed fractional position sizing (risk % per trade)
