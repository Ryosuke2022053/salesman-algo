# -*- coding: utf-8

from flask import Flask, app, render_template, request, send_file
import pandas as pd
from geopy.distance import great_circle
from connectDB import connectDB
from algo import route

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        check_list = request.form.getlist("hage[]")
        now_dis = check_list[:2]
        now_dis = [float(i) for i in now_dis]
        check_list = check_list[2:]
        df = connectDB(check_list)
        header = df.columns
        record = df.values.tolist()
        df_copy = df.copy(deep=True)
        route_list = route(now_dis, df_copy)

        return render_template('index.html', header=header, record=record, route_list=route_list)


@app.route('/map.html')
def show_map():
    return send_file('./templates/map.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
