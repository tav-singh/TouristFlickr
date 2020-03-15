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
    try:
        for child in root:
            count += 1
            if(count < 8756):
                continue
            # print(child.tag, child.attrib)
            childLocation = 0
            for subchild in child:
                # print(subchild.tag)
                if subchild.tag == "urls":
                    for tag_child in subchild:
                        url = tag_child.text
                        # print(url)

                        r = requests.head(url.replace("http", "https"))
                        # print(r.status_code)
                        if (r.status_code / 100 == 2):
                            # print("appending " + str(count))
                            newRoot.append(child)
            if (count % 100 == 0):
                print(count)
                # break
    finally:
        print(count)
        newTree = ET.ElementTree(newRoot)
        print("writing exception xml...")
        newPath = "./tmp/flickr_exception_2.xml"
        newTree.write(newPath)
    countNew = 0
    for child in newRoot:
        # print(child.tag, child.attrib)
        countNew += 1

    newTree = ET.ElementTree(newRoot)
    print("writing new xml...")
    newPath = "./tmp/flickr_nus_xabc_no_dead_links.xml"
    newTree.write(newPath)

    print(count, countNew)
    print("done")