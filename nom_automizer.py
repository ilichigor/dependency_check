import sys
import subprocess
import os
import shutil

src_dat = "res.txt" # path to data file
dst_rep = "."       # path to save the report
url_src = "http://10.7.204.11:8081/repository/npmjs/" # url for upload packages
url_dst = "http://10.7.204.11:8081/repository/base-npm/" # url for unload packages
text_report = ""

tmp_folder = "./tmp"
# Parses command line arguments and set src_dat, dst_rep, url_src, url_dst
# [in] argv - command line arguments
def parse_argv(argv):
    try:
        i = 1
        for param in argv:
            if (param == "-s" or param == "--src"):
                src_dat = argv[i]
            if (param == "-d" or param == "--dest"):
                dst_rep = argv[i]
            if (param == "-us" or param == "--url-src"):
                url_src = argv[i]
            if (param == "-ud" or param == "--url-dst"):
                url_dst = argv[i]
            i += 1
    except:
        text_report += "\nCommand line processing exception\n"

# Downloads package from npm to tmp
# [in] name, version, folder - name and version package, path to folder for download
# [out] respones from npm
def load_package(name, version, folder):
    output = subprocess.run(["npm", "install", name + "@" + version], cwd=folder, stdout=subprocess.PIPE)
    return output.stdout

# Returns a sentence meaningful search text
def search_line_in_text(text, word):
    for i in text.split('\\n'):
        if word in i:
            return str(i)

# Searchs for a non-zero number of vulnerabilities
# [in] respones from npm
# [out] list with remark, if any, else - empty
def check_respones(text):
    text = str(text)
    respones = []
    if text.find("high") != -1 or text.find("critical") != -1:
        if text.find("critical") != -1:
            respones.append(search_line_in_text(text, "critical"))
        else:
            respones.append(search_line_in_text(text, "high"))
    return respones

# Fixes the vulnerability if it can.
# [in] name, version - Name and version package
# [out] if there is a fix version, function generates a new package.json and return 1, else 0
def fix_vulnerability(name, version):
    return 0

# Publishes all dependencies from the current folder to the Nexus
# [in] path to folder with package.json
# [out] list with remark, if any, else - empty
def unload_packages_to_nexus(path):
    # Change rep registry
    subprocess.run(["npm", "set", "registry", url_dst], stdout=subprocess.PIPE)
    try:
        subprocess.run(["npm", "set", "registry", url_dst], cwd=path, stdout=subprocess.PIPE)
    except:
        text_report += "\nUnload packages to nexus exception\n"
    # Restore rep registry
    subprocess.run(["npm", "publish"], stdout=subprocess.PIPE)
    return 0

# Deletes all contents of a folder
# [in] path to folder
def clear_folder(name_folder):
    shutil.rmtree(name_folder)

# Creates a new report file
# [in] text to write to the report
def generate_report(text):
    return 0

# Extracts the package name and version from a string
# [in] line with information about package
# [out] package name, package version
def get_param(line):
    start_version = line.rfind('@')
    return line[0:start_version], line[(start_version + 1):(len(line)-1)]

# Extracts the package name and version from a string
# [in] line with information about package
# [out] package name, package version
def package_cleaning(line):
    if (line.find(" ") == -1 and line.find(",") == -1):
            name, version = get_param(line)
    else:    
        if (line.find(' ') != -1):
            line = line.split(' ')[0] + '\n'
            name, version = get_param(line)
        else:
            line = line.split(',')[0] + '\n'
            name, version = get_param(line)
    return name, version

# General function, calls the functions for loading, checking, and unload(to Nexus) packages.
def packet_processing():
    os.mkdir("report")

    file = open("res.txt",'r',encoding = 'utf-8')

    for line in file:
        os.mkdir(tmp_folder)
        name, version = package_cleaning(line)
        print(name, version)

        # Check packet
        respones = load_package(name, version, tmp_folder)
        check = check_respones(respones)
        if (len(check) == 0):
            print("unload")
            #unload_packages_to_nexus(tmp_folder)
        else:
            print("...")
        
        clear_folder(tmp_folder)

if __name__ == "__main__":
    if len (sys.argv) != 3 and len (sys.argv) != 5 and len (sys.argv) != 7 and len (sys.argv) != 9:
        print ("Usage:\npython npm_automizer.py [options...] \
            \n-s,   --src     <file>   Path to file data \
            \n-d,   --dest    <folder> Path to save the report \
            \n-us,  --url-src <url>    Url for upload packages \
            \n-ud,  --url-dst <url>    Url for unload packages")
    else:
        parse_argv(sys.argv)

    try:
        packet_processing()
    except:
        text_report += "\nGLOBAL EXCEPTION\n"
        print("GLOBAL EXCEPTION")

    print ("check")

    generate_report(text_report)

    clear_folder("report")
    #clear_folder("tmp")
