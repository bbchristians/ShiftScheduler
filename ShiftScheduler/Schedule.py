from ShiftScheduler import Employee, ShiftTime
from random import shuffle

MAX_EMPLOYEES_PER_SHIFT = 1 # Max imployees per shift
PREFERRED_STRING_SHIFTS = 4 # Preferred number of shifts to assign to one employee
SCHEDULE_VIEW_COL_WIDTH = 15



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

    def schedule_view(self, location):
        """
        A different to_string function
        :param location: the location to get the schedule of
        :return: A schedule formatted string of the schedule
        at the given location
        """
        assert location in self.get_locations()

        shifts = self.schedule.get_sorted_shifts_from_location(location)
        schedule_str = location + "\n" + " "*SCHEDULE_VIEW_COL_WIDTH + "|"
        all_times = self.all_times()
        shift_times = set()

        # Dress the top row to have the names of the days
        for day in ShiftTime.Day:
            schedule_str += set_string_width(str(day), SCHEDULE_VIEW_COL_WIDTH) + "|"

        schedule_str += "\n"

        # Get a set of all times on the schedule (to be used later)
        for shift in all_times.schedule.get_sorted_shifts_from_location("ALL"):
            if shift in shifts:
                shift_times.update({shift.time})

        # Add each employee listed for each shift
        for time in sorted(shift_times, key=lambda x:x):
            schedule_str += set_string_width(str(time), SCHEDULE_VIEW_COL_WIDTH) + "|"
            for day in ShiftTime.Day:
                this_shift = ShiftTime.ShiftTime(day, time.hour, time.minute)
                if this_shift in shifts:
                    employees = self.schedule.shifts.get(location).get(this_shift)
                    if len(employees) == 0:
                        schedule_str += set_string_width("NOBODY", SCHEDULE_VIEW_COL_WIDTH) + "|"
                    else:
                        schedule_str += set_string_width(str(employees[0]), SCHEDULE_VIEW_COL_WIDTH) + "|"
            schedule_str += "\n"



            # because we just want the time for each shift, ignore the day
            # if shift.day == ShiftTime.Day.monday and:
            #     schedule_str += set_string_width(str(shift.time), SCHEDULE_VIEW_COL_WIDTH) + "|"


        return schedule_str

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
        # TODO Fix problem with generating shifts that are too small
        #  ^This typically happens when there is a location with say 6.5 hours per day of work
        # TODO Generate more than one schedule (do in another function)

        for location in self.schedule.shifts.keys():
            # Assign employees to their preferred times
            # Preferred times start with seniority
            employees = sorted(employees, key=lambda x: 0 if x.seniority else 1)
            for employee in employees:
                for shift in employee.get_preferred_times():
                    # attempt to schedule them for their preferred shift
                    self.attempt_to_assign_shift(location, employee, shift)

        for location in self.schedule.shifts.keys():

            # Assign employees to the rest of the times
            for shift in self.schedule.get_sorted_shifts_from_location(location):

                # Dont schedule employees to shifts that have >= the maximum number
                # of employees already schedules for it
                if not self.can_assign(location, shift):
                    continue

                # Sort in order of hours assigned (least to greatest) also
                # factoring in seniority
                employees = sorted(employees, key=lambda x: \
                    x.hours_assigned - (Employee.SENIORITY_EXTRA_HOURS if x.seniority else 0))

                for employee in employees:
                    self.attempt_to_assign_shift(location, employee, shift)
                    # # Old code to assign a single shift at a time
                    # if employee.available_for_shift(shift) and \
                    #         not employee.get_total_assigned_hours() >= self.get_max_hours():
                    #     self.assign(location, employee, shift)
                    #     break

    def attempt_to_assign_shift(self, location, employee, shift):
        """
        Attempts to assign the employee to a shift at the location
        This will assign multiple shifts based off of Schedule.PREFFERED_STRING_SHIFTS
        :param location: the location to assign the employee to
        :param employee: the employee to assign to a shift
        :param shift: the shift to assign the employee to
        :return: True if the employee was assigned to all shifts else False
        """
        # Find the shifts after the current shift
        potential_shifts = self.get_next_shifts(location, shift, PREFERRED_STRING_SHIFTS)

        # Don't overbooking employees
        if employee.get_total_assigned_hours() + .5 * len(potential_shifts) > self.get_max_hours():
            return False

        # First remove any shifts that arent on the day of the original shift
        # Don't schedule employees for shifts that they aren't available for
        for p_shift in potential_shifts:
            if p_shift.get_day() != shift.day:
                potential_shifts.remove(p_shift)
            elif not employee.available_for_shift(p_shift):
                return False

        # Assign shifts
        for p_shift in potential_shifts:
            if self.can_assign(location, p_shift):
                self.assign(location, employee, p_shift)
            else:
                # break to avoid gaps in shifts for odd reasons
                return False
        # return True because employee was assigned to all shifts
        return True

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

    def get_max_hours(self):
        """
        :return: double representing the maximum hours an employee can work
        """
        # TODO actual calculation
        # TODO Test
        return 7

    def get_next_shifts(self, location, shift, n_shifts):
        """
        :param location: the location of the shifts
        :param shift: the shift to get the shifts after
        :param n_shifts: how many shifts to get
        :return: A sorted list of shifts starting with the given shift,
        and ending with the shift (n_shifts-1) shifts in the future.
        ex. get_next_shifts( "location", m9:30, 3) -> [m9:30, m10:00, m10:30]
        Note: if there are not enough shifts before the end of the day,
        then the list will only consist of the shifts that were before the end of the day
        """
        next_shifts = []

        # return on bad input
        if n_shifts < 1 or location not in self.schedule.shifts.keys():
            return next_shifts

        for iter_shift in self.schedule.get_sorted_shifts_from_location(location):
            # if it (has) found the queried shift
            if iter_shift == shift or len(next_shifts) > 0:
                next_shifts.append(iter_shift)
                n_shifts -= 1

                # if it has found all the required shifts
                if n_shifts <= 0:
                    break

        return next_shifts

    def get_locations(self):
        """
        :return: A sorted list of locations on the schedule
        """
        return sorted(self.schedule.shifts.keys(), key=lambda x: x)

    @staticmethod
    def all_times():
        """
        :return: a schedule filled with all times
        """
        schedule = Schedule(["ALL"])
        for day in ShiftTime.Day:
            start_time = ShiftTime.ShiftTime(day, 00, 00)
            end_time = ShiftTime.ShiftTime(day, 23, 30)
            schedule.add_hours("ALL", start_time, end_time)

        return schedule

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

    def get_sorted_shifts_from_location(self, location):
        """
        :param location: the location to find shifts from
        :return: A sorted list of shifts
        """
        return sorted(self.shifts[location].keys(), key=lambda x: x.count())

def set_string_width(string, width):
    """
    Fixes the string length to the given width
    :param string: A String
    :param width: A width (int)
    :return: a fixed string. This either cuts off the lsat characters to
    make the length = 'width', or adds spaces evenly to either side
    """
    if len(string) >= width:
        return string[:width]
    else:
        num_spaces = width - len(string)
        left = False
        for space in range(0, num_spaces):
            if left:
                string = " " + string
            else:
                string += " "
            left = not left

    return string

if __name__ == "__main__":
    # ben = Employee.Employee("Ben Christians", True)
    # locations = ['GPC', 'GFH']
    #
    # time1 = ShiftTime.ShiftTime(ShiftTime.Day.tuesday, 9, 45)
    # time2 = ShiftTime.ShiftTime(ShiftTime.Day.tuesday, 18, 15)
    #
    # schedule = Schedule(locations=locations)
    #
    # schedule.add_hours('GPC', time1, time2)
    #
    # print(str(ben))
    # print(str(schedule))

    print(set_string_width("a", 10))
    print("----------")



