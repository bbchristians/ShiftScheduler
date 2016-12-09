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

    # Create a basic Schedule
    schedule = Schedule.Schedule(LOCATIONS)

    for day in ShiftTime.Day:
        if day.is_weekday():
            start = ShiftTime.ShiftTime(day,
                    WEEKDAY_HOURS_START, WEEKDAY_MINS_START)
            end   = ShiftTime.ShiftTime(day,
                    WEEKDAY_HOURS_END, WEEKDAY_MINS_END)
            schedule.add_hours(LOCATIONS[0], start, end)

    # Create some Employees
    ben  = Employee.Employee("Ben Christians", True)
    kevin = Employee.Employee("Kevin REDACTED", False)
    victoria = Employee.Employee("Victoria REDACTED", True)

    # Create some times
    time1 = ShiftTime.ShiftTime(ShiftTime.Day.monday, 9, 45)
    time2 = ShiftTime.ShiftTime(ShiftTime.Day.tuesday, 9, 45)
    time3 = ShiftTime.ShiftTime(ShiftTime.Day.monday, 10, 30)

    # Assign Employees Shifts
    schedule.assign(LOCATIONS[0], ben, time1)
    schedule.assign(LOCATIONS[0], kevin, time2)
    schedule.assign(LOCATIONS[0], victoria, time2)
    schedule.assign(LOCATIONS[0], ben, time3)
    schedule.assign(LOCATIONS[0], kevin, time3)
    schedule.assign(LOCATIONS[0], victoria, time3)

    print(str(schedule))


if __name__ == "__main__":
    main()