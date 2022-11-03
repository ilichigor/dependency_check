import sys
import subprocess
import os
import shutil
import datetime
from time import sleep


class Automizer:
    def __init__(self, src_dat = "res.txt", dst_rep = ".", url_src = "http://10.7.204.11:8081/repository/npmjs/", url_dst = "http://10.7.204.11:8081/repository/base-npm/"):
        self.src_dat = src_dat # path to data file
        self.dst_rep = dst_rep # path to save the report
        self.url_src = url_src # "https://registry.npmjs.com/" # url for upload packages
        self.url_dst = url_dst # url for unload packages

        self.text_report = []
        self.total_pack = 0
        self.num_unloaded_pack = 0
        self.num_not_unloaded_pack = 0

        self.tmp_folder = "./tmp"
        self.rep_folder = "/report"
        
    # Parses command line arguments and set src_dat, dst_rep, url_src, url_dst
    # [in] argv - command line arguments
    def parse_argv(self, argv):
        try:
            i = 1
            for param in argv:
                if param == "-s" or param == "--src":
                    src_dat = argv[i]
                if param == "-d" or param == "--dest":
                    dst_rep = argv[i]
                if param == "-us" or param == "--url-src":
                    url_src = argv[i]
                if param == "-ud" or param == "--url-dst":
                    url_dst = argv[i]
                i = i + 1
        except:
            self.text_report.append("\nError command line processing exception\n")

    # Downloads package from npm to tmp
    # [in] name, version, folder - name and version package, path to folder for download
    # [out] respones from npm and error
    def load_package(self, name, version, folder):
        try:
            output = subprocess.run(["npm", "install", name + "@" + version], cwd=folder, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        except subprocess.TimeoutExpired:
            self.text_report.append("\nTimeoutExpired npm install " + name + "@" + version)
            return "error", "error"
        return output.stdout, output.stderr

    # Returns a sentence meaningful search text
    def search_line_in_text(self, text, word):
        for i in text.split('\\n'):
            if word in i:
                return str(i)

    # Searchs for a non-zero number of vulnerabilities
    # [in] respones from npm
    # [out] list with remark, if any, else - empty
    def check_respones(self, text):
        text = str(text)
        respones = []
        if text.find("ERR!") != -1:
            respones.append(self.search_line_in_text(text, "ERR!"))
        if text.find("high") != -1 or text.find("critical") != -1:
            if text.find("critical") != -1:
                respones.append(self.search_line_in_text(text, "critical"))
            if text.find("high") != -1:
                respones.append(self.search_line_in_text(text, "high"))
        return respones

    # Fixes the vulnerability if it can.
    # [in] name, version - Name and version package
    # [out] if there is a fix version, function generates a new package.json and return 1, else 0
    def fix_vulnerability(self, name, version):
        return 0

    # Searches text for confirmation of package download
    # [out] 1 - package downloaded, else - 0
    def search_approve(self, text):
        if (text.readlines()[-1]).find("+") != -1:
            return 1
        else:
            self.num_not_unloaded_pack = self.num_not_unloaded_pack + 1
            return 0
        
    # Submits an answer to a question
    def submit_answer(answer):
        sleep(1)
        res.stdin.write(answer)
        res.stdin.flush()

    # Publishes all dependencies from the current folder to the Nexus
    # [in] path to folder with package.json
    # [out] list with remark, if any, else - empty
    def unload_packages_to_nexus(self, path):
        # Change rep registry
        subprocess.run(["npm", "set", "registry", self.url_dst], stdout=subprocess.PIPE)
        res = subprocess.Popen(["npm", "login"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        submit_answer(b'opikpo\n')
        submit_answer(b'Opikpo495\n')
        submit_answer(b'tmp@tmp.tmp\n')
        stdout, stderr = res.communicate()
        try:
            subprocess.run(["npm", "set", "registry", self.url_dst], cwd=path, stdout=subprocess.PIPE)
        except:
            self.text_report.append("\nError unload packages to nexus exception\n")
        # Restore rep registry
        res = subprocess.run(["npm", "publish"], cwd=path + "/node_modules/", stdout=subprocess.PIPE)
        if self.search_approve(res.stdout) == 1:
            self.num_unloaded_pack = self.num_unloaded_pack + 1
        return 0

    # Deletes all contents of a folder
    # [in] path to folder
    def clear_folder(self, name_folder):
        shutil.rmtree(name_folder)

    # Creates a new report file
    # [in] text to write to the report
    # [out] returns files report name
    def generate_report(self, text):
        os.mkdir(self.dst_rep + self.rep_folder)
        now = datetime.datetime.now()
        filename = "report_" + now.strftime("%d-%m-%Y %H:%M") + ".log"
        file = open(self.dst_rep + "/report/" + filename, "w")
        file.write(text)
        file.write("\n\n" + "TOTAL: " + str(self.total_pack) + \
                   "\nUNLOADED PACKAGE: " + str(self.num_unloaded_pack) + \
                   "\nNOT UNLOADED PACKAGE: " + str(self.num_not_unloaded_pack))
        file.close()
        return 0

    # Extracts the package name and version from a string
    # [in] line with information about package
    # [out] package name, package version
    def get_param(self, line):
        start_version = line.rfind('@')
        return line[0:start_version], line[(start_version + 1):(len(line)-1)]

    # Extracts the package name and version from a string
    # [in] line with information about package
    # [out] package name, package version
    def package_cleaning(self, line):
        if line.find(" ") == -1 and line.find(",") == -1:
                name, version = self.get_param(line)
        else:    
            if line.find(' ') != -1:
                line = line.split(' ')[0] + '\n'
                name, version = self.get_param(line)
            else:
                line = line.split(',')[0] + '\n'
                name, version = self.get_param(line)
        return name, version

    # General function, calls the functions for loading, checking, and unload(to Nexus) packages.
    def packet_processing(self):
        file = open(self.src_dat,'r',encoding = 'utf-8')
        self.total_pack = self.total_pack + 1
        for line in file:
            print("\n")
            self.total_pack = self.total_pack + 1
            os.mkdir(self.tmp_folder)
            name, version = self.package_cleaning(line)
            print(name, version)

            # Check packet
            respones, error = self.load_package(name, version, self.tmp_folder)
            if error:
                self.num_not_unloaded_pack  = self.num_not_unloaded_pack + 1
                self.text_report.append("\nError unload " + name + " " + version + "\n")
            else:
                check = self.check_respones(respones)
                if len(check) == 0:
                    print("unload")
                    #unload_packages_to_nexus(tmp_folder)
                else:
                    self.num_not_unloaded_pack = self.num_not_unloaded_pack + 1
                    self.text_report.append("\nError unload " + name + " " + version + "\n")
                    for remark in check:
                        self.text_report.append(str(remark) + "\n")

            self.clear_folder(self.tmp_folder)

if __name__ == "__main__":
    if len (sys.argv) != 3 and len (sys.argv) != 5 and len (sys.argv) != 7 and len (sys.argv) != 9:
        print ("Usage:\npython npm_automizer.py [options...] \
            \n-s,   --src     <file>   Path to file data \
            \n-d,   --dest    <folder> Path to save the report \
            \n-us,  --url-src <url>    Url for upload packages \
            \n-ud,  --url-dst <url>    Url for unload packages")
    else:
        automizer = Automizer()

        try:
            automizer.packet_processing()
        except:
            automizer.text_report.append("\nError GLOBAL EXCEPTION\n")
            print("GLOBAL EXCEPTION")


        automizer.generate_report("".join(automizer.text_report))

    #clear_folder("report")
    #lear_folder("tmp")
