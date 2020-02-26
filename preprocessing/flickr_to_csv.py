import xml.etree.ElementTree as ET
import sys
import csv

# This file only gets the following tags : travel, nature, beach, museum, wildlife, landscape
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 flickr.py [filepath]')
        sys.exit(0)

    path = sys.argv[1]

    print(path)
    
    tree = ET.parse(path)
    root = tree.getroot()

    print("writing csv...")

    with open('./tmp/flickr_sample.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["photo_id", "views", "comments", "tags_raw", "tags", "photo_link"])
        
        for child in root:
            row = []
            row.append(child.attrib["id"])
            row.append(child.attrib["views"])
            for subchild in child:

                if subchild.tag == "tags":
                    tags_raw = []
                    tags= []
                    for tag in subchild:
                        tags_raw.append(tag.attrib["raw"])
                        tags.append(tag.text.join(tag.text.split()))
                    row.append(','.join(tags_raw))
                    row.append(','.join(tags))

                if subchild.tag == "urls":
                    for url in subchild:
                        row.append(url.text)

                if subchild.tag == "comments":
                    # row.append(subchild.text)
                    if subchild.text.isspace() == False: 
                        row.append(subchild.text)

            writer.writerow(row)
            
    print("done")
