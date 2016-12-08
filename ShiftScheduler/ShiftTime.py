from enum import Enum
import datetime

def make_time(hour, min):
    """
    Returns a properly formatted time given an hour and a minute
    :param hour: An integer representing the hour in military time
    :param min: An integer representing the minute in military time
    :return: a 'time' object containing an hour and a minute property
    """
    return datetime.time(hour=hour, minute=min)

class Day(Enum):
    monday = 1
    tuesday = 2
    wednesday = 3
    thursday = 4
    friday = 5
    saturday = 6
    sunday = 7

    def __str__(self):
        return self.name

class ShiftTime():
    """
    Class that represents the time of a shift
    """
    day = Day.monday
    time = make_time(00, 00)

    def __init__(self, day, hour, min):
        self.day = day
        self.time = make_time(hour, min)

    def __str__(self):
        return str(self.day) + " at " + str(self.time)

def shift_time_from_range(start_time, end_time):
    """
    Returns a list of ShiftTime's from given time range.
    These times are separated by at least 30 minutes, generally
    on the :00 and :30 minute marks
    :return: A List of ShiftTimes
    """
    # TODO
    return []

if __name__ == "__main__":
    day1 = Day.tuesday
    day2 = Day.friday

    time1 = make_time(12, 30)
    time2 = make_time(14, 15)

    shift1 = ShiftTime(day1, time1)
    shift2 = ShiftTime(day2, time2)

    print(str(shift1))
    print(str(shift2))