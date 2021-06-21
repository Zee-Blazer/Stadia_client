import re
import datetime


class DateTimeHandler:
    def __init__(self, date_n_time):
        """
        Takes a date and time string with the format "MM/DD/YYYY HH/MM"

        This was built to be part of a more robust application and is built
        to withstand greater time handling effects.
        """

        if self.__validate_format(date_n_time):
            self.data_n_time = date_n_time
            self.datetime = None

            self.__set_date_n_time()
        else:
            raise ValueError("Invalid datetime format")

    def __set_date_n_time(self):
        """
        Sets datetime attribute to datetime module format
        """
        _date, _time, _quart = self.data_n_time.split(' ')

        month, day, year = map(int, _date.split('/'))
        hour, minutes = map(int, _time.split(':'))

        if _quart == 'PM':
            if hour > 12:
                raise ValueError("Invalid Time Format")
            else:
                hour += 12

        self.datetime = datetime.datetime(year, month, day, hour, minutes)

    def __time_past(self):
        time_diff = self.datetime - datetime.datetime.now()

        return not (time_diff.seconds <= 1 or time_diff.days < 0), time_diff

    def on_set_time(self):
        time_diff = self.datetime - datetime.datetime.now()

        return not (time_diff.seconds <= (10 * 60) or time_diff.days < 0)

    @staticmethod
    def cal(time_diff):
        def mask(val, term):
            if val > 1:
                term += "s"
            return val, term

        context = dict()
        context['days'] = mask(time_diff.days, "day")

        seconds = time_diff.seconds

        context['hours'] = mask((seconds // (60 * 60)), "hr")
        seconds = seconds % (60 * 60)

        context['minutes'] = mask((seconds // 60), "min")
        seconds %= 60

        context['seconds'] = mask(seconds, "sec")

        return context

    def time_left(self):
        _, time_diff = self.__time_past()

        if _:
            time_repr = self.cal(time_diff)

            for _time in ['days', 'hours', 'minutes', 'seconds']:
                if time_repr[_time][0] != 0:
                    return ' '.join(map(str, time_repr[_time]))

    @staticmethod
    def __validate_format(_format):
        return bool(re.match(r"^[0-1][1-2]|[0][1-9]|10/[0-3][1]|[0-2][2-9]/[0-9][0-9][0-9][0-9] "
                             r"[0-1][0-2]|[0][1-9]:[0-5][0-9] [AP]M$",
                             _format))


def day_prefix_setter(day):
    if str(day).endswith('1'):
        return 'st'
    elif str(day).endswith('2'):
        return 'nd'
    elif str(day).endswith('3'):
        return 'rd'
    else:
        return 'th'


def month_setter(month):
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November',
              'December']

    setter = {num: name for num, name in zip(range(1, 13), months)}

    return setter[month]
