# -*- coding: utf-8
import psycopg2 as pg
import pandas as pd


def connectDB(route_list):
    context = "select spot_name, spot_latitude, spot_longitude from hamamatsu_spot where "
    for route in range(len(route_list)):
        str_text = "spot_name= '" + route_list[route] + "' "
        context = context + str_text
        if route == len(route_list)-1:
            context = context + ';'
        else:
            context = context + 'or '

    conn = pg.connect("host='localhost' port=5432 dbname=ai-tech")
    df = pd.read_sql_query(context, conn)
    return df
