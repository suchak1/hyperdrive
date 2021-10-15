| <img src="https://raw.githubusercontent.com/suchak1/hyperdrive/master/img/1.png" width="75" /> | _hyperdrive_: Robinhood analytics and algorithmic trading |
| ---------------------------------------------------------------------------------------------- | --------------------------------------------------------- |

![Build Pipeline](https://github.com/suchak1/hyperdrive/workflows/Build%20Pipeline/badge.svg) ![Dev Pipeline](https://github.com/suchak1/hyperdrive/workflows/Dev%20Pipeline/badge.svg) ![New Release](https://github.com/suchak1/hyperdrive/workflows/New%20Release/badge.svg)

_hyperdrive_ is a project to obtain stock data, create trading strategies, test against historical data (backtesting), and deploy strategies for algorithmic trading.

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

### Testing

```
python -m pytest -s -v test/test_filename -k function_name
```

## Use

### Making Scripts

To make a script, create a new .py file in the `scripts/` dir with the following code:

```
import sys
sys.path.append('src')
from Algotrader import HyperDrive  # noqa autopep8

drive = HyperDrive()
```

## Features:

- [x] Broker authentication
- [x] Automated data storage
- [x] Backtesting engine
- [ ] Monte Carlo simulations
- [ ] Plotting and technical analysis
- [ ] Model training
- [x] Strategy definition (start with buy and hold)
- [ ] Buy and sell functionality
- [ ] Live trading
- [ ] Documentation

Check out the [Roadmap](https://github.com/suchak1/hyperdrive/projects/2) for progress
...

### Auth

Using Robinhood 2FA, we can simply provide our MFA one-time password in the `.env` file to login to Robinhood (via `pyotp`).

### Data

- [x] Price and Volume
  - [x] [![Symbols](https://github.com/suchak1/hyperdrive/workflows/Symbols/badge.svg)](https://github.com/suchak1/hyperdrive/actions?query=workflow%3ASymbols)
  - [x] [![OHLC](https://github.com/suchak1/hyperdrive/workflows/OHLC/badge.svg)](https://github.com/suchak1/hyperdrive/actions?query=workflow%3AOHLC)
  - [x] [![Intraday](https://github.com/suchak1/hyperdrive/workflows/Intraday/badge.svg)](https://github.com/suchak1/hyperdrive/actions?query=workflow%3AIntraday)
- [x] Actions
  - [x] [![Dividends](https://github.com/suchak1/hyperdrive/workflows/Dividends/badge.svg)](https://github.com/suchak1/hyperdrive/actions?query=workflow%3ADividends)
  - [x] [![Splits](https://github.com/suchak1/hyperdrive/workflows/Splits/badge.svg)](https://github.com/suchak1/hyperdrive/actions?query=workflow%3ASplits)
- [ ] Sentiment
  - [ ] News Sentiment
  - [x] [![Social Sentiment](<https://github.com/suchak1/hyperdrive/workflows/Social%20Sentiment%20(1)/badge.svg>)](https://github.com/suchak1/hyperdrive/actions?query=workflow%3A%22Social+Sentiment+%281%29%22)
  - [ ] [Investor Sentiment](http://www.aaii.com/files/surveys/sentiment.xls)
  - [ ] Analyst Recommendations
- [ ] Company / Micro
  - [ ] Profile (Sector, # of Employees)
  - [ ] Earnings
  - [ ] Cash Flow
  - [ ] CEO Compensation
- [ ] Government / Macro <!-- this stuff prob won't be v useful -->
  - [x] [![Unemployment](https://github.com/suchak1/hyperdrive/workflows/Unemployment/badge.svg)](https://github.com/suchak1/hyperdrive/actions?query=workflow%3AUnemployment) <!-- BLS -->
  - [ ] Real GDP <!-- BEA -->
  - [ ] US Recession Probabilities <!-- FRED -->
- [ ] Market
  - [ ] General Volatility (VIX)
  - [ ] Sector Performance

### Strategy

- [x] Buy and Hold
- [ ] Indicator/TA based
- [ ] Portfolio Optimization

---
