import json
import os, datetime, time, threading, csv
from operator import itemgetter

from flask import Flask, render_template, g, redirect, url_for, request

from applib.Rules import Rules
from applib.Schedule import Schedule
from applib.ScheduleRow import ScheduleRow
from applib.Test import Test


def create_types_data(file):
    # Słownik z mapowaniem numer na gatunek i częstotliwość występowania
    types_data = {}

    with open(file, newline='') as csv_file:
        c_reader = csv.reader(csv_file, delimiter=',')
        for row in c_reader:
            types_data[row[1]] = [row[0], row[6]]

    return types_data


def get_types(file):
    # Słownik z mapowaniem numer na gatunek
    types_numbers_mapping = {}

    with open(file, newline='') as csv_file:
        c_reader = csv.reader(csv_file, delimiter=',')
        for row in c_reader:
            types_numbers_mapping[row[1]] = row[0]

    return types_numbers_mapping


data = os.getcwd() + "/data/"
types_data = create_types_data(data + "types-stal.csv")
types_numbers = get_types(data + "types-stal.csv")

schedule_status = {
    "status": "0"
}

schedule = Schedule()
order = []
extra_items = 0

app = Flask(__name__)


@app.context_processor
def get_current_status():
    return {"current_status": schedule_status}


def create_schedule():
    with app.app_context():
        global schedule_status
        global types_numbers
        global types_data

        schedule_status['status'] = '0'

        print('CWD')
        print(os.getcwd() + "/data")
        data = os.getcwd() + "/data/"

        r = Rules(data + "prod-stal.csv")
        r.get_rules(data + "rules-stal.csv", data + "types-stal.csv")
        r.create_rules_dictionary()
        r.print_brands_list()

        global order
        global extra_items
        t = Test()
        sequences = t.test_1(data + "rules-stal.csv", types_numbers, order, extra_items)

        ordered_types = [item['id'] for item in order]

        if len(sequences[0]) == len(order):
            final_path = sequences[0]
        else:
            sequences_with_score = []
            for sequence in sequences:
                sequence_with_score = {"sequence": sequence}
                score = 0
                for steel_type in sequence:
                    if str(steel_type) not in ordered_types:
                        score += int(types_data.get(str(steel_type))[1])
                sequence_with_score["score"] = score
                sequences_with_score.append(sequence_with_score)

            print(sequences_with_score)
            final_path = max(sequences_with_score, key=itemgetter('score')).get('sequence')

        global schedule
        schedule = Schedule()

        print(final_path)
        for i in range(len(final_path)):
            row = ScheduleRow(datetime.date.today(), 145, types_data.get(str(final_path[i]))[0])
            schedule.add_row(row)
            if str(final_path[i]) not in ordered_types:
                schedule.add_extra_type(final_path[i])

        print("Extra types in schedule: ")
        print(schedule.extra_types)
        print("Changing schedule_status")
        schedule_status['status'] = '1'


@app.route('/', methods=['GET'])
def index():
    global types_data
    return render_template('index.html', types=types_data.items())


@app.route('/create-plan', methods=['POST'])
def create_plan():
    item_list = request.form.getlist('items[]')
    global order
    order = []

    for item in item_list:
        item_dict = json.loads(item)
        type_name = types_data.get(item_dict['id'])[0]
        item_dict["name"] = type_name
        order.append(item_dict)

    global extra_items
    extra_items = request.form.get('extra-items')

    thread = threading.Thread(target=create_schedule)
    thread.daemon = True
    thread.start()

    return render_template("order-data.html", order=order)


@app.route('/plan', methods=['GET'])
def plan():
    with app.app_context():
        global schedule_status
        global order
        if schedule_status['status'] == '0':
            return render_template('progress.html', order=order)
        else:
            global schedule
            return render_template('plan.html', order=order, schedule=schedule.schedule)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
