

class Schedule():
    """
    A class to represent the overall schedule of the workplace
    """
    schedule = None
    locations = []

    def __init__(self, locations ):
        self.locations = locations
        schedule = ScheduleMap(locations.size)


class ScheduleMap():
    """
    A class to represent a schedule that maps times to
    employees
    """
    total_locations = 1
    shifts = [{}]

    def __init__(self, total_locations):
        self.total_locations = total_locations

    def all_hours_filled(self):
        """
        Determines if all the hours in the schedule are filled
        :return: True if all hours in the schedule are filled,
        else false
        """
        # TODO
        return False

if __name__ == "__main__":
    pass



