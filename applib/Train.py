#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import os
import csv

import numpy as np
import pandas as pd
from applib.Rules import Rules
from sklearn.neighbors import KNeighborsClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from joblib import dump, load


class Train:
    hd = []
    s_types = {}
    columns = 9
    data_folder_name = "/data/"
    rules_csv_file = "rules.csv"
    types_csv_file = "types.csv"

    i_brand = 8
    i_weight = 6

    def gen_plan(self, types):
        print('gen_plan')

    def first_model_train(self, hd_csv_file):
        data_path = os.getcwd() + self.data_folder_name
        rules = Rules(data_path + hd_csv_file)
        rules.get_rules(data_path + self.rules_csv_file, data_path + self.types_csv_file)

        # df = pd.read_csv(data_path + hd_csv_file)
        # print(df)
        #
        # dd = df.groupby(["Rok", "Miesiąc", "Dzień", "Gatunek"]).agg({"Tonaż": np.sum})

        # print(dd)

        with open(data_path + hd_csv_file, newline='') as cvf:
            cr = csv.reader(cvf, delimiter=',')
            next(cr)
            for row in cr:
                if len(row) == self.columns:
                    self.hd.append(row)

        # zamiana nazw typow stali na dict klucz=nazwa, watrosc=liczba
        idx = 1
        with open(data_path + self.types_csv_file, newline='') as cvf:
            cr = csv.reader(cvf, delimiter=',')
            for row in cr:
                self.s_types[row[0]] = idx
                idx += 1

        print(self.s_types)

        step = 0
        day = 0
        stt = 0
        sts = 0
        part = []
        parts = []
        for d in self.hd:
            if int(d[2]) != day:
                day = int(d[2])
                parts.append(part)
                part = []
            else:
                part.append(d)

        features = []
        labels = []
        for p in parts:
            tt = {}
            label = []
            for d in p:
                if self.s_types.get(d[self.i_brand]) in tt:
                    tt[self.s_types.get(d[self.i_brand])] += float(d[self.i_weight])
                else:
                    tt[self.s_types.get(d[self.i_brand])] = float("0")

                tt[self.s_types.get(d[self.i_brand])] = int(tt[self.s_types.get(d[self.i_brand])])
                if not self.s_types.get(d[self.i_brand]) in label:
                    label.append(self.s_types.get(d[self.i_brand]))

            features.append(tt)
            labels.append(label)

        model = KNeighborsClassifier(n_neighbors=20)

        fff = [
            [1, 2, 3, 4],
            [2, 1, 3, 4],
            [3, 1, 2, 4],
            [1, 3, 2, 4],
            [2, 3, 1, 4],
            [3, 2, 1, 4],
            [3, 2, 4, 1],
            [2, 3, 4, 1],
            [4, 3, 2, 1],
            [3, 4, 2, 1],
            [2, 4, 3, 1],
            [4, 2, 3, 1],
            [4, 1, 3, 2],
            [1, 4, 3, 2],
            [3, 4, 1, 2],
            [4, 3, 1, 2],
            [1, 3, 4, 2],
            [3, 1, 4, 2],
            [2, 1, 4, 3],
            [1, 2, 4, 3],
            [4, 2, 1, 3],
            [2, 4, 1, 3],
            [1, 4, 2, 3],
            [4, 1, 2, 3]
        ]
        lll = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        clf = OneVsRestClassifier(SVC()).fit(fff, lll)
        model.fit(fff, lll)

        print(model.predict([[self.s_types.get('S355J2'), 1001]]))
        print(clf.predict([[self.s_types.get('S355J2'), 1001]]))

        # for i, v in enumerate(features):
        #     feature_dict = features[i]
        #     feature = []
        #     for key in feature_dict:
        #         feature.append([key, feature_dict[key]])
        #
        #     label = labels[i]
        #
        #     if len(feature) > 0 and len(label) > 0:
        #         print(i)
        #         print(feature)
        #         print(label)
        #         model.fit(feature, label)
        #
        # print("-----------------------------------------------------------------------------")
        # print(model.predict([[43, 297], [85, 1477], [45, 0], [63, 1064], [68, 153], [62, 148]]))
        # print(model.predict([[85, 1477], [45, 0], [63, 1064], [68, 153], [62, 148], [43, 297]]))
        # print(model.predict([[45, 0], [63, 1064], [68, 153], [62, 148], [43, 297], [85, 1477]]))
        # print(model.predict([[43, 297]]))
        # print(model.predict([[68, 153], [62, 148]]))

        # if stt != self.s_types.get(d[8]):
        #     features.append([stt, sts])
        #     stt = self.s_types.get(d[8])
        #     sts = d[6]
        # else:
        #     sts += d[6]
