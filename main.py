#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import os
from applib.Rules import Rules


def main():
    print('CWD')
    print(os.getcwd() + "/data")
    data = os.getcwd() + "/data/"

    r = Rules(data + "prod-stal.csv")
    r.get_rules(data + "rules-stal.csv", data + "types-stal.csv")
    r.print_brands_list()


if __name__ == '__main__':
    main()
