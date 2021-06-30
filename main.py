#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import os
from applib.Rules import Rules
# from applib.Plan import Plan
# from applib.Train import Train
from applib.Test import Test
# import matplotlib.pyplot as plt
# from matplotlib import cm
# from matplotlib.ticker import LinearLocator
# import numpy as np


def main():
    print('CWD')
    print(os.getcwd() + "/data")
    data = os.getcwd() + "/data/"

    r = Rules(data + "prod-stal.csv")
    r.get_rules(data + "rules-stal.csv", data + "types-stal.csv")
    r.print_brands_list()

    # p = Plan()
    # p.load_from_csv(data + "prod-stal.csv")
    # p.print_plan()
    # p.train_data()

    # t = Train()
    # t.first_model_train("prod-stal.csv")

    t = Test()
    t.test_1(data + "rules-stal.csv", data + "types-stal.csv")



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


if __name__ == '__main__':
    main()
