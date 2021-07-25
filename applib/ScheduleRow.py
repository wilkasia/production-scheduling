class ScheduleRow:
    months_mapping = {1: 'Styczeń', 2: 'Luty', 3: 'Marzec', 4: 'Kwiecień', 5: 'Maj', 6: 'Czerwiec',
                      7: 'Lipiec', 8: "Sierpień", 9: 'Wrzesień', 10: 'Październik', 11: 'Listopad',
                      12: 'Grudzień'}

    def __init__(self, date, tonnage, steel_type):
        self.date = date
        self.day = date.day
        self.month = self.months_mapping.get(date.month)
        self.year = date.year
        self.tonnage = tonnage
        self.steel_type = steel_type
