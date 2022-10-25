from types import NoneType
from xml.dom.minidom import Element
from xml.etree import ElementTree
import re
import classDependency
import numpy as np 

def check_none(value):
    if value == None:
        return "Empty"
    else:
        return value.text

POM_FILE="pom.xml"
namespaces = {'xmlns' : 'http://maven.apache.org/POM/4.0.0'}

tree = ElementTree.parse(POM_FILE)
root = tree.getroot()

#Properties(versions)
dickt = {}
prop = root.findall(".//xmlns:properties", namespaces=namespaces)
for elem in prop:
    for p in elem:
        text = re.sub(r'\{[^()]*\}', '', p.tag)
        if (text.find("version") != -1):
            dickt[str(text)] = p.text

# Dependencies
dependencies = []
deps = root.findall(".//xmlns:dependency", namespaces=namespaces)
for d in deps:
    groupId = d.find("xmlns:groupId", namespaces=namespaces)
    artifactId = d.find("xmlns:artifactId", namespaces=namespaces)
    version    = d.find("xmlns:version", namespaces=namespaces)
    if version != NoneType:
        if check_none(version).find("${") != -1:
            ver = str(check_none(version))[2:][:-1]
            if ver in dickt:
                dependencies.append(classDependency.Dependency(groupId.text, artifactId.text, dickt[ver]))
            else:
                print("Error, " + ver + " not found")
        else:
            dependencies.append(classDependency.Dependency(groupId.text, artifactId.text, check_none(version)))

for p in dependencies: 
    print(p.groupId, p.artifactId, p.version)
    