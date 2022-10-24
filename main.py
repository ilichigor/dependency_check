from types import NoneType
from xml.dom.minidom import Element
from xml.etree import ElementTree
import re

def check_none(value):
    if value == None:
        return "Empty"
    else:
        return value.text

POM_FILE="pom.xml"
namespaces = {'xmlns' : 'http://maven.apache.org/POM/4.0.0'}

tree = ElementTree.parse(POM_FILE)
root = tree.getroot()

dickt = {}
prop = root.findall(".//xmlns:properties", namespaces=namespaces)
for elem in prop:
#    print(elem.tag, elem.attrib)
    for p in elem:
        text = re.sub(r'\{[^()]*\}', '', p.tag)
        dickt[str(text)] = p.text
 #       print(text, p.text)


deps = root.findall(".//xmlns:dependency", namespaces=namespaces)

i = 0
for d in deps:
    groupId = d.find("xmlns:groupId", namespaces=namespaces)
    artifactId = d.find("xmlns:artifactId", namespaces=namespaces)
    version    = d.find("xmlns:version", namespaces=namespaces)
    if version != NoneType:
        print(str(i) + '. ' + check_none(groupId) + '\t' + check_none(artifactId) + '\t' + check_none(version))
        i += 1

for key, value in dickt.items():
    print(key, value)
#for gp in dickt:
#    print(gp, gp)