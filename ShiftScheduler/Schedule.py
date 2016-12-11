from ShiftScheduler import Employee, ShiftTime
from random import shuffle

MAX_EMPLOYEES_PER_SHIFT = 1

class Schedule():
    """
    A class to represent the overall schedule of the workplace
    :var schedule: A ScheduleMap of all shifts and who is on scheduled
    for them
    :var locations: A list of locations that the employees can work,
    (ex. 'Front desk', 'Kitchen', 'Room 210', etc.)
    """

    def __init__(self, locations ):
        self.locations = locations
        self.schedule = ScheduleMap(locations)

    def __str__(self):
        """
        :return: A string representing the schedule in the form of:
        LOCATION:
        From DAY at START_TIME to DAY at END_TIME: EMPLOYEE, EMPLOYEE, ...
        ...
        ...
        LOCATION:
        ...
        """
        ret = ""
        for location in self.locations:
            ret += location + ":\n"

            # Get all shifts at the location
            shifts = self.schedule.shifts.get(location).keys()

            # If there are no shifts at the location
            if not shifts:
                ret += "No Shifts\n"
                continue

            final_shift = self.last_shift(location)
            start_of_shift = None # the start of the shift
            shift_employees = None # the employee(s) of the current shift
            last_shift = None # last_shift needs to be recorded to reference when overlapping days

            for shift in sorted(self.schedule.shifts.get(location),
                                key=lambda x: x.count()):
                cur_employees = self.schedule.shifts.get(location).get(shift)

                if start_of_shift is None:
                    start_of_shift = shift
                    shift_employees = cur_employees

                # If this is the last shift of the week
                elif shift == final_shift:
                    if len(shift_employees) == 0:
                        ret += "From " + str(start_of_shift) + " to " + str(shift.increase()) + ": Nobody\n"
                    else:
                        employee_string = ""
                        for employee_each in shift_employees:
                            employee_string += str(employee_each) + ","
                        ret += "From " + str(start_of_shift) + " to " + str(shift.increase()) + ": " + employee_string + "\n"

                # If there is any change of employees between shifts
                # or shift of same employees overlaps to a non-continuous shift
                elif not Employee.same_employees(shift_employees, cur_employees) or \
                        (last_shift is not None and shift != last_shift.increase()):
                    # Display properly that nobody is on this shift
                    if len(shift_employees) == 0:
                        ret += "From " + str(start_of_shift) + " to " + str(last_shift.increase()) + ": Nobody\n"
                    else:
                        employee_string = ""
                        for employee_each in shift_employees:
                            employee_string += str(employee_each) + ","
                        ret += "From " + str(start_of_shift) + " to " + \
                               str(last_shift.increase()) + ": " + employee_string + "\n"

                    # Save current values for use on the next shift
                    start_of_shift = shift
                    shift_employees = cur_employees

                last_shift = shift
        return ret

    def add_hours(self, location, start_time, end_time):
        """
        Adds working hours to the current location in the schedule
        Note: Adding time to the schedule that already has employees
        assigned to it will remove those assignments
        :param location: The location to add the hours (String)
        :param start_time: The starting time of the shifts to add
        :param end_time: The ending time of the shifts to add
        :return: None
        """
        # TODO Test
        # Assure that the given location is valid
        assert location in self.locations
        # Get the list of times from the given range
        times = ShiftTime.shift_time_from_range(start_time, end_time)
        # Add all shifts to the schedule
        for shift in times:
            self.schedule.shifts.get(location).update({shift:[]})

    def add_location(self, location):
        """
        Adds a location to the schedule
        :param location: The name of the location (String)
        :return: None
        """
        # TODO Test
        # TODO Update all employees' availability at the hours of the new place
        self.locations.append(location)
        self.schedule.shifts.update({location: {}})

    def can_assign(self, location, shift):
        """
        Determines if an employee can be assigned at the current shift
        :param location: the location to query
        :param shift: the shift to query
        :return: True if they can be assigned, else False
        Note: This does not take into account if the employee is available
        at the time of the given shift
        """

        if shift not in self.schedule.shifts[location].keys():
            return False

        schedule = self.schedule.shifts.get(location).get(shift)
        length = len(schedule)

        return length < MAX_EMPLOYEES_PER_SHIFT

        #return len(self.schedule.shifts[location][shift]) < MAX_EMPLOYEES_PER_SHIFT

    def assign(self, location, employee, shift):
        """
        Assigns an employee to a given shift
        Note: Multiple employees can be assigned to one shift
        :param location: The location to assign the shift at
        :param employee: The employee to assign to the shift
        :param shift: The shift to assign the employee to
        :return: True if the employee was scheduled to the shift,
        False if they weren't
        """
        # TODO Check if employee is available at the given time
        self.schedule.shifts.get(location).get(shift).append(employee)
        employee.hours_assigned += 0.5
        employee.available_times.availability_times.update({shift: False})

        return employee in self.schedule.shifts.get(location).get(shift)

    def populate(self, employees):
        """
        Fills a schedule with at most one employee per shift
        :param employees: A list of employees
        :return: None
        """
        # TODO Change return value?
        # TODO Test
        for location in self.schedule.shifts.keys():

            # Assign employees to their preferred times
            # Preffered times start with seniority
            employees = sorted(employees, key=lambda x: 0 if x.seniority else 1)
            for employee in employees:
                for shift in employee.preferred_times.availability_times:

                    if self.can_assign(location, shift):
                        self.assign(location, employee, shift)

            # Assign employees to the rest of the times
            for shift in sorted(self.schedule.shifts[location].keys(), key=lambda x: x.count()):

                # Dont schedule employees to shifts that have >= the maximum number
                # of employees already schedules for it
                if not self.can_assign(location, shift):
                    continue

                # Sort in order of hours assigned (least to greatest) also
                # factoring in seniority
                employees = sorted(employees, key=lambda x: \
                    x.hours_assigned - (Employee.SENIORITY_EXTRA_HOURS if x.seniority else 0))

                for employee in employees:
                    if employee.available_for_shift(shift):
                        self.assign(location, employee, shift)
                        break

    def last_shift(self, location):
        """
        :param location: The location to get the last shift of
        :return: The last shift of the location (Sunday is counted
        as the last day of the week) or None if there are no shifts at the location
        """
        shifts = self.schedule.shifts[location]

        # Sort the shifts in descending order
        shifts = sorted(shifts, key=lambda x: -1*x.count())

        if len(shifts) == 0:
            return None

        return shifts[0]

class ScheduleMap():
    """
    A class to represent a schedule that maps times to
    employees
    :var shifts: A Dictionary mapping locations to Dictionaries that map ShiftTimes to
    a list of Employees {Location -> {ShiftTime -> [Employee]}}
    """
    shifts = {}

    def __init__(self, locations):
        for location in locations:
            self.shifts.update({location: {}})

    def all_hours_filled(self, location=None):
        """
        Determines if all the hours in the schedule are filled
        :param location: a location to determine the fullness of shifts.
        If left as None, then query the fullness of all locations
        :return: True if all hours in the schedule are filled,
        else false
        """
        # TODO Test
        if location is None:
            for location in self.shifts.keys():
                for shift in self.shifts[location]:
                    if len(self.shifts[location][shift]) == 0:
                        return False
        else:
            for shift in self.shifts[location]:
                if len(self.shifts[location][shift]) == 0:
                    return False
        # Return true if no all shifts of location(s) queried
        # are mapped to a non-None object
        return True

    def get_total_locations(self):
        """
        :return: The total number of locations in the schedule
        """
        return self.shifts.keys.size

if __name__ == "__main__":
    ben = Employee.Employee("Ben Christians", True)
    locations = ['GPC', 'GFH']

    time1 = ShiftTime.ShiftTime(ShiftTime.Day.tuesday, 9, 45)
    time2 = ShiftTime.ShiftTime(ShiftTime.Day.tuesday, 18, 15)

    schedule = Schedule(locations=locations)

    schedule.add_hours('GPC', time1, time2)

    print(str(ben))
    print(str(schedule))



