import os
import sqlite3
from flask import Flask
from flask import request, render_template
import sys
from wtforms import Form, SelectMultipleField
from flask_jsglue import JSGlue 

NUM_ELE = 2

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


def get_top_elements_from_db(pref):
    query = "select * from photos where class_tag = ? order by popularity desc"
    total_pref = len(pref)
    ret_ele = []
    for ele in pref:
        query_response = query_db(query, (ele,), int(NUM_ELE/total_pref))
        # print(query_response)
        ret_ele.extend(query_response)
    return  ret_ele

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
        result = get_top_elements_from_db([pref])
        # print(result)
        return render_template('map.html', result=result, pref=pref)

    from . import db
    db.init_app(app)

    return app