#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import os, datetime
from applib.Rules import Rules
from applib.ScheduleRow import ScheduleRow
from applib.Schedule import Schedule


def main():
    print('CWD')
    print(os.getcwd() + "/data")
    data = os.getcwd() + "/data/"

    r = Rules(data + "prod-stal.csv")
    r.get_rules(data + "rules-stal.csv", data + "types-stal.csv")
    r.create_rules_dictionary()
    r.print_brands_list()

    schedule = Schedule()

    valid_sequence = ['S235JR', 'S235JR', 'B500B', '1006', 'XE400P', 'C4D1', 'C4D', 'B500B', '1018', '19MnB4']
    for i in range(10):
        row = ScheduleRow(datetime.date.today(), 141 + i, valid_sequence[i])
        schedule.add_row(row)

    invalid_sequence = ['1006', '16MnCr5', 'C4D1', 'C4D', 'B500SP', 'B500B', 'S235JR', 'C7D']
    for i in range(8):
        row = ScheduleRow(datetime.date.today() + datetime.timedelta(days=1), 142 + i, invalid_sequence[i])
        schedule.add_row(row)


    valid_daily_sequence = schedule.return_daily_sequence(datetime.date.today())
    invalid_daily_sequence = schedule.return_daily_sequence(datetime.date.today() + datetime.timedelta(days=1))

    print(r.validate_daily_sequence(valid_daily_sequence))
    print(r.validate_daily_sequence(invalid_daily_sequence))


if __name__ == '__main__':
    main()
