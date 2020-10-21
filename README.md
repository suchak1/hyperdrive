| <img src="img/arc3.png" width="50" /> | _scarlett_: Robinhood analytics and algorithmic trading |
| ------------------------------------- | ------------------------------------------------------- |


![Build Pipeline](https://github.com/suchak1/scarlett/workflows/Build%20Pipeline/badge.svg) ![Dev Pipeline](https://github.com/suchak1/scarlett/workflows/Dev%20Pipeline/badge.svg) ![New Release](https://github.com/suchak1/scarlett/workflows/New%20Release/badge.svg)

_scarlett_ is a project to obtain stock data, create trading strategies, test against historical data (backtesting), and deploy strategies for algorithmic trading.

## Getting Started

### Prerequisites

You will need Python 3.8+ and a Robinhood account.

Place your credentials in a file named `.env` in the project root directory.
Follow this structure:

```
RH_USERNAME=...
RH_PASSWORD=...
RH_2FA=...
IEXCLOUD=...
```

### Installation

To install the necessary packages, run

```
pip install -r requirements.txt
```

## Use

### Making Scripts

To make a script, create a new .py file in the `scripts/` dir with the following code:

```
import sys
sys.path.append('src')
from Algotrader import Scarlett  # noqa autopep8

sl = Scarlett()
```

## Features:

- [x] Broker authentication
- [ ] Automated data storage
- [ ] Backtesting engine
- [ ] Monte Carlo simulations
- [ ] Plotting and technical analysis
- [ ] Model training
- [ ] Strategy definition (start with buy and hold)
- [ ] Buy and sell functionality
- [ ] Live trading
- [ ] Documentation

Check out the [Roadmap](https://github.com/suchak1/scarlett/projects/2) for progress
...

### Auth

Using Robinhood 2FA, we can simply provide our MFA one-time password in the `.env` file to login to Robinhood (via `pyotp`).

### Data

- [ ] Price and Volume
  - [x] ![Symbols](https://github.com/suchak1/scarlett/workflows/Symbols/badge.svg)
  - [x] ![OHLC](https://github.com/suchak1/scarlett/workflows/OHLC/badge.svg)
  - [ ] Intraday 1 or 5 min OHLCV
- [x] Actions
  - [x] ![Dividends](https://github.com/suchak1/scarlett/workflows/Dividends/badge.svg)
  - [x] ![Splits](https://github.com/suchak1/scarlett/workflows/Splits/badge.svg)
  - [ ] Mergers
- [ ] Sentiment
  - [ ] News Sentiment
  - [x] ![Social Sentiment](<https://github.com/suchak1/scarlett/workflows/Social%20Sentiment%20(1)/badge.svg>)
  - [ ] Analyst Recommendations
- [ ] Company / Micro
  - [ ] Profile (Sector, # of Employees)
  - [ ] Earnings
  - [ ] Cash Flow
  - [ ] CEO Compensation
- [ ] Government / Macro

  - [ ] Unemployment Rate
  - [ ] Real GDP
  - [ ] US Recession Probabilities

- [ ] Market
  - [ ] General Volatility (VIX)
  - [ ] Sector Performance

---
