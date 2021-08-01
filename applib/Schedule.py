class Schedule:
    rules_dictionary = {}

    def __init__(self):
        self.schedule = []
        self.extra_types = []

    def add_row(self, schedule_row):
        self.schedule.append(schedule_row)

    def add_extra_type(self, extra_type):
        self.extra_types.append(extra_type)

    def return_daily_sequence(self, date):
        daily_sequence = []
        for row in self.schedule:
            if row.date == date:
                daily_sequence.append(row.steel_type)

        print(daily_sequence)
        return daily_sequence

    def set_rules_dictionary(self, rules_dictionary):
        self.rules_dictionary = rules_dictionary

    def find_new_rules(self, schedule_sequence):
        #invalid sequence
        #schedule_sequence = ['1006', '16MnCr5', 'C4D1', 'C4D', 'B500SP', 'B500B', 'S235JR', 'C7D']

        new_rules = []
        for index, steel_type in enumerate(schedule_sequence):
            if (index + 1) == len(schedule_sequence):
                break
            valid_next_types = self.rules_dictionary[steel_type]
            if schedule_sequence[index + 1] not in valid_next_types:
                new_rules.append([schedule_sequence[index], schedule_sequence[index + 1]])

        print("New rules: " + str(new_rules))
        return new_rules
