import os, datetime, time, threading, csv

from flask import Flask, render_template, g, redirect, url_for, request

from applib.Rules import Rules
from applib.Schedule import Schedule
from applib.ScheduleRow import ScheduleRow
from applib.Test import Test


def get_types(file):
    # Słownik z mapowaniem numer na gatunek
    types_numbers_mapping = {}
    # Wypełnienie słownika z mapowaniem numer na gatunek

    with open(file, newline='') as csv_file:
        c_reader = csv.reader(csv_file, delimiter=',')
        for row in c_reader:
            types_numbers_mapping[row[1]] = row[0]

    return types_numbers_mapping


data = os.getcwd() + "/data/"
types_numbers = get_types(data + "types-stal.csv")

schedule_status = {
    "status": "0",
    "progress": '0'
}

schedule = Schedule()

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

        t = Test()
        sequences = t.test_1(data + "rules-stal.csv", types_numbers)

        global schedule
        schedule = Schedule()

        for i in range(len(sequences[0])):
            row = ScheduleRow(datetime.date.today(), 141 + i, sequences[0][i])
            schedule.add_row(row)

        time.sleep(20)
        print("Changing schedule_status")
        schedule_status['status'] = '1'


@app.route('/', methods=['GET'])
def index():
    global types_numbers
    return render_template('index.html', types=types_numbers.items())


@app.route('/create-plan', methods=['POST'])
def create_plan():
    selected = request.form.get('type')
    tonnage = request.form.get('type_tonnage')
    print("Selected type: " + str(selected))
    print("Input tonnage: " + str(tonnage))

    thread = threading.Thread(target=create_schedule)
    thread.daemon = True
    thread.start()
    return redirect(url_for('index'))


@app.route('/plan', methods=['GET'])
def plan():
    with app.app_context():
        global schedule_status
        if schedule_status['status'] == '0':
            return render_template('progress.html')
        else:
            global schedule
            return render_template('plan.html', schedule=schedule.schedule)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
