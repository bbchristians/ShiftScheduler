import sqlite3
from ShiftScheduler import Schedule, Employee, ShiftTime

# TODO ALL
# TODO learn how to use SQL/otherdb with python and replace globals
LOCATIONS = ["GPC", "GFH"]
WEEKDAY_HOURS_START = 10
WEEKDAY_MINS_START = 00
WEEKDAY_HOURS_END = 18
WEEKDAY_MINS_END = 00

EMPLOYEE_RECORDS = "EmployeeRecords.csv"

def load_from_csv(file_name, schedule):
    """
    Imports a csv file containing all the employees' records
    Note: Employees' schedules will be completed after the import
    :param file_name: The name of the CSV file
    :param schedule: The schedule holding all operating hours for
    each location
    :return: A list of employees
    """
    file = open(file_name)

    employees = []
    for line in file:
        line = line.split(',')

        # Generate Employee
        name = line[0]
        seniority = line[1] == "Yes"
        employee = Employee.Employee(name, seniority)

        # Fill all the hours of the employee to be available (default)
        for location in schedule.locations:
            for shift in schedule.schedule.shifts[location].keys():
                employee.add_time(shift, True)

        # Fill the hours of un-availability for the Employee
        for i in range(2, len(line)):
            parsed_shifts, preferred = ShiftTime.parse_range_from_record(line[i])

            # For all shifts in the parsed record, set the employee
            # to unavailable at that time
            for shift in parsed_shifts:
                if preferred:
                    employee.add_preferred_time(shift)
                else:
                    employee.add_time(shift, False)


        employees.append(employee)

    file.close()

    return employees


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

    # Load records from csv
    employees = load_from_csv(EMPLOYEE_RECORDS, schedule)

    for employee in employees:
        print(str(employee) + " : " + str(employee.get_total_hours()) + " hours.")

    # Book at most one employee to each shift
    schedule.populate(employees)

    print(str(schedule))

    print(schedule.schedule.all_hours_filled())



if __name__ == "__main__":
    main()