import xml.etree.ElementTree as ET
import sys
import sqlite3


def insert_db(num_columns, out):
    query = 'insert into photos_nus(comments, views, popularity, latitude, longitude, city, country, url, cdn_url, class_tag' \
            ') values ({0})'
    query = query.format(','.join('?' * num_columns))
    connection = sqlite3.connect('../instance/flaskr.sqlite')
    cursor = connection.cursor()
    for tup in out:
        cursor.execute(query, tup)
        connection.commit()

def get_cost_from_db(city, country):
    print(city, country)
    connection = sqlite3.connect('../instance/flaskr.sqlite')
    cursor = connection.cursor()
    t = (city.lower(),)
    query = 'select id from cost where LOWER(city)=?'
    cursor.execute(query, t)
    cost = cursor.fetchone()
    if cost is None:
        query = 'select id from costs_combined where LOWER(country)=?'
        cursor.execute(query, (country.lower(),))
        cost = cursor.fetchone()
    print("Getting cost")
    print(cost)
    return cost

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 load_photos_to_db.py [filepath]')
        sys.exit(0)

    path = sys.argv[1]

    tree = ET.parse(path)
    root = tree.getroot()
    a = {}
    p_tags= ["city", "nature", "beach", "architecture", "lake", "mountains"]
    i = 0
    tuplist = []
    count_city = 0
    count_country = 0
    # get_cost_from_db('Agoura Hills', 'United States')
    # exit(0)
    for child in root:
        # i = i % 6
        flag = 1
        views = int(child.attrib["views"])
        comments = 0
        popularity = views + comments
        latitude = 0.0
        longitude = 0.0
        city = ""
        country = ""
        photo_url = ""
        tag = ""
        class_tag = p_tags[i]
        crime_id = 0
        tagsList = []
        cdn_url = "https://farm{0}.staticflickr.com/{1}/{2}_{3}.jpg".format(child.attrib["farm"],
                                                                            child.attrib["server"],
                                                                            child.attrib["id"],
                                                                            child.attrib["secret"])
        # print(cdn_url)
        # break
        for subchild in child:
            if subchild.tag == "urls":
                for url in subchild:
                    photo_url = photo_url + url.text

            if subchild.tag == "tags":
                for tag in subchild:
                    # tagsList.append(tag.text.join(tag.text.split()))
                    tag_text = tag.text.join(tag.text.split())
                    if tag_text in p_tags:
                        tagsList.append(tag_text)
                    # if tag_text in a:
                    #     a[tag_text] = a[tag_text] + 1
                    # else:
                    #     a[tag_text] = 1
                # tagsList.append(p_tags[i])
                if not tagsList:
                    continue
            if subchild.tag == "comments":
                if subchild.text.isspace() == False:
                    comments = int(subchild.text)
            if subchild.tag == "location":
                latitude = float(subchild.attrib["latitude"])
                longitude = float(subchild.attrib["longitude"])
                locality = subchild.find("locality")
                if locality is None:
                    flag = 0
                    count_city = count_city + 1
                    break
                else:
                    city = city + locality.text

                country_t = subchild.find("country")
                if country_t is None:
                    flag = 0
                    count_country = count_country + 1
                    break
                else:
                    country = country + country_t.text
        if(flag == 0):
            continue
        class_tag = "-".join(ele for ele in tagsList)
        # print(tagsList)
        # print(comments, views, popularity, latitude, longitude, city, country, photo_url, tags, class_tag)
        # cost_id = get_cost_from_db(city, country)
        # if cost_id is None:
        #     continue
        # print(cost_id[0])
        tuplist.append((comments, views, popularity, latitude, longitude, city, country, photo_url, cdn_url, class_tag,))
        # print(tags)
        # i = i + 1
        # if(i == 4):
        #     break

    print(count_city)
    insert_db(10, tuplist)
    print("done processing xml")











                    # print(tag.text)
                    # tag_text = tag.text
                    # if tag_text in a:
                    #     a[tag_text] = a[tag_text] + 1
                    # else:
                    #     a[tag_text] = 1
        # break
    # a_rev = {k: v for k, v in sorted(a.items(), key=lambda item: item[1], reverse=True)}
    # sorted_a = sorted(a.items(), key=lambda kv: kv[1], reverse=True)
    # print(sorted_a[:100])


