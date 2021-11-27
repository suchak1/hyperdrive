
class Calculator:
    def delta(self, series):
        return series / series.shift() - 1
