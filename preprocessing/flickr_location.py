import xml.etree.ElementTree as ET
import sys
import gzip
from xml.dom import minidom

def parsePhotos(path):
    print("opening file")
    f = open(path, 'r')
    f.readline()

    content = ""
    for l in f:
        content += l
        if l.startswith(""):
            yield ET.fromstring(content)
            content = ""

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

        # print(child.tag, child.attrib)
        childLocation = 0
        for subchild in child:
            # print(subchild.tag, subchild.attrib)
            if subchild.tag == "location":            
                hasLocation += 1
                childLocation = 1
                newRoot.append(child)

        # if childLocation == 0:
        #     root.remove(child)

    countNew = 0
    for child in newRoot:
        # print(child.tag, child.attrib)
        countNew += 1

    newTree = ET.ElementTree(newRoot)
    print("writing new xml...")
    newPath = "./tmp/flickr_filtered.xml"
    newTree.write(newPath)

    # prettify xml
    # dom = minidom.parse(newPath) # or xml.dom.minidom.parseString(xml_string)
    # pretty_xml_as_string = dom.toprettyxml()
    # pretty = ET.ElementTree(ET.fromstring(pretty_xml_as_string))
    # pretty.write(newPath)

    print(count, hasLocation, countNew)
    print("done")
