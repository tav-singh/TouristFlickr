import json
import sqlite3
import sys

TRAFFIC_FILE = "../data/traffic.json"
CRIME_FILE = "../data/crime.json"
POLLUTION_FILE = "../data/pollution.json"
COST_FILE = "../data/cost_of_living.json"

def get_tuple(type, city_data, year):
    if type == "traffic":
        return (city_data["city_name"].split(",")[0], city_data["country"], round(city_data["traffic_index"], 2),
                round(city_data["time_index"], 2), round(city_data["inefficiency_index"], 2), int(year))
    elif type == "crime":
        return (city_data["city_name"].split(",")[0], city_data["country"], round(city_data["crime_index"],2),
                round(city_data["safety_index"], 2), int(year))
    elif type == "pollution":
        return (city_data["city_name"].split(",")[0], city_data["country"], round(city_data["pollution_index"],2),
                int(year) )
    elif type == "cost_of_living":
        return (city_data["city_name"].split(",")[0], city_data["country"], round(city_data["cpi_index"], 2),
                round(city_data["groceries_index"],2), round(city_data["restaurant_price_index"], 2), int(year))
    print("Unknown type : " + type )
    sys.exit(-1)

def get_query(type):
    if type == "traffic":
        return 'insert into traffic(city, country, traffic_index, time_index, inefficiency_index, year) values ({0})'
    elif type == "crime":
        return "insert into crime(city, country, crime_index, safety_index, year) values ({0})"
    elif type == "pollution":
        return "insert into pollution(city, country, pollution_index, year) values ({0})"
    elif type == "cost_of_living":
        return "insert into cost(city, country, cost_living_index, groceries_index, restaurant_price_index, year) values ({0})"
    print("Unknown type : " + type )
    sys.exit(-1)

def load_json(file):
    type = file.split("/")[-1].split(".")[0]
    connection = sqlite3.connect('../instance/flaskr.sqlite')
    cursor = connection.cursor()
    with open(file) as json_file:
        data = json.load(json_file)
        traffic_dict_list = []
        for year,value in data.items():
            for city_data in value:
                db_tup = get_tuple(type, city_data, year)
                # print(len(db_tup))
                query = get_query(type)
                query = query.format(','.join('?' * len(db_tup)))
                # print(db_tup)
                # print(query)
                cursor.execute(query, db_tup)
                connection.commit()
                # break

    connection.close()

if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print('Usage: python3 load_json_to_db.py [filepath]')
    #     sys.exit(-1)
    load_json(COST_FILE)

