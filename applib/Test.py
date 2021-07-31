#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import csv
import networkx as nx
import matplotlib.pyplot as plt
import trotter


class Test:
    #
    # Lista na reguly nastepstw z wygenerowanego pliku csv
    #
    g_data = []

    def test_1(self, file_1, types_numbers_mapping, order, extra_items=[]):

        items = 0

        #
        # Zadane typy stali do wyprodukowania
        #
        # types_to_process = [100, 102, 88, 33]
        types_to_process = []

        # Przykład tablicy order
        # [{'id': '33', 'tonnage': '900', 'name': 'ATLASIII'}, {'id': '102', 'tonnage': '700', 'name': 'ATLASIII S2'},
        # {'id': '100', 'tonnage': '500', 'name': 'C17CMC-B'}, {'id': '88', 'tonnage': '400', 'name': 'S355K2'}]
        for item in order:
            types_to_process.append(int(item['id']))

        # Typy stali do przetworzenia
        # INFO:
        # Poniewaz ze wzgledu na reguly nastepstw najczessciej zadane typy stali nie bedzie mozna
        # polaczyc w jeden ciag wiec w sekwencji docelowej musza byc dodane dodatkowe typy stali
        # aby w sekwencja wynikowa byla zgodna z regulami nastepstw i zawierala wszystkie
        # zadane typy stali
        #
        all_types_to_process = []

        #
        # Lista na reguly nastepstw z ktore zawiera w sobie zadane typy stali na 1 lub drugiej pozycji
        #
        rules = []

        #
        # Lista na sciezki pomiedzy kazda kombinacja 2 punktow grafu
        #
        paths_all_single = []

        #
        # Czasami istneije koniecznosc lacznie pojedynczych sciezek poniewaz moze
        # sie zdarzyc ze zadna pojedyncza sciezka nie bedzie zawierala wszystkich
        # punktow, czyli zadanych typow stali
        #
        paths_all = []

        #
        # Lista na sciezki (sekwencje) ktore zawieraja w sobie zadane typy stali
        #
        paths_correct = []

        #
        # Lista na sciezki (sekwencje) ktore zawieraja w sobie zadane typy stali
        # Jest to sublista "paths_correct" ktora zawiera te sekwencje ktore sa najkrotsze
        #
        paths_result = []

        #
        # Przetworzenie pliku csv zawierajacego reguly
        #
        with open(file_1, newline='') as csv_file:
            c_reader = csv.reader(csv_file, delimiter=',')
            for row in c_reader:
                if row[3] != row[4]:
                    # self.rules[0].append(int(row[3]))
                    # self.rules[1].append(int(row[4]))
                    # self.rules[2].append(int(row[2]))
                    self.g_data.append([int(row[3]), int(row[4])])
                    items += 1

        #
        # Wypenienie listy rules cyli listy:
        # ktora zawiera w sobie zadane typy stali na 1 lub 2 pozycji
        #
        for x in self.g_data:
            for z in types_to_process:
                if z == x[0] or z == x[1]:
                    rules.append(x)

        print("Rules: ")
        print(rules)

        #
        # WIZUALIZACJA (zapisanie grafy do pliku graph.png)
        #
        # Poniewaz liste regul nastepstw naturalnie mozna pradstawic za pomoca grafu skierowanego
        # ponizszy kod tworzy i wizualizuje graf przy uzyciu biblioteki networkx
        #
        plt.figure(figsize=(20, 20), dpi=80)

        G = nx.DiGraph()
        G.add_edges_from(rules)

        color_map = []
        for node in G:
            if node in types_to_process:
                color_map.append('red')
            else:
                color_map.append('lightgray')

        nx.draw_networkx(G, node_color=color_map, with_labels=True)
        plt.savefig('graph.png')
        plt.clf()

        # *****************Wyszukiwanie sekwencji ************************

        #
        # Utworzenie listy "all_types_to_process" na podstawie wyselekcjonowanych regul "rules"
        #
        for r in rules:
            if r[0] not in all_types_to_process:
                all_types_to_process.append(r[0])
            if r[1] not in all_types_to_process:
                all_types_to_process.append(r[1])

        print("all types to process:")
        print(all_types_to_process)
        print("types to process:")
        print(types_to_process)

        #
        # Utworzenie listy wszystkich par typow stali do przetworzenia i zapisanie ich do listy "perm"
        #
        p = trotter.Permutations(2, types_to_process)
        perm = p[0:]

        print("Perm: ")
        print(perm)

        # ZZZ
        # Wyszukanie w utworzonym grafie najkrotszych sciezek poniedzy kombinacja wszystkich punktow
        # Wynik zapisujemy do paths_all_single i paths_all
        # W liscie paths_all bedziemu pozniej dodawac zlaczenie pojedynczycz sciezek wg regul nastepstw
        # poniewaz nie kazde dwie pojedyncze sciezki mozna ze soba polaczyc
        #
        for p in perm:
            if nx.has_path(G, p[0], p[1]):
                sp = nx.shortest_path(G, p[0], p[1])
                paths_all_single.append(sp)
                paths_all.append(sp)

        print("paths 1")
        print(paths_all)
        paths_all = sorted(paths_all, key=len)
        paths_all_single = sorted(paths_all_single, key=len)
        print("paths 1")
        print(paths_all)

        found = 0
        tmp_paths = []
        while found != 1:
            for p1 in paths_all:
                if set(types_to_process).issubset(p1):
                    print("found:")
                    print(p1)
                    found = 1
                    break
                for p2 in paths_all_single:
                    if p1[-1] == p2[0]:
                        tmp_paths.append(p1[:-1] + p2)

            for p3 in tmp_paths:
                paths_all.append(p3)

            tmp_paths = []


        #
        # Laczenie sciezek. Poniewaz w "paths_all" i "paths_all_single" sa te same sciezki laczymy ze soba
        # pojedyncze sciezki.
        # UWAGA
        # Byc moze badzie koniecznosc laczyc wiecej pijedynczych sciezek ze soba, nalezalo by wowczas
        # ustalic tzw glebokosc laczenia np na podstawie  ilosci zadanych typow stali
        # Aktualnie mozna powiedziec ze glebokosc jest stala i wynosi 2
        #
        # for p1 in paths_all_single:
        #     for p2 in paths_all_single:
        #         if list(p1) != list(p2):
        #             for r in rules:
        #                 if p1[-1] == r[0] and p2[0] == r[1]:
        #                     pm = p1 + p2
        #                     add = 1
        #                     for p in paths_all:
        #                         if list(p) == list(pm):
        #                             add = 0
        #                             break
        #                     if add == 1:
        #                         paths_all.append(pm)
        #
        # print("paths 2")
        # print(paths_all)
        #
        # #
        # Utworzenie listy prawidlowych sekwencji "paths_correct"
        #
        for path in paths_all:
            print(path)
            if all(elem in list(path) for elem in types_to_process):
                paths_correct.append(path)

        print("paths correct:")
        print(paths_correct)

        #
        # Wyselekcjonowanie najkrotszych sekwencji.
        #
        # Jest to nasz wynik
        #
        min_l = min(map(len, paths_correct))
        print("min l: ", min_l)

        paths_result_mapped = []
        for p in paths_correct:
            if len(p) == min_l:
                path_result_mapped = []
                for type in p:
                    path_result_mapped.append(types_numbers_mapping.get(str(type)))
                paths_result.append(p)
                paths_result_mapped.append(path_result_mapped)

        print("---------------Paths result: ----------------")
        print(paths_result)
        print(paths_result_mapped)

        #
        # WIZUALIZACJA WYNIKU
        #
        no = 1
        for p in paths_result:
            color_map = []
            GS = G.subgraph(p)

            lbl = {}
            sec = 1
            for x in p:
                if x in lbl:
                    lbl[x] = lbl[x] + ", " + str(sec)
                else:
                    lbl[x] = "(" + str(x) + ") " + str(sec)
                sec += 1

            for node in GS:
                if node in types_to_process:
                    color_map.append('red')
                else:
                    color_map.append('lightgray')
                # if node in list([p[0]]):
                #     color_map.append('green')
                # elif node in list([p[-1]]):
                #     color_map.append('red')
                # else:
                #     color_map.append('lightblue')

            nx.draw_networkx(GS, node_color=color_map, arrowsize=20, with_labels=True, labels=lbl, label="Legenda")
            plt.savefig('graph_' + str(no) + '.png')
            plt.clf()
            no += 1

        return paths_result
