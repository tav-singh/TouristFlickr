# import csvreader
import csv
import sqlite3

NUM_COLUMNS = 6
FILE = "../data/cost-of-living-2018-1.csv"

NUM_ELE = 20

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def query_db(query, params, num_ele = 20):
    connection = sqlite3.connect('../instance/flaskr.sqlite')
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

def read_csv(filename):
    connection = sqlite3.connect('../instance/flaskr.sqlite')
    # YEAR = "2016"
    # YEAR = "2017"
    YEAR = "2018"
    # YEAR = str(filename.split("-")[-1].split(".")[0])
    with open(filename) as f:
        reader = csv.reader(f)
        columns = next(reader)
        query = 'insert into living_expense(city, country, cost_living_index, groceries_index, restaurant_price_index, year) values ({0})'
        query = query.format(','.join('?' * NUM_COLUMNS))
        cursor = connection.cursor()
        for line in reader:
            # col_list = []
            # 2016
            # out = (str(line[0]), str(line[1]), str(line[2]), str(line[5]), str(line[6]), YEAR)

            # 2017
            # out = (str(line[0]), str(line[2]), str(line[4]), str(line[6]), str(line[7]), YEAR)

            # 2018
            place = line[1].split(",")
            if(len(place) == 2):
                city = place[0]
                country = place[1]
            elif(len(place) == 3):
                city = place[0]
                country = place[2]
            out = (str(city), str(country), str(line[2]), str(line[5]), str(line[6]), YEAR)
            print(out)
            cursor.execute(query, out)
            connection.commit()
            # break
        connection.close()

if __name__ == '__main__':
    # read_csv(FILE)
    a = get_top_elements_from_db(['nightlife', 'nature'])
    # print(a)
    print(len(a))
