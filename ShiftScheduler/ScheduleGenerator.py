import sqlite3
from ShiftScheduler import Schedule, Employee, ShiftTime

# TODO ALL
# TODO learn how to use SQL/otherdb with python and replace globals
LOCATIONS = ["GPC", "GFH"]
WEEKDAY_HOURS_START = 9
WEEKDAY_MINS_START = 45
WEEKDAY_HOURS_END = 18
WEEKDAY_MINS_END = 15

def main():
    schedule = Schedule.Schedule(LOCATIONS)

    for day in ShiftTime.Day:
        if day.is_weekday():
            start = ShiftTime.ShiftTime(day,
                    WEEKDAY_HOURS_START, WEEKDAY_MINS_START)
            end   = ShiftTime.ShiftTime(day,
                    WEEKDAY_HOURS_END, WEEKDAY_MINS_END)
            schedule.add_hours(LOCATIONS[0], start, end)

    print(str(schedule))


if __name__ == "__main__":
    main()