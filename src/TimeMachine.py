from datetime import datetime, timedelta
from Constants import TZ, DATE_FMT


class TimeTraveller:
    def convert_to_delta(self, timeframe):
        # convert timeframe to timedelta
        if timeframe == 'max':
            return timedelta(days=36500)

        periods = {'y': 365, 'm': 30, 'w': 7, 'd': 1}
        period = 'y'
        idx = -1

        for curr_period in periods:
            idx = timeframe.find(curr_period)
            if idx != -1:
                period = curr_period
                break

        if idx == -1:
            supported = ', '.join(list(periods))
            error_msg = f'Only certain suffixes ({supported}) are supported.'
            raise ValueError(error_msg)

        num = int(timeframe[:idx])
        days = periods[period] * num
        delta = timedelta(days=days)

        return delta

    def convert_to_timeframe(self, delta):
        # convert timedelta to timeframe
        days = int(delta.total_seconds() / timedelta(days=1).total_seconds())
        return f'{days}d'

    def add_timeframes(self, timeframes):
        delta = timedelta(days=0)
        for timeframe in timeframes:
            delta += self.convert_to_delta(timeframe)

        return self.convert_to_timeframe(delta)

    def get_start_and_end(self, timeframe, format=DATE_FMT):
        # if timeframe='max': timeframe = '25y'
        end = datetime.now(TZ) - self.convert_to_delta('1d')
        delta = self.convert_to_delta(timeframe) - self.convert_to_delta('1d')
        start = end - delta
        if format:
            start = start.strftime(format)
            end = end.strftime(format)
        return start, end

    def get_dates_in_timeframe(self, timeframe, format=DATE_FMT):
        start, end = self.get_start_and_end(timeframe, None)
        dates = [start + timedelta(days=x)
                 for x in range(0, (end - start).days + 1)]
        if format:
            dates = [date.strftime(format) for date in dates]
        return dates

    def combine_date_time(self, date, time):
        date = datetime.strptime(date, DATE_FMT)
        time = datetime.strptime(time, '%H:%M').time()
        return date.combine(date, time)
