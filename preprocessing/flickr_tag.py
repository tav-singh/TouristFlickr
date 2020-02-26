import xml.etree.ElementTree as ET
import sys
import gzip
from xml.dom import minidom
from collections import Counter

# This file only gets the following tags : travel, nature, beach, museum, wildlife, landscape
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
    tags = ["travel", "nature", "beach", "museum", "wildlife", "landscape"]

    for child in root:
        count += 1

        childLocation = 0
        for subchild in child:
            if subchild.tag == "tags":
                for tag in subchild:
                    if tag.text in tags:

                        newRoot.append(child)
                        break
            # break
                    

    countNew = 0
    for child in newRoot:
        # print(child.tag, child.attrib)
        countNew += 1

    newTree = ET.ElementTree(newRoot)
    print("writing new xml...")
    newPath = "./tmp/flickr_bytag_s.xml"
    newTree.write(newPath)

    print(count, hasLocation, countNew)
    print("done")
