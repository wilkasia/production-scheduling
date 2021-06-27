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

# Klasa tworzaca reguly dla poprawnosci przyszlego planu na podstawie danych archiwalnych z pliku
class Rules:
    sec_list = []
    columns = 9
    col_day = 2
    col_brand = 8
    last_day = 0
    tmp = []
    rules = []
    types = {}

    def __init__(self, in_file):
        self.in_file = in_file

    def get_rules(self, out_file_1, out_file_2):
        print("Reding lines...")
        with open(self.in_file, newline='') as csvfile:
            c_reader = csv.reader(csvfile, delimiter=',')
            first_row = next(c_reader)
            tmp = []
            for row in c_reader:
                if len(row) == self.columns:
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
                        self.types[row[self.col_brand]] = {"day_first": 0, "day_last": 0, "rule_first": 0,
                                                           "rule_last": 0}

        for t in self.types.keys():
            self.rules.append([t, t])

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
                if add == 1:
                    self.rules.append([x[y], x[y + 1]])

        for t in self.types.keys():
            for r in self.rules:
                if r[0] != r[1]:
                    if r[0] == t:
                        self.types[t]["rule_first"] = 1
                    if r[1] == t:
                        self.types[t]["rule_last"] = 1

        file_1 = open(out_file_1, 'w+', newline='')
        with file_1:
            write = csv.writer(file_1)
            self.rules.sort()
            write.writerows(self.rules)

        t_types = []
        for t in self.types.keys():
            t_types.append([t, self.types[t]["day_first"], self.types[t]["day_last"], self.types[t]["rule_first"],
                            self.types[t]["rule_last"]])

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
            print(x+" : "+str(self.types[x]))

        print("-------------------------------------")
