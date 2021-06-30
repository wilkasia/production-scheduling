#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import sklearn
import csv
import os
import pandas as pd
from datetime import date
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from joblib import dump, load


class Plan:
    columns = 9
    df = []
    days = []
    types = {}

    def load_from_csv(self, csv_file):
        with open(csv_file, newline='') as cvf:
            cr = csv.reader(cvf, delimiter=',')
            next(cr)
            for row in cr:
                if len(row) == self.columns:
                    self.df.append(row)

    def print_plan(self):
        for row in self.df:
            print(row)

    def train_data(self):

        features = [[1, 1200], [2, 120], [3, 1200]]

        labels = [1, 2, 3]

        # encoded_features = le.fit_transform(features)
        # encoded_labels = le.fit_transform(labels)

        model = KNeighborsClassifier(n_neighbors=3)
        model.fit(features, labels)

        print(model.predict(features))

        dump(model, 'myfile.joblib')

        # self.df = pd.read_csv(csv_file)
        # ls = self.df.to_list()
        # for x in ls:
        #     print(x)
