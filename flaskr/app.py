import json
import os, datetime, time, threading, csv

from flask import Flask, render_template, g, redirect, url_for, request

from applib.Rules import Rules
from applib.Schedule import Schedule
from applib.ScheduleRow import ScheduleRow
from applib.Test import Test


def get_types(file):
    # Słownik z mapowaniem numer na gatunek
    types_numbers_mapping = {}

    with open(file, newline='') as csv_file:
        c_reader = csv.reader(csv_file, delimiter=',')
        for row in c_reader:
            types_numbers_mapping[row[1]] = row[0]

    return types_numbers_mapping


data = os.getcwd() + "/data/"
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

        global schedule
        schedule = Schedule()

        for i in range(len(sequences[0])):
            row = ScheduleRow(datetime.date.today(), 145, sequences[0][i])
            schedule.add_row(row)

        print("Changing schedule_status")
        schedule_status['status'] = '1'


@app.route('/', methods=['GET'])
def index():
    global types_numbers
    return render_template('index.html', types=types_numbers.items())


@app.route('/create-plan', methods=['POST'])
def create_plan():
    item_list = request.form.getlist('items[]')
    global order
    order = []

    for item in item_list:
        item_dict = json.loads(item)
        type_name = types_numbers.get(item_dict['id'])
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
