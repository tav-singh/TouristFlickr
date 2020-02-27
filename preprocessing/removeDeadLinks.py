import xml.etree.ElementTree as ET
import sys
import requests

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 flickr.py [filepath]')
        sys.exit(0)

    path = sys.argv[1]

    print(path)

    tree = ET.parse(path)
    newRoot = ET.Element("photos")
    root = tree.getroot()
    count = 0
    hasLocation = 0
    for child in root:
        count += 1
        print(child.tag, child.attrib)
        childLocation = 0
        for subchild in child:
            # print(subchild.tag)
            if subchild.tag == "urls":
                for tag_child in subchild:
                    url = tag_child.text
                    print(url)

                    r = requests.get(url)
                    if(r.status_code/100 == 2):
                        newRoot.append(child)

    countNew = 0
    for child in newRoot:
        # print(child.tag, child.attrib)
        countNew += 1

    newTree = ET.ElementTree(newRoot)
    print("writing new xml...")
    newPath = "./tmp/flickr_no_dead_links.xml"
    newTree.write(newPath)

    print(count, countNew)
    print("done")