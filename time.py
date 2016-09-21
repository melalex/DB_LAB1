import re


class Time(object):

    def __init__(self, time_str):
        time = re.match(r'^(([0,1][0-9])|(2[0-3])):[0-5][0-9]$', time_str)
        if time:
            buff_list = time.group(0).split(':')
            self._time = int(buff_list[0]) * 3600
            self._time += int(buff_list[1]) * 60
        else:
            raise ValueError

    @property
    def time(self):
        return self._time

    def __ge__(self, other):
        return self.time >= other.time

    def __str__(self):
        hours = self._time // 3600
        minutes = self.time // 60
        return str(hours) + ':' + str(minutes)
