class Schedule:

    def __init__(self):
        self.schedule = []

    def add_row(self, schedule_row):
        self.schedule.append(schedule_row)

    def return_daily_sequence(self, date):
        daily_sequence = []
        for row in self.schedule:
            if row.date == date:
                daily_sequence.append(row.steel_type)

        print(daily_sequence)
        return daily_sequence
