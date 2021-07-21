import sys
sys.path.append('src')
from Adjustment import SplitWorker  # noqa autopep8
import Constants as C  # noqa autopep8

provider = 'polygon'
symbols = ['TSLA', 'AAPL', 'VWDRY', 'NEE', 'CP']
# if provider == 'polygon':
#     symbols.remove('VWDRY')
timeframe = '1y'
# timeframe = '18m'
worker = SplitWorker()
worker.process(symbols, timeframe, provider)


for symbol in splits:
    print(symbol)
    # print(splits[symbol])
    ohlc[symbol] = md.get_ohlc(symbol, timeframe)
    intra[symbol] = pd.concat(md.get_intraday(symbol, timeframe=timeframe))
    div[symbol] = md.get_dividends(symbol, timeframe)

    last_split = splits[symbol].tail(1)
    ex = last_split[C.EX].iloc[0]
    ratio = last_split[C.RATIO].iloc[0]

    # OHLC
    row_before_ex_date = ohlc[symbol][ohlc[symbol]
                                      [C.TIME] < ex].tail(1)
    row_on_ex_date = ohlc[symbol][ohlc[symbol]
                                  [C.TIME] == ex]
    if len(row_before_ex_date) and len(row_on_ex_date):
        diff = row_on_ex_date.drop(
            [C.TIME], axis=1).iloc[0] / row_before_ex_date.drop([C.TIME], axis=1).iloc[0]
        diff[C.VOL] = 1 / diff[C.VOL]
        if C.TRADES in diff:
            diff[C.TRADES] = 1 / diff[C.TRADES]
        certainty = avg(abs(diff - ratio) < (ratio*0.1)) > 0.5

        if certainty:
            # update ohlc
            print(f'{symbol} needs to have OHLC adjusted for splits')

    # Intraday
    # need check to see if ex date is even in df - otherwise error single positional indexer is out-of-bounds
    row_before_ex_date = intra[symbol][intra[symbol]
                                       [C.TIME] < ex].tail(1)
    row_on_ex_date = intra[symbol][intra[symbol]
                                   [C.TIME] >= ex].head(1)

    print(row_before_ex_date)
    print(row_on_ex_date)
    if len(row_before_ex_date) and len(row_on_ex_date):
        diff = row_on_ex_date.drop(
            [C.TIME], axis=1).iloc[0] / row_before_ex_date.drop([C.TIME], axis=1).iloc[0]
        diff[C.VOL] = 1 / diff[C.VOL]
        if C.TRADES in diff:
            diff[C.TRADES] = 1 / diff[C.TRADES]
        # certainty = avg(abs(diff - ratio) < 0.02) > 0.5
        certainty = avg(abs(diff - ratio) < (ratio*0.1)) > 0.5

        if certainty:
            # update intraday
            print(f'{symbol} needs to have Intraday adjusted for splits')

    # Dividends
    # implement few days smart check
    # implement split update
    # test w expected iexcloud and polygon updates
    # write tests
    # split worker class
    # make sure trades number is as expected for iexcloud and polygon (verify ratio)
    # use intraday specific logic
    # create scheduled workflow and have try catches
    # whatever logic here

# update dividend, ohlc (prices, volume, num trades), and intraday (prices, volume, num trades)
# prices * ratio and vol or trades / ratio?
