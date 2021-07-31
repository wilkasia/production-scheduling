import pandas as pd


def remove_duplicates(x):
    return list(dict.fromkeys(x))


def make_zeros_list(n):
    list_of_zeros = [0] * n
    return list_of_zeros


df = pd.read_csv('prod-stal.csv')
df["Tonaż"] = pd.to_numeric(df["Tonaż"])

pd.set_option('display.max_rows', df.shape[0] + 1)

# Liczba dni na jaką jest ułożony jest ten harmonogram
unique_days = df.groupby(['Rok', 'Miesiąc', 'Dzień']).size().reset_index().rename(columns={0: 'count'})
index = unique_days.index
number_of_rows = len(index)
print("Liczba dni: " + str(number_of_rows))

# Tonaż całkowity dla poszczególnych materiałów
total_materials = df.groupby('Gatunek')['Tonaż'].sum()
print(total_materials)

# Dzienne sekwencje gatunków
gatunki = dict(tuple(df.groupby(['Rok', 'Miesiąc', 'Dzień'])))

sequences = []

for k, v in gatunki.items():
    sequence = []
    for x in v['Gatunek']:
        sequence.append(x)
    sequences.append(sequence)

print(sequences)

# Reguły następstw po sobie gatunków - dwuelementowe zbiory

rules = []

for sequence in sequences:
    if len(sequence) > 1:
        for i in range(len(sequence) - 1):
            rules.append(tuple([sequence[i], sequence[i + 1]]))

final_rules = remove_duplicates(rules)
print(final_rules)

# Materiały i informacja czy material moze byc pierwszy i ostatni

materials = list(total_materials.keys())
is_first = make_zeros_list(len(materials))
is_last = make_zeros_list(len(materials))

for sequence in sequences:
    first_material = sequence[0]
    last_material = sequence[-1]

    first_material_index = materials.index(first_material)
    last_material_index = materials.index(last_material)

    is_first[first_material_index] = 1
    is_last[last_material_index] = 1

print(len(materials))
print(len(is_first))
print(len(is_last))

materials_data = {'material': materials, 'is_first': is_first, 'is_last': is_last}

materials_data_frame = pd.DataFrame(materials_data)

# Ilość wystąpień poszczególnych gatunków
occurences = df['Gatunek'].value_counts()
print(occurences.get("B500SP"))
