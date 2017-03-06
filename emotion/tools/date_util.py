import datetime
import re


class DateUtil(object):

    today = '今天'
    yesterday = '昨天'
    other_pattern = '([0-9]{1,2})月([0-9]{1,2})日'
    regex = re.compile(other_pattern)
    def __init__(self):
        pass


    @classmethod
    def analysis_data(cls, date_str):
        date = datetime.date.today()
        month = date.month
        year = date.year
        day = date.day
        hour = 0
        min = 0
        date, time = date_str.split(' ')
        if cls.today in date:
            pass
        if cls.yesterday in date:
            pass
        else:
            m = cls.regex.search(date)
            if m:
                month = m.group(1)
                day = m.group(2)
        hour,min = time.split(":")
        return datetime.datetime(int(year),int(month),int(day),int(hour),int(min))

    @classmethod
    def str2date(cls, date_str):
        return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M')


    @classmethod
    def date2str(cls, dtime):
        return dtime.strftime('%Y-%m-%d %H:%M')


if __name__ == "__main__":
    #regex = re.compile("([0-9]{1,2})月([0-9]{1,2})日")
    #m = regex.search("2月22日")
    #print(m.group(1))
    str = '2017-10-10 13:00'
    print(DateUtil.str2date(str))