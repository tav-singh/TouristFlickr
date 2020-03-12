import os
import sqlite3
from flask import Flask
from flask import request, render_template
from flask import jsonify
import sys
from wtforms import Form, SelectMultipleField
from flask_jsglue import JSGlue 
import json

NUM_ELE = 2

LIVING_INDEX_YEARS = ["2016", "2017", "2018"]

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def query_db(query, params, num_ele = 20):
    connection = sqlite3.connect('instance/flaskr.sqlite')
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    # for row in rows:
    #     print(row)
    #     break
    # print(rows[0])
    return rows[:num_ele]

def get_city_info(photo_id):
    query = "select *, photos.id as photo_id from photos inner join costs_combined on photos.cost_id=costs_combined.id where photo_id = ?"
    query_response = query_db(query, (photo_id,), 1)
    return query_response

def create_json(photos_list):
    # pics_json = json.dumps(photos_list)
    # print(pics_json)
    formatted_list = []
    for photos in photos_list:
        a = dict()
        a["city"] = photos['city']
        a["country"] = photos['country']
        a["latitude"] = photos['latitude']
        a["longitude"] = photos['longitude']
        a["cost_id"] = photos['cost_id']
        a["popularity"] = photos['popularity']
        description_list = []
        url_list = photos['url'].split(',')
        print(photos['url'])
        print(url_list)
        class_tags_list = photos['class_tag'].split(',')
        for index in range(0,len(url_list)):
            description_dict = dict()
            description_dict["url"] = url_list[index]
            description_dict["class_tag"] = class_tags_list[index]
            description_list.append(description_dict)
        a["description"] = description_list
        for year in LIVING_INDEX_YEARS:
            a["cost_living_index_" + year] = photos['cost_living_index_' + year]
            a["groceries_index_" + year] = photos['groceries_index_' + year]
            a["restaurant_price_index_" + year] = photos['restaurant_price_index_' + year]
        formatted_list.append(a)
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n")
    print(formatted_list)
    return formatted_list


def get_top_elements_from_db(pref):
    # query = "select * from photos where class_tag = ? order by popularity desc"
    # query = "select *, photos.id as photo_id from photos inner join costs_combined on photos.cost_id=costs_combined.id where class_tag = ? order by popularity desc"
    total_pref = len(pref)
    ret_ele = []
    inner_query = "select * from photos where class_tag=?"
    if(total_pref == 2 or total_pref == 3):
        inner_query = inner_query + " and class_tag=?" * (number_of_pref - 1)
    query = "select * from (" \
            "select city, country, latitude, longitude, cost_id, sum(popularity) as popularity, group_concat(url) as url, group_concat(class_tag) as class_tag " \
            "from (" + inner_query + ")" + " group by city" \
            ") as p inner join costs_combined on p.cost_id=costs_combined.id order by p.popularity desc"
    and_query_response = query_db(query, tuple(pref), NUM_ELE)
    ret_ele.extend(and_query_response)
    ele_remaining = NUM_ELE - len(and_query_response)
    if(ele_remaining > 2 and total_pref > 1):
        query = "select * from (" \
                "select city, country, latitude, longitude, cost_id, sum(popularity) as popularity, group_concat(url) as url, group_concat(class_tag) as class_tag " \
                "from (" + "select * from photos where class_tag=?" + ")" + " group by city" \
                                               ") as p inner join costs_combined on p.cost_id=costs_combined.id order by p.popularity desc"
        for ele in pref:
            query_response = query_db(query, (ele,), int(ele_remaining/total_pref))
            # print(query_response)
            ret_ele.extend(query_response)
    # print(ret_ele)
    formatted_list = create_json(ret_ele)
    return  formatted_list

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    jsglue = JSGlue(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        title = "Input Preference"
        print(os.getcwd(), file=sys.stderr)
        return render_template('user_pref.html', title=title)

    @app.route('/attractions', methods=['GET'])
    def user_pref():
        # print(request.args.get('pref'), file=sys.stderr)
        pref = request.args.get('pref')
        # print(pref, file=sys.stderr)
        result = json.dumps(get_top_elements_from_db([pref]))
        print(result)
        return render_template('map.html', result=result, pref=pref)

    @app.route('/city_info')
    def city_info():
        query = request.args.get('photo_id')
        data = get_city_info(query)
        print(data[0], file=sys.stderr)
        html = render_template('city_info.html', data=data[0])
        return jsonify({'results':html})

    from . import db
    db.init_app(app)

    return app