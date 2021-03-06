from ShiftScheduler import ShiftTime

# The approximated extra hours to be given to employees with seniority
SENIORITY_EXTRA_HOURS = 1

class AvailabilityMap():
    """
    A class to represent each employee's availability
    :var availability_times: a map linking ShiftTime -> Boolean to signify
    the availability of an employee at a given time
    """

    def __init__(self):
        self.availability_times = {}

    def __str__(self):
        # TODO Test
        available_times = "Available Times: \n"
        unavailable_times = "Unavailable Times: \n"
        for key in sorted(self.availability_times.keys(), key=lambda x: x.count()):
            if self.availability_times.get(key):
                available_times += str(key) + "\n"
            else:
                unavailable_times += str(key) + "\n"
        return available_times + unavailable_times


    def add_time(self, time, available):
        """
        Adds a time to the map of available times
        :param time: a ShiftTime
        :param available: boolean value representing if the employee
        is available at the given time
        :return: None
        """
        # TODO Test
        assert type(time) is ShiftTime.ShiftTime

        if available:
            self.availability_times.update({time: True})
        else:
            self.availability_times.update({time: False})

    def get_total_hours(self):
        """
        Determines the total hours the employee is available
        :return: a double representing the total hours an employee
        is available
        """
        # TODO Test
        hours = 0
        for key in self.availability_times.keys():
            if self.availability_times.get(key):
                hours += 0.5
        return hours

class Employee():
    """
    A Class to represent each employee in the schedule
    :var name: The name of the employee
    :var seniority: Boolean, True if employee has seniority, else False.
    Note: Seniority increases odds of getting preferred shifts
    :var available_times: an AvailabilityMap of all available and
    unavailable times
    :var preferred_times: an AvailabilityMap of all preferred times
    Note: True == time is preferred
    """

    def __init__(self, name, seniority):
        self.name = name
        self.seniority = seniority
        self.available_times = AvailabilityMap()
        self.preferred_times = AvailabilityMap()
        self.hours_assigned = 0

    def __str__(self):
        return self.name

    def get_total_available_hours(self):
        """
        :return: the total available hours for the employee
        """
        return self.available_times.get_total_hours()

    def get_total_assigned_hours(self):
        """
        :return: the total assigned hours for the employee
        """
        return self.hours_assigned

    def add_time(self, time, available):
        """
        Adds an time to the employee's schedule of available times
        :param time: A ShiftTime object
        :param available: boolean determining if the employee is
        available at the given time
        :return: None
        """
        # TODO Test
        if available:
            self.available_times.add_time(time=time, available=available)
        else:
            self.available_times.add_time(time=time, available=available)

    def add_preferred_time(self, time):
        """
        Adds a preferred time to the employee
        :param time: A ShiftTime object
        :return: true if the time was added, false if it was
        already in the preferred time map
        """
        # TODO Test
        return self.preferred_times.add_time(time, True)

    def get_available_times(self):
        """
        :return: A sorted list of shifts the employee can work
        """
        available_times = []
        for shift in sorted(self.available_times.availability_times.keys(),
                                key=lambda x: x.count()):
            if self.available_times.availability_times[shift]:
                available_times.append(shift)

        return available_times

    def get_preferred_times(self):
        """
        :return: A sorted list of shifts the employee prefers
        """
        # TODO Test
        preferred_times = []
        for shift in sorted(self.preferred_times.availability_times.keys(),
                                key=lambda x: x.count()):
            if self.preferred_times.availability_times[shift]:
                preferred_times.append(shift)

        return preferred_times

    def available_for_shift(self, shift):
        """
        :param shift: The shift in question
        :return: True if the employee is available for the
        queried shift, else false.
        """
        # TODO Test
        return self.available_times.availability_times[shift]

def same_employees(list1, list2):
    """
    Determines if two lists of employees are equal
    :param list1: a list of Employees
    :param list2: a list of Employees
    :return: True if the lists are equal, else False
    """
    # TODO Test
    for employee1 in list1:
        if not employee1 in list2:
            return False
    return True


if __name__ == "__main__":
    bobby = Employee("Bobby Smith", True)

    time1 = ShiftTime.ShiftTime(ShiftTime.Day.monday, 12, 30)
    time2 = ShiftTime.ShiftTime(ShiftTime.Day.saturday, 1, 00)

    bobby.add_time(time=time1, available=True)
    bobby.add_time(time=time2, available=False)

    print(str(bobby.available_times))
    print(bobby.available_times)