from ensurepip import version
from unicodedata import name


class Vulnerability:
  def __init__(self, cveNum = '', publicationDate = '', cvss3 = '', vector = ''):
    self.cveNum = cveNum
    self.publicationDate = publicationDate
    self.cvss3 = cvss3
    self.vector = vector

class Dependency:
  def __init__(self, type = '', groupId = '', artifactId = '', version = '', public = '', publicationDate = '', numDownloads = '', vulnerabilities = []):
    self.type = type
    self.groupId = groupId
    self.artifactId = artifactId
    self.version = version
    self.public = public
    self.publicationDate = publicationDate
    self.numDownloads = numDownloads
    self.vulnerabilities = vulnerabilities

def __str__(self):
        return("Dependency "+str(self.type)+":"+str(self.groupId)+":"+str(self.artifactId)+":"+str(self.version)
        +":"+str(self.public)+":"+str(self.publicationDate)+":"+str(self.numDownloads)+":"+str(self.vulnerabilities))
    