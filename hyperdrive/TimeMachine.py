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
        target_time = self.get_time(time)
        target_seconds = target_time.hour * 3600 + \
            target_time.minute * 60 + target_time.second
        sec_in_a_day = int(timedelta(days=1).total_seconds())

        # while
        now = datetime.utcnow()

        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        seconds = (now - midnight).seconds

        # cases:
        # curr: 11pm, sched: 1am
        # result: wait 2hr
        # curr > sched
        # curr is before midnight and sched is after midnight
        # curr is after noon and sched is before noon

        # curr: 1pm, sched: 3pm
        # result: wait 2hr
        # curr < sched
        # curr is before midnight and sched is before midnight
        # curr is after noon and sched is after noon

        # curr: 1am, sched: 11pm
        # result: no wait, return
        # curr < sched
        # curr is after midnight and sched is before midnight
        # curr is before noon and sched is after noon

        # curr: 3pm, sched: 1pm
        # result: no wait, return
        # curr > sched
        # curr is before midnight and sched is before midnight
        # curr is after noon and sched is after noon


# times close to noon are anomaly
        # curr: 11am, sched: 1pm
        # result: wait 2hr
        # curr < sched
        # curr is before noon and sched is after noon

        # curr: 1pm, sched: 11am
        # result: no wait, return
        # curr > sched
        # curr is after noon and sched is before noon

        if seconds > target_seconds:
            #
            return
