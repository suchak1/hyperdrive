from time import sleep
from datetime import datetime, timedelta
from Constants import TZ, DATE_FMT, TIME_FMT, PRECISE_TIME_FMT


class TimeTraveller:
    def convert_delta(self, timeframe):
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

    def convert_dates(self, timeframe, format=DATE_FMT):
        # if timeframe='max': timeframe = '25y'
        end = datetime.now(TZ) - self.convert_delta('1d')
        delta = self.convert_delta(timeframe) - self.convert_delta('1d')
        start = end - delta
        if format:
            start = start.strftime(format)
            end = end.strftime(format)
        return start, end

    def dates_in_range(self, timeframe, format=DATE_FMT):
        start, end = self.convert_dates(timeframe, None)
        dates = [start + timedelta(days=x)
                 for x in range(0, (end - start).days + 1)]
        if format:
            dates = [date.strftime(format) for date in dates]
        return dates

    def get_time(self, time):
        return datetime.strptime(
            time, TIME_FMT if len(time.split(':')) == 2 else PRECISE_TIME_FMT
        ).time()

    def combine_date_time(self, date, time):
        date = datetime.strptime(date, DATE_FMT)
        time = self.get_time(time)
        return date.combine(date, time)

    def get_diff(self, t1, t2):
        return abs((t1 - t2).total_seconds())

    def sleep_until(self, time):
        # time could be "00:00"
        curr = datetime.utcnow()
        prev_sched = datetime.combine(curr.date(), self.get_time(time))
        next_sched = prev_sched + timedelta(days=1)

        prev_diff = self.get_diff(curr, prev_sched)
        next_diff = self.get_diff(curr, next_sched)

        sched = next_sched if next_diff < prev_diff else prev_sched
        diff = self.get_diff(curr, sched) if sched > curr else 0

        while diff > 0:
            curr = datetime.utcnow()
            diff = self.get_diff(curr, sched) if sched > curr else 0
            sleep(diff)
