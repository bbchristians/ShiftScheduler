from ShiftScheduler import ShiftTime

class AvailabilityMap():
    """
    A class to represent each employee's availability
    """
    availability_times = {}

    def __str__(self):
        # TODO
        return "asd"

    def add_time(self, time):
        """
        Adds a time to the map of available times
        :param time: a ShiftTime
        :return: true if the time was added, false if it was
        already in the map
        """
        # TODO Test
        assert type(time) is ShiftTime.ShiftTime

        # If the employee is already available at time return false
        # to signify no changes made
        if self.availability_times.get(time):
            return False

        self.availability_times.update({time: True})
        return True

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
    """
    name = "Anonymous Employee"
    seniority = False;
    available_times = AvailabilityMap()
    preffered_times = AvailabilityMap()


    def __init__(self, name, seniority):
        self.name = name
        self.seniority = seniority

if __name__ == "__main__":
    bobby = Employee("Bobby Smith", True)

    print(str(bobby.available_times))