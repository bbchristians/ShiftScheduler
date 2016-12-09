from ShiftScheduler import Employee, ShiftTime

class Schedule():
    """
    A class to represent the overall schedule of the workplace
    :var schedule: A ScheduleMap of all shifts and who is on scheduled
    for them
    :var locations: A list of locations that the employees can work,
    (ex. 'Front desk', 'Kitchen', 'Room 210', etc.)
    """
    schedule = None
    locations = []

    def __init__(self, locations ):
        self.locations = locations
        self.schedule = ScheduleMap(locations)

    def __str__(self):
        ret = ""
        for location in self.locations:
            ret += location + ":\n"

            #Get all shifts at the location
            shifts = self.schedule.shifts.get(location).keys()

            # If there are no shifts at the location
            if not shifts:
                ret += "No Shifts\n"

            for shift in sorted(self.schedule.shifts.get(location),
                                key=lambda x: x.count()):
                ret += str(shift) + ": "

                # If there are no employees on the current shift
                if len(self.schedule.shifts.get(location).get(shift)) == 0:
                    ret += "Nobody"

                for employee in self.schedule.shifts.get(location).get(shift):
                    ret += str(employee) + ", "
                ret += "\n"

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
        self.locations.append(location)
        self.schedule.shifts.update({location: {}})

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
        # TODO return the correct value
        return True

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

    def all_hours_filled(self):
        """
        Determines if all the hours in the schedule are filled
        :return: True if all hours in the schedule are filled,
        else false
        """
        # TODO
        return False

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



