#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import os, datetime
from applib.Rules import Rules
from applib.ScheduleRow import ScheduleRow
from applib.Schedule import Schedule
# from applib.Plan import Plan
# from applib.Train import Train
from applib.Test import Test
# import matplotlib.pyplot as plt
# from matplotlib import cm
# from matplotlib.ticker import LinearLocator
# import numpy as np
from flaskr.app import get_types


def main():
    print('CWD')
    print(os.getcwd() + "/data")
    data = os.getcwd() + "/data/"

    r = Rules(data + "prod-stal.csv")
    r.get_rules(data + "rules-stal.csv", data + "types-stal.csv")
    r.create_rules_dictionary()
    r.print_brands_list()

    # p = Plan()
    # p.load_from_csv(data + "prod-stal.csv")
    # p.print_plan()
    # p.train_data()

    # t = Train()
    # t.first_model_train("prod-stal.csv")

    t = Test()

    order = [
        {'id': '100', 'tonnage': '900', 'name': 'S-100'},
        {'id': '102', 'tonnage': '700', 'name': 'S-102'},
        {'id': '88', 'tonnage': '500', 'name': 'S-88'},
        {'id': '33', 'tonnage': '400', 'name': 'S-33'},
        {'id': '12', 'tonnage': '400', 'name': 'S-12'},
        {'id': '11', 'tonnage': '400', 'name': 'S-11'},
        {'id': '99', 'tonnage': '900', 'name': 'S-99'},
        {'id': '10', 'tonnage': '700', 'name': 'S-10'},
        {'id': '89', 'tonnage': '500', 'name': 'S-89'},
        {'id': '3', 'tonnage': '400', 'name': 'S-3'},
        {'id': '91', 'tonnage': '400', 'name': 'S-91'},
        {'id': '90', 'tonnage': '400', 'name': 'S-90'},
        # {'id': '20', 'tonnage': '400', 'name': 'S-20'}
    ]

    types_numbers = get_types(data + "types-stal.csv")
    t.test_1(data + "rules-stal.csv", types_numbers, order)



    # fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    #
    # # Make data.
    # X = np.arange(-5, 5, 0.25)
    # Y = np.arange(-5, 5, 0.25)
    # X, Y = np.meshgrid(X, Y)
    # R = np.sqrt(X ** 2 + Y ** 2)
    # Z = np.sin(R)
    #
    # # Plot the surface.
    # surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
    #                        linewidth=0, antialiased=False)
    #
    # # Customize the z axis.
    # ax.set_zlim(-1.01, 1.01)
    # ax.zaxis.set_major_locator(LinearLocator(10))
    # # A StrMethodFormatter is used automatically
    # ax.zaxis.set_major_formatter('{x:.02f}')
    #
    # # Add a color bar which maps values to colors.
    # fig.colorbar(surf, shrink=0.5, aspect=5)
    #
    # plt.show()


    # schedule = Schedule()
    #
    # valid_sequence = ['S235JR', 'S235JR', 'B500B', '1006', 'XE400P', 'C4D1', 'C4D', 'B500B', '1018', '19MnB4']
    # for i in range(10):
    #     row = ScheduleRow(datetime.date.today(), 141 + i, valid_sequence[i])
    #     schedule.add_row(row)
    #
    # invalid_sequence = ['1006', '16MnCr5', 'C4D1', 'C4D', 'B500SP', 'B500B', 'S235JR', 'C7D']
    # for i in range(8):
    #     row = ScheduleRow(datetime.date.today() + datetime.timedelta(days=1), 142 + i, invalid_sequence[i])
    #     schedule.add_row(row)
    #
    #
    # valid_daily_sequence = schedule.return_daily_sequence(datetime.date.today())
    # invalid_daily_sequence = schedule.return_daily_sequence(datetime.date.today() + datetime.timedelta(days=1))
    #
    # print(r.validate_daily_sequence(valid_daily_sequence))
    # print(r.validate_daily_sequence(invalid_daily_sequence))


if __name__ == '__main__':
    main()
