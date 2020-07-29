from Broker import Robinhood


class Scarlett:
    # scarlett should have attrs Broker, Backtester, Strategy

    def __init__(self, load=False):

        self.broker = Robinhood()

        if load is True:
            self.broker.load_portfolio()


# Scarlett(load=True).save_symbols()
