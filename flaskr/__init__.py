import os
import sqlite3
from flask import Flask
from flask import request, render_template, redirect
from flask import jsonify
import sys
from wtforms import Form, SelectMultipleField
from flask_jsglue import JSGlue 
import json
import copy

NUM_ELE = 15

# LIVING_INDEX_YEARS = ["2015", "2016", "2017", "2018", "2019"]

info_params = {"cost" : ["cost_living_index", "groceries_index" , "restaurant_price_index"] , "pollution" : ["pollution_index"]
    , "traffic": ["traffic_index", "time_index", "inefficiency_index"], "crime": ["crime_index", "safety_index"] }

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def query_db(query, num_ele = 20):
    connection = sqlite3.connect('instance/flaskr.sqlite')
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    # for row in rows:
    #     print(row)
    #     break
    # print(rows[0])
    return rows[:num_ele]

def get_city_info(city):
    query = "select *, photos_nus.id as photo_id from photos_nus inner join cost_view on photos_nus.city=cost_view.city where cost_view.city like '%{}%'" 
    query = query.format(city)
    print(query, file=sys.stderr)
    query_response = query_db(query, 1)
    return query_response

def create_json(photos_list):
    # pics_json = json.dumps(photos_list)
    # print(pics_json)
    formatted_list = []
    class_tag_overall = set()
    for photos in photos_list:
        a = dict()
        a["city"] = photos['city']
        a["country"] = photos['country']
        a["latitude"] = photos['latitude']
        a["longitude"] = photos['longitude']
        # a["cost_id"] = photos['cost_id']
        a["popularity"] = photos['popularity']
        a["class_tag_overall"] = {}
        description_list = []
        url_list = photos['url'].split(',')
        cdn_url_list = photos['cdn_url'].split(',')
        indl_popularity_list = photos['indl_popularity'].split(',')
        print(photos['url'])
        print(url_list)
        class_tags_list = photos['class_tag'].split(',')
        for index in range(0,len(url_list)):
            description_dict = dict()
            description_dict["url"] = url_list[index]
            description_dict["cdn_url"] = cdn_url_list[index]
            description_dict["class_tag"] = class_tags_list[index]
            description_dict["indl_popularity"] = indl_popularity_list[index]
            # print(class_tags_list[index].split("-"))
            for class_tag in class_tags_list[index].split("-"):
                # print(class_tag)
                if class_tag in a["class_tag_overall"]:
                    a["class_tag_overall"][class_tag] = a["class_tag_overall"][class_tag] + 1
                else:
                    a["class_tag_overall"][class_tag] = 1
            class_tag_overall.add(class_tags_list[index])
            description_list.append(description_dict)
        a["description"] = description_list
        for view in info_params:
            view_columns = info_params[view]
            year_list = photos[view + "_year"].split(",")
            view_columns_list = []
            for column_names in view_columns:
                view_columns_list.append(photos[column_names].split(","))
            view_dict = {}
            for year_index in range(len(year_list)):
                year = year_list[year_index]
                view_dict[year] = {}
                for i in range(len(view_columns_list)):
                    view_dict[year][view_columns[i]] = view_columns_list[i][year_index]

            a[view] = copy.deepcopy(view_dict)

        # cost_year_list = photos["year"].split(",")
        # groceries_index_list = photos["groceries_index"].split(",")
        # restaurant_price_index_list = photos["restaurant_price_index"].split(",")
        # cost_living_index_list = photos["cost_living_index"].split(",")
        # cost_dict = {}
        # for year_index in range(len(cost_year_list)):
        #     year = year_list[year_index]
        #     cost_dict[year] = {}
        #     cost_dict[year]["groceries_index"] = groceries_index_list[year_index]
        #     cost_dict[year]["restaurant_price_index"] = restaurant_price_index_list[year_index]
        #     cost_dict[year]["cost_living_index"] = cost_living_index_list[year_index]
        # a["cost"] = copy.deepcopy(cost_dict)


        # for year in LIVING_INDEX_YEARS:
        #     a["cost_living_index_" + year] = photos['cost_living_index_' + year]
        #     a["groceries_index_" + year] = photos['groceries_index_' + year]
        #     a["restaurant_price_index_" + year] = photos['restaurant_price_index_' + year]
        formatted_list.append(a)
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n")
    # print(formatted_list)
    return formatted_list


def get_top_elements_from_db(pref):
    # query = "select * from photos where class_tag = ? order by popularity desc"
    # query = "select *, photos.id as photo_id from photos inner join costs_combined on photos.cost_id=costs_combined.id where class_tag = ? order by popularity desc"
    total_pref = len(pref)
    ret_ele = []
    inner_query = "select * from photos_nus where class_tag like '%{}%'"
    inner_query = inner_query.format(pref[0])
    print(inner_query)
    if(total_pref == 2 ):
        inner_query = inner_query + " and class_tag like '%{}%'"
        inner_query = inner_query.format(pref[1])
    elif(total_pref == 3):
        inner_query = inner_query +  " and class_tag like '%{}%'" + " and class_tag like '%{}%'"
        inner_query = inner_query.format(pref[1], pref[2])
    # for p in pref:
    #     inner_query.format()
    query = "select * from (" \
            "select city, country, latitude, longitude, sum(popularity) as popularity, group_concat(url) as url, " \
            "group_concat(cdn_url) as cdn_url, group_concat(class_tag) as class_tag, group_concat(popularity) as " \
            "indl_popularity from (" + inner_query + ")" + " group by city, country" \
            ") as p inner join  [cost_view] c on p.city = c.city inner join [pollution_view] po on c.city = po.city " \
                                                           "inner join [crime_view] cr on cr.city = po.city inner join " \
                                                           "[traffic_view] t on t.city = cr.city where " \
                                                           "p.country = c.country and po.country = c.country and cr.country = po.country " \
                                                           "and t.country = cr.country order by p.popularity desc"
    print(query)
    # print(tuple(pref))
    and_query_response = query_db(query, NUM_ELE)
    ret_ele.extend(and_query_response)
    ele_remaining = NUM_ELE - len(and_query_response)
    if(ele_remaining > 2 and total_pref > 1):
        query = "select * from (" \
                "select city, country, latitude, longitude, sum(popularity) as popularity, group_concat(url) as " \
                "url, group_concat(class_tag) as class_tag from (" + "select * from photos_nus where class_tag like '%?%'" + \
                ")" + " group by city,country) as p inner join  [cost_view] c on p.city = c.city inner join [pollution_view] po on c.city = po.city " \
                      "inner join [crime_view] cr on cr.city = po.city inner join " \
                      "[traffic_view] t on t.city = cr.city where " \
                      "p.country = c.country and po.country = c.country and cr.country = po.country " \
                      "and t.country = cr.country " \
                      "order by p.popularity desc"
        for ele in pref:
            query_response = query_db(query.format(ele), int(ele_remaining/total_pref))
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
        if pref is None:
            return redirect('/')
        print(pref, file=sys.stderr)
        result = json.dumps(get_top_elements_from_db(pref))
        print(result, file=sys.stderr)
        return render_template('map.html', result=result, pref=pref)

    @app.route('/city_info', )
    def city_info():
        query = request.args.get('data')
        query = json.loads(query)
        # data = get_city_info(query)
        print(json.dumps(query), file=sys.stderr)
        html = render_template('city_info.html', data=query, raw=json.dumps(query))
        return jsonify({'results':html})

    from . import db
    db.init_app(app)

    return app