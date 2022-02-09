from time import sleep
from datetime import datetime, timedelta
from Constants import TZ, DATE_FMT, TIME_FMT


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
        return datetime.strptime(time, TIME_FMT).time()

    def combine_date_time(self, date, time):
        date = datetime.strptime(date, DATE_FMT)
        time = self.get_time(time)
        return date.combine(date, time)

    def wait_until(self, time):
        # time could be "00:00"
        curr_time = datetime.utcnow()
        prev_sched_time = datetime.combine(
            curr_time.date(), self.get_time(time))
        next_sched_time = prev_sched_time + timedelta(days=1)

        prev_diff = abs((curr_time - prev_sched_time).total_seconds())
        next_diff = abs((curr_time - next_sched_time).total_seconds())

        sched_time = prev_sched_time
        # diff = prev_diff

        if next_diff < prev_diff:
            sched_time = next_sched_time
            # diff = next_diff

        diff = sched_time - curr_time if sched_time > curr_time else 0
        sleep(diff)
        # new idea:
        # take curr time and sched time w current day and sched time w next day
        # sched time will be one that is closer to curr time
        # diff = sched - curr if sched > curr else 0
        # sleep(diff)
