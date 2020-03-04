import xml.etree.ElementTree as ET
import sys
import csv

def import_cost(year, cost, row_country, row_city, row_cost):
    NEW_YORK_COST = cost
    col_2018 = []
    file_path = ('../data/cost-of-living/cost-of-living-%s.csv' % year)
    with open(file_path) as csv_file:
        print("Getting living cost %s ..." % year)
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                if row_country == -1:
                    split = [x.strip() for x in row[1].split(',')] 
                    # print(split[0], split[-1])
                    col_data = {
                        "city": split[0],
                        "country": split[-1],
                        "cost": round((float(row[2]) / 100) * NEW_YORK_COST, 2)
                    }
                else:
                    country = "United States" if len(row[row_country]) == 2 else row[row_country]
                    col_data = {
                        "city": row[row_city],
                        "country": country.lstrip(),
                        "cost": round((float(row[row_cost]) / 100) * NEW_YORK_COST, 2)
                    } 
                col_2018.append(col_data)
                line_count += 1
    return col_2018

def get_country_avg(col):
    col_avg = []
    for item in col:
        exist_idx = -1
        for idx, c_avg in enumerate(col_avg):
            if item["country"] == c_avg["country"]:
                exist_idx = idx
                break
        
        if exist_idx == -1:
            col_avg.append({
                "country": item["country"],
                "count": 1,
                "total": item["cost"]
            })
        else:
            col_avg[exist_idx]["count"] += 1
            col_avg[exist_idx]["total"] += item["cost"]

    for idx, item in enumerate(col_avg):
        col_avg[idx] = ({
            "country": item["country"],
            "cost": round(item["total"] / item["count"], 2)
        })

    # print(col_avg)

    return col_avg

# This file only gets the following tags : travel, nature, beach, museum, wildlife, landscape
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 flickr.py [filepath]')
        sys.exit(0)

    path = sys.argv[1]

    print(path)
    
    col_2016 = import_cost("2016", 1140.68, 1, 0, 2)
    col_2016_avg = get_country_avg(col_2016)
    col_2017 = import_cost("2017", 1139.51, 2, 0, 4)
    col_2017_avg = get_country_avg(col_2017)
    print(col_2017)
    col_2018 = import_cost("2018", 1249.44, -1, 1, 2)
    col_2018_avg = get_country_avg(col_2018)

    tree = ET.parse(path)
    root = tree.getroot()

    print("writing csv...")

    with open('./tmp/flickr_sample.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        p_tags= ["travel", "nature", "beach", "museum", "wildlife", "landscape"]
        writer.writerow(["photo_id", "views", "comments", "parent_tag", "tags", "latitude", "longitude", "locality", "country", "photo_link", "cost_2018", "cost_2017", "cost_2016"])
        
        for child in root:
            tags_t = []
            for subchild in child:

                if subchild.tag == "tags":
                    for tag in subchild:
                        if tag.text.join(tag.text.split()) in p_tags:
                            tags_t.append(tag.text.join(tag.text.split()))
            if tags_t == []:
                continue

            row = []
            row.append(child.attrib["id"])
            row.append(child.attrib["views"])
            for subchild in child:

                if subchild.tag == "tags":
                    tags_raw = []
                    tags = []
                    parent_tag = "unknown"
                    for tag in subchild:
                        if tag.text.join(tag.text.split()) in p_tags:
                            parent_tag = tag.text.join(tag.text.split())
                        tags_raw.append(tag.attrib["raw"])
                        tags.append(tag.text.join(tag.text.split()))
                    

                    row.append(parent_tag)
                    row.append(','.join(tags))


                if subchild.tag == "urls":
                    for url in subchild:
                        row.append(url.text)

                if subchild.tag == "comments":
                    # row.append(subchild.text)
                    if subchild.text.isspace() == False: 
                        row.append(subchild.text)

                if subchild.tag == "location":
                    row.append(subchild.attrib["latitude"])
                    row.append(subchild.attrib["longitude"])

                    locality = subchild.find("locality")
                    if locality is None:
                        row.append("unknown")
                    else:
                        row.append(locality.text)

                    country = subchild.find("country")
                    if country is None:
                        row.append("unknown")
                    else:
                        row.append(country.text)

            # print(row)

            # 2018
            cost_found = 0
            for col in col_2018:
                if col["city"].lower() == row[7].lower() and col["country"].lower() == row[8].lower():
                    row.append(col["cost"])
                    cost_found = 1
                    break

            if cost_found == 0:
                country_found = 0
                for col in col_2018_avg:
                    if col["country"].lower() == row[8].lower(): 
                        row.append(col["cost"])
                        country_found = 1
                        break

                if country_found == 0:
                    row.append("unknown")

            # 2017
            cost_found = 0
            for col in col_2017:
                if col["city"].lower() == row[7].lower() and col["country"].lower() == row[8].lower():
                    row.append(col["cost"])
                    cost_found = 1
                    break

            if cost_found == 0:
                country_found = 0
                for col in col_2017_avg:
                    if col["country"].lower() == row[8].lower(): 
                        row.append(col["cost"])
                        country_found = 1
                        break

                if country_found == 0:
                    row.append("unknown")

            # 2016
            cost_found = 0
            for col in col_2016:
                if col["city"].lower() == row[7].lower() and col["country"].lower() == row[8].lower():
                    row.append(col["cost"])
                    cost_found = 1
                    break

            if cost_found == 0:
                country_found = 0
                for col in col_2016_avg:
                    if col["country"].lower() == row[8].lower(): 
                        row.append(col["cost"])
                        country_found = 1
                        break

                if country_found == 0:
                    row.append("unknown")

            with open(file_path) as csv_file:
                print("Getting safety index %s ..." % year)
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row_c in csv_reader:
                
            writer.writerow(row)
            
    print("done")
