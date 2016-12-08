from ShiftScheduler import ShiftTime

class AvailabilityMap():
    """
    A class to represent each employee's availability
    :var availability_times: a map linking ShiftTime -> Boolean to signify
    the availability of an employee at a given time
    """
    availability_times = {}

    def __str__(self):
        # TODO Test
        available_times = "Available Times: \n"
        unavailable_times = "Unavailable Times: \n"
        for key in self.availability_times.keys():
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
    name = "Anonymous Employee"
    seniority = False;
    available_times = AvailabilityMap()
    preferred_times = AvailabilityMap()


    def __init__(self, name, seniority):
        self.name = name
        self.seniority = seniority

    def get_total_hours(self):
        """
        Returns the total available hours for the employee
        :return: the total available hours for the employee
        """
        return self.available_times.get_total_hours()

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
        return self.preferred_times.add_time(time)


if __name__ == "__main__":
    bobby = Employee("Bobby Smith", True)

    time1 = ShiftTime.ShiftTime(ShiftTime.Day.monday, 12, 30)
    time2 = ShiftTime.ShiftTime(ShiftTime.Day.saturday, 1, 00)

    bobby.add_time(time=time1, available=True)
    bobby.add_time(time=time2, available=False)

    print(str(bobby.available_times))
    print(bobby.available_times)