import sqlite3
from ShiftScheduler import Schedule, Employee, ShiftTime

# TODO ALL
# TODO learn how to use SQL/otherdb with python

LOCATION_RECORDS = "LocationRecords.csv"
EMPLOYEE_RECORDS = "ManyEmployeeRecords.csv"
#EMPLOYEE_RECORDS = "EmployeeRecords.csv"
#EMPLOYEE_RECORDS = "OneEmployeeRecord.csv"

def load_schedule_from_csv(file_name):
    """
    Imports a csv file containing all the locations' records
    :param file_name: The name of the CSV file
    :return: A list of employees
    """
    file = open(file_name)

    # Create new schedule with no locations (to be added later)
    schedule = Schedule.Schedule([])

    for line in file:
        line = line.split(',')

        # Add location to schedule
        location = line[0]
        schedule.add_location(location)

        # Add hours to the schedule for the location
        for i in range(1, len(line)):
            record = line[i].strip().split(' ')
            day = ShiftTime.DAY_DICTIONARY.get(record[0])
            start_time = ShiftTime.ShiftTime(day, int(record[1]), int(record[2]))
            end_time = ShiftTime.ShiftTime(day, int(record[3]), int(record[4]))

            schedule.add_hours(location, start_time, end_time)


    file.close()

    return schedule


def load_employees_from_csv(file_name, schedule):
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
        seniority = (line[1].strip() == "yes")
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

    # Load records from csv
    schedule = load_schedule_from_csv(LOCATION_RECORDS)
    employees = load_employees_from_csv(EMPLOYEE_RECORDS, schedule)

    # Schedule employees for shifts
    schedule.populate(employees)

    # Display schedule
    print(str(schedule))

    print("All hours filled: " + str(schedule.schedule.all_hours_filled()))

    print("\nEmployee Hours:")
    for employee in employees:
        print(employee.name + ": " + str(employee.hours_assigned))



if __name__ == "__main__":
    main()