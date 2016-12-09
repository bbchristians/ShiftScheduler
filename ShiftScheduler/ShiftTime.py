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

    def is_weekday(self):
        """
        :return: True if the day is a weekday, else False
        """
        return self.value <= 5

# A dictionary matching string codes to the members of
# the 'Day' enum
DAY_DICTIONARY = {'m': Day.monday,
                  't': Day.tuesday,
                  'w': Day.wednesday,
                  'th': Day.thursday,
                  'f': Day.friday,
                  's': Day.saturday,
                  'sun': Day.sunday}


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

    def __eq__(self, other):
        # Assure the correct type
        assert type(other) is ShiftTime

        return self.day.value == other.day.value and \
               self.time.hour == other.time.hour and \
               self.time.minute == self.time.minute

    def __hash__(self):
        return self.count()


    def count(self):
        """
        :return: The count of the object (used to sort/compare them)
        """
        return (self.day.value * 10000) + \
               (self.time.hour * 100) + \
                self.time.minute

    def increase(self):
        """
        Increases the current time by 30 minutes
        :return: None
        """
        # TODO Test
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
    # TODO Tset
    # Assertions to protect typing
    assert type(start_time) is ShiftTime
    assert type(end_time) is ShiftTime

    cur_time = start_time
    times = []

    while cur_time.time.hour < end_time.time.hour:
        times.append(cur_time)
        cur_time = cur_time.increase()

    return times

def parse_range_from_record(record):
    """
    Parses a range in record format into a list
    of shifts
    :param record: String of form: "DAY START_H START_M END_H END_M"
    :return: TUPLE( A list of ShiftTimes, True if preferred time (else false))
    """

    record = record.split()

    # assure the record isn't missing any fields
    assert len(record) == 5 or len(record) == 6

    start_time = ShiftTime(DAY_DICTIONARY[record[0]], int(record[1]), int(record[2]))
    end_time = ShiftTime(DAY_DICTIONARY[record[0]], int(record[3]), int(record[4]))

    return shift_time_from_range(start_time, end_time), (len(record) == 6 and record[5] == "p")

if __name__ == "__main__":
    day1 = Day.tuesday
    day2 = Day.friday

    shift1 = ShiftTime(day1, 9, 45)
    shift2 = ShiftTime(day2, 18, 15)

    #print(str(shift1))
    #print(str(shift2))

    for shift_time in shift_time_from_range(shift1, shift2):
        print(str(shift_time)+"\n")