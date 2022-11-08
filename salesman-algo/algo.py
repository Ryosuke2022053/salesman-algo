from geopy.distance import great_circle
import pandas as pd
import folium
from folium.features import DivIcon


# 2点間の距離計算関数
def clac(disA, disB):
    return great_circle(disA, disB).km


# 次の目的地を決める関数
def algo(now_dis, df_loc):
    df_loc['distance'] = 0
    for i in range(len(df_loc)):
        loc_list = [df_loc.loc[i, 'spot_latitude'],
                    df_loc.loc[i, 'spot_longitude']]
        df_loc.loc[i, 'distance'] = clac(now_dis, loc_list)

    next_loc_index = df_loc['distance'].idxmin()
    next_spot = df_loc.loc[next_loc_index, 'spot_name']
    next_loc = [df_loc.loc[next_loc_index, 'spot_latitude'],
                df_loc.loc[next_loc_index, 'spot_longitude']]
    df_loc = df_loc.drop(df_loc.index[[next_loc_index]])
    df_loc = df_loc.reset_index(drop=True)

    return next_spot, df_loc


# 実行関数
def route(now_dis, df_loc):
    create_map(now_dis, df_loc)
    route_list = []
    for i in range(len(df_loc)):
        now_spot, df_loc = algo(now_dis, df_loc)
        route_list.append(now_spot)

    return route_list


def create_map(now_dis, df_loc, zoom=10):
    f = folium.Figure(width=500, height=500)

    m = folium.Map(now_dis, zoom_start=zoom)
    folium.Marker(
        location=now_dis,
        popup='現在地',
        tooltip="<i>現在地</i>",  # HTMLタグも使える
        icon=folium.Icon(color="red", icon="info-sign"),  # 色やマーカーのアイコンを変更できる
    ).add_to(m)

    for i in range(0, len(df_loc)):
        folium.Marker(location=[df_loc["spot_latitude"][i],
                                df_loc["spot_longitude"][i]],
                      icon=DivIcon(
            icon_size=(150, 36),
            icon_anchor=(7, 20),
            html='<div style="font-size: 18pt; color : black">' +
            str(i+1) + '</div>'),
            tooltip="<i>" + df_loc['spot_name'][i] + "</i>",
            popup=df_loc['spot_name'][i]
        ).add_to(m)
        m.add_child(folium.CircleMarker([df_loc["spot_latitude"][i],
                                         df_loc["spot_longitude"][i]], radius=15))

    m.save('./templates/map.html')
