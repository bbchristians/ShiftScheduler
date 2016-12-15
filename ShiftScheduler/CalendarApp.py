from tkinter import *
from tkinter import font
from ShiftScheduler import ScheduleGenerator, ShiftTime

LOCATION_RECORDS = "LocationRecords.csv"
EMPLOYEE_RECORDS = "ManyEmployeeRecords.csv"
#EMPLOYEE_RECORDS = "EmployeeRecords.csv"
#EMPLOYEE_RECORDS = "OneEmployeeRecord.csv"

class Application:
    def __init__(self, master):
        TkDefaultFont = font.Font(family='Courier', size=10)
        self.schedule = ScheduleGenerator.load_schedule_from_csv(LOCATION_RECORDS)
        self.employees = ScheduleGenerator.load_employees_from_csv(EMPLOYEE_RECORDS, self.schedule)
        self.schedule.populate(self.employees)

        self.master = master
        master.title("Shift Scheduler")

        # Location sections
        self.schedule_labels = []
        for location in self.schedule.get_locations():
            schedule_label = Label(master, text=self.schedule.schedule_view(location), font=TkDefaultFont)
            self.schedule_labels.append(schedule_label)
            schedule_label.pack(pady=10)

        # Close Button (leaving in as example)
        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

if __name__ == '__main__':
    root = Tk()

    my_gui = Application(root)
    root.mainloop()