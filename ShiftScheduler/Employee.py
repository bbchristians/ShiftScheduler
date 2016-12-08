from ShiftScheduler import ShiftTime

class Employee():
    """
    A Class to represent each employee in the schedule
    """
    name = "John Doe"
    seniority = False;

    def __init__(self, name, seniority):
        self.name = name
        self.seniority = seniority


class AvailabilityMap():
    """
    A class to represent each employee's availability
    """
    availability_times = {}

    def add_time(self, time):
        """
        Adds a time to the map of available times
        :param time: a ShiftTime
        :return: true if the time was added, false if it was
        already in the map
        """
        # TODO
        assert type(time) is ShiftTime.ShiftTime

        self.availability_times.update()

