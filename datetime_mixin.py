# @Date  : 2021/5/11
# @Author: Hugh
# @Email : 609799548@qq.com

import calendar
from datetime import datetime, timedelta


class DateTimeMixin(datetime):
    default_format = '%Y-%m-%d %H:%M:%S'

    def __new__(cls, year, month=None, day=None, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0):
        return super().__new__(cls, year, month, day, hour, minute, second, microsecond, tzinfo, fold=fold)

    def format_str(self, format_string=default_format):
        return self.strftime(format_string)

    def __repr__(self):
        return self.__str__()

    @property
    def today_start(self):
        return DateTimeMixin(self.year, self.month, self.day)

    @property
    def today_end(self):
        return DateTimeMixin(self.year, self.month, self.day, 23, 59, 59)

    def get_last_n_week_start(self, n, s=1):
        start = self - timedelta(days=self.isoweekday() + 7 - s + (n - 1) * 7)
        return DateTimeMixin(start.year, start.month, start.day)

    def get_last_n_week_end(self, n, s=1):
        end = self - timedelta(days=self.isoweekday() + (n - 1) * 7 + s - 1)
        end = DateTimeMixin(end.year, end.month, end.day, 23, 59, 59)
        return end

    def get_last_n_week_start_end(self, n):
        return self.get_last_n_week_start(n), self.get_last_n_week_end(n)

    def get_last_n_month_start(self, n):
        month = self.month - 1 - n
        year = self.year + month // 12
        month = month % 12 + 1
        return DateTimeMixin(year, month, 1)

    def get_last_n_month_end(self, n):
        month = self.get_last_n_month_start(n)
        month_end_day = calendar.monthrange(month.year, month.month)[-1]
        return DateTimeMixin(month.year, month.month, month_end_day, 23, 59, 59)

    def get_last_n_month_start_end(self, n):
        return self.get_last_n_month_start(n), self.get_last_n_month_end(n)

    @property
    def last_month_start(self):
        return self.get_last_n_month_start(1)

    @property
    def last_month_end(self):
        return self.get_last_n_month_end(1)

    @property
    def last_month_start_end(self):
        return self.get_last_n_month_start_end(1)

    @property
    def last_week_start(self):
        """最近一个自然周的周一0点0时0分0秒"""
        return self.get_last_n_week_start(1)

    @property
    def last_week_end(self):
        """最近一个自然周的周日23点59时59分59秒"""
        return self.get_last_n_week_end(1)

    @property
    def last_week_start_end(self):
        """最近一个自然周的周一0点0时0分0秒，周日23点59时59分59秒"""
        return self.get_last_n_week_start_end(1)


if __name__ == '__main__':
    dt = DateTimeMixin.fromtimestamp(datetime.now().timestamp())
    print(dt)
    print(dt.last_week_start, dt.last_week_end)
    print(dt.last_week_start_end)
    print(dt.last_month_start, dt.last_month_end)
    print(dt.last_month_start_end)
