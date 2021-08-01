#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import csv


# class BaseData:
#     columns = 9
#     list_brand = []
#
#     def __init__(self, path):
#         self.path = path
#
#     def get_data(self):
#         with open(self.path, newline='') as csv_file:
#             c_reader = csv.reader(csvfile, delimiter=',')
#             first_row = next(c_reader)
#             for row in c_reader:
#                 if len(row) == self.columns:

# Klasa tworzaca reguly dla poprawnosci przyszlego planu na podstawie danych archiwalnych z pliku: prod-stal.csv
#
# Format i znaczenie wygenerowantch regul:
# 1. Reguly okreslajace mozliwe nastepstwa typow stali: out_file_1. Kazdy wiersz reprezentuje 1 mozliwosc
#    TYP,TYP
# 2. Dodatkowe reguly dodtyczace danego gatunku stali out_file_2
#    TYP,[0|1],[0|1],[0|1],[0|1]
#
#    TYP - TYP Stali,
#    [0|1] - Mozliwosc wystapienia w jednym dniu jako pierszy,
#    [0|1] - Mozliwosc wystapienia w jednym dniu jako ostatni,
#    [0|1] - Istnieje regula nastepstwa gdzie wystepuje jako pierwszy,
#    [0|1] - Istnieje regula nastepstwa gdzie wystepuje jako ostatni
#
class Rules:
    sec_list = []
    columns = 9
    col_day = 2
    col_brand = 8
    last_day = 0
    tmp = []
    rules = []
    types = {}
    rules_dictionary = {}

    def __init__(self, in_file):
        self.in_file = in_file

    def get_rules(self, out_file_1, out_file_2):
        print("Reading lines...")
        types_frequency = {}

        # Create dictionary of types - keys = type names
        # Create sequences as list two (sec_list) of two elements list [[name, name], [name, name], ...]
        #    Sequences are in scope of single day
        # self.types
        with open(self.in_file, newline='') as csvfile:
            c_reader = csv.reader(csvfile, delimiter=',')
            first_row = next(c_reader)
            tmp = []
            type_id = 1
            for row in c_reader:
                if len(row) == self.columns:

                    if row[self.col_brand] in types_frequency.keys():
                        types_frequency[row[self.col_brand]] += 1
                    else:
                        types_frequency[row[self.col_brand]] = 1

                    day = int(row[self.col_day])
                    if day != self.last_day:
                        tmp = []
                        self.sec_list.append(tmp)

                    if len(tmp) == 0:
                        tmp.append(row[self.col_brand])
                    else:
                        if tmp[-1] != row[self.col_brand]:
                            tmp.append(row[self.col_brand])

                    self.last_day = day

                    if not row[self.col_brand] in self.types:
                        self.types[row[self.col_brand]] = {"id": type_id, "day_first": 0, "day_last": 0,
                                                           "rule_first": 0, "rule_last": 0}
                        type_id += 1

        # Create rules for the same types. This means that the same type may be continue in the next step
        for t in self.types.keys():
            self.rules.append([t, t, 0])

        for x in self.sec_list:

            for t in self.types.keys():
                if x[0] == t:
                    self.types[t]["day_first"] = 1
                if x[-1] == t:
                    self.types[t]["day_last"] = 1

            # if len(x) == 1:
            #     add = 1
            #     for c in self.rules:
            #         if c[0] == x[0] and c[1] == x[0]:
            #             add = 0
            #     if add == 1:
            #         self.rules.append([x[0], x[0]])
            for y in range(len(x) - 1):
                add = 1
                for c in self.rules:
                    if c[0] == x[y] and c[1] == x[y + 1]:
                        add = 0
                        c[2] += 1
                if add == 1:
                    self.rules.append([x[y], x[y + 1], 1])

        for t in self.types.keys():
            for r in self.rules:
                if r[0] != r[1]:
                    if r[0] == t:
                        self.types[t]["rule_first"] = 1
                    if r[1] == t:
                        self.types[t]["rule_last"] = 1

        for r in self.rules:
            r.append(self.types[r[0]]["id"])
            r.append(self.types[r[1]]["id"])

        file_1 = open(out_file_1, 'w+', newline='')
        with file_1:
            write = csv.writer(file_1)
            # self.rules.sort()
            write.writerows(self.rules)

        t_types = []
        for t in self.types.keys():
            t_types.append([t, self.types[t]["id"], self.types[t]["day_first"], self.types[t]["day_last"], self.types[t]["rule_first"],
                            self.types[t]["rule_last"], types_frequency.get(t)])

        print(types_frequency)
        file_2 = open(out_file_2, 'w+', newline='')
        with file_2:
            write = csv.writer(file_2)
            t_types.sort()
            write.writerows(t_types)

        # print(len(row))
        # print(type(row[0]))
        # print(row[0])

    def print_brands_list(self):
        for x in self.sec_list:
            print(x)

        for x in self.rules:
            print(x)

        for x in self.types.keys():
            print(x + " : " + str(self.types[x]))

        print("-------------------------------------")

    def create_rules_dictionary(self):
        for x in self.rules:
            if x[0] in self.rules_dictionary:
                self.rules_dictionary[x[0]].append(x[1])
            else:
                self.rules_dictionary[x[0]] = [x[1]]

    def validate_daily_sequence(self, daily_sequence):
        for index, type in enumerate(daily_sequence):
            valid_next_types = self.rules_dictionary[type]

            if index == 0:
                if self.types[type]["day_first"] == 0:
                    print("Daily sequence not valid")
                    return False

            if (index + 1) == len(daily_sequence):
                if self.types[type]["day_last"] == 0:
                    print("Daily sequence not valid")
                    return False
                break

            if daily_sequence[index + 1] not in valid_next_types:
                print("Daily sequence not valid")
                return False

        return True


def get_types_numbers_mapping(file):
    # Słownik z mapowaniem numer na gatunek
    types_numbers_mapping = {}

    with open(file, newline='') as csv_file:
        c_reader = csv.reader(csv_file, delimiter=',')
        for row in c_reader:
            types_numbers_mapping[row[1]] = row[0]

    return types_numbers_mapping

