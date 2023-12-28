import sys
import xml.etree.ElementTree as ET
import glob
import rlog

'''
1. getXML:
- pull XML values from xml file
- set in-file constants to those values
- return them based on "attribute tag"
2. setXML:
- update in-file constants with given value
- update xml file with given value
'''

# Set defaults
mConfigLoc = 'Dateconfig.xml'


def countXML():
    file = glob.glob(mConfigLoc, recursive=False)
    if file:
        tree = ET.parse(mConfigLoc)
        root = tree.getroot()
        a = 0
        b = 0
        f = 0
        for x in root:
            print("[" + str(a) + "]" + " " + x.tag)
            for y in x:
                print("[" + str(a) + "][" + str(b) + "]" + " " + y.tag)
                for z in y:
                    print("[" + str(a) + "][" + str(b) + "][" + str(f) + "]" + " " + z.tag)
                    f += 1
                b += 1
            a += 1


def getXML(attribute, subattribute=''):
    file = glob.glob(mConfigLoc, recursive=False)
    if file:
        tree = ET.parse(mConfigLoc)
        root = tree.getroot()
        for x in root.iter(attribute):
            if subattribute == '':
                return x.text
            else:
                for y in x.iter(subattribute):
                    return y.text
    else:
        rlog.writelog("Dateconfig.xml does not exist")
        # TODO: create xml with default values


def getXMLName(attribute, subattribute=''):
    file = glob.glob(mConfigLoc, recursive=False)
    if file:
        tree = ET.parse(mConfigLoc)
        root = tree.getroot()
        for x in root.iter(attribute):
            if subattribute == '':
                return x.get('name')
            else:
                for y in x.iter(subattribute):
                    return y.get('name')
    else:
        rlog.writelog("Dateconfig.xml does not exist")
        # TODO: create xml with default values

def setXML(attribute, value, subattribute=''):
    file = glob.glob(mConfigLoc, recursive=False)
    tree = ET.parse(mConfigLoc)
    if file:
        root = tree.getroot()
        for x in root.iter(attribute):
            if subattribute == '':
                x.text = value
            else:
                for y in x.iter(subattribute):
                    y.text = value
    else:
        rlog.writelog("Dateconfig.xml does not exist")
        # TODO: create xml with default values
    tree.write(mConfigLoc)

def getXMLChildren(attribute):
    file = glob.glob(mConfigLoc, recursive=False)
    if file:
        tree = ET.parse(mConfigLoc)
        root = tree.getroot()
        for x in root.findall(attribute):
            return x.findall("*")
        # for x in root.find(attribute):
        #     return x.attrib
    else:
        rlog.writelog("Dateconfig.xml does not exist")
