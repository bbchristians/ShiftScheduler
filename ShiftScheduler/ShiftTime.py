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

    # TODO Delete?
    """
    def __gt__(self, other):
        # TODO Test
        assert type(other) is ShiftTime

        if self.day.value == other.day.value:
            if self.time.hour == other.time.hour:
                return self.time.minute > other.time.minute
            elif self.time.hour > other.time.hour:
                return True
        elif self.day.value > other.day.value:
            return True
        return False
    """

    def count(self):
        """
        :return: The count of the object (used to sort them)
        """
        return (self.day.value * 10000) + \
               (self.time.hour * 100) + \
                self.time.minute

    def increase(self):
        """
        Increases the current time by 30 minutes
        :return: None
        """
        new_time = None

        if self.time.minute == 00 :
            new_time = ShiftTime(day=self.day, hour=self.time.hour, min=30)
        elif self.time.minute > 0 and self.time.minute <= 30:
            new_time = ShiftTime(day=self.day, hour=self.time.hour+1, min=00)
        elif self.time.minute > 30:
            new_time = ShiftTime(day=self.day, hour=self.time.hour+1, min=30)

        return new_time

def shift_time_from_range(start_time, end_time):
    """
    Returns a list of ShiftTime's from given time range.
    These times are separated by at least 30 minutes, generally
    on the :00 and :30 minute marks
    :return: A List of ShiftTimes
    """
    # Assertions to protect typing
    assert type(start_time) is ShiftTime
    assert type(end_time) is ShiftTime

    cur_time = start_time
    times = []

    while cur_time.time.hour < end_time.time.hour:
        times.append(cur_time)
        cur_time = cur_time.increase()

    return times

if __name__ == "__main__":
    day1 = Day.tuesday
    day2 = Day.friday

    shift1 = ShiftTime(day1, 9, 45)
    shift2 = ShiftTime(day2, 18, 15)

    #print(str(shift1))
    #print(str(shift2))

    for shift_time in shift_time_from_range(shift1, shift2):
        print(str(shift_time)+"\n")