#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2018 Aitor Alonso at mail@aalonso.pw
# This script is under MIT license

"""
This script allows you to download all the
content from your UC3M Aula Global courses.
"""

import getpass
import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as elementTree
import os
import re

domain = "aulaglobal.uc3m.es"
webservice = "/webservice/rest/server.php"
service = "ag_mobile"


# First we need the token
def get_token(user, passwd):
    safe_passwd = urllib.parse.quote(passwd, safe='')
    url_token = "https://" + domain + "/login/token.php?username=" \
        + user + "&password=" + safe_passwd + "&service=" + service
    req = urllib.request.Request(url_token)
    resp = urllib.request.urlopen(req).read()

    # JSON
    data = json.loads(resp.decode("utf8"))
    token = data.get("token")

    # If token is None wrong user/passwd
    if token is None:
        print(data.get("error"))
        exit()
    return token


# Get the userid necessary for get user courses
def get_user_info(token):
    url_info = "https://" + domain + webservice + "?wstoken=" + token \
        + "&wsfunction=core_webservice_get_site_info"
    req = urllib.request.Request(url_info)
    resp = urllib.request.urlopen(req).read()

    # XML
    root = elementTree.fromstring(resp)
    print("Logged as " + root.find("SINGLE/KEY[@name='fullname']/VALUE").text)
    user_id = root.find("SINGLE/KEY[@name='userid']/VALUE").text
    lang = root.find("SINGLE/KEY[@name='lang']/VALUE").text
    return user_id, lang


# Just simply return a list of courses ids with its courses names
def get_courses(token, user_id, lang):
    url_courses = "https://" + domain + webservice + "?wstoken=" \
        + token + "&wsfunction=core_enrol_get_users_courses&userid=" \
        + user_id
    req = urllib.request.Request(url_courses)
    resp = urllib.request.urlopen(req).read()

    root = elementTree.fromstring(resp)
    ids = root.findall("MULTIPLE/SINGLE/KEY[@name='id']/VALUE")  # This is a list
    names = root.findall("MULTIPLE/SINGLE/KEY[@name='fullname']/VALUE")
    courses = [None] * len(names)

    # Format names. Get the name in the correct language and remove metadata
    for i in range(len(names)):
        html_name = names[i].text.split("</span>")
        if len(html_name) > 1:
            tag = 'lang="' + lang + '"'
            for name in html_name:
                if tag in name and "Grado" not in name and "Bachelor" not in name and "Semana" not in name:
                    full_name = re.sub("<.*?>", "", name)
                    courses[i] = {"course_id": ids[i].text, "course_name": re.sub(".[0-9]+/+[0-9]+-\w*", "", full_name)}
    return courses


# Get the course contents (files urls)
def get_course_content(token, course_id):
    url_course = "https://" + domain + webservice + "?wstoken=" + token \
                 + "&wsfunction=core_course_get_contents&courseid=" + course_id

    req = urllib.request.Request(url_course)
    resp = urllib.request.urlopen(req).read()
    root = elementTree.fromstring(resp)
    xml_modules = "MULTIPLE/SINGLE/KEY[@name='modules']/MULTIPLE/"
    xml_contents = "SINGLE/KEY[@name='contents']/MULTIPLE/SINGLE"
    file_contents = root.findall(xml_modules + xml_contents)
    files = []
    for file_content in file_contents:
        file_url = file_content.find("KEY[@name='fileurl']/VALUE").text
        file_name = file_content.find("KEY[@name='filename']/VALUE").text
        file_type = file_content.find("KEY[@name='type']/VALUE").text
        if file_type == "file":
            moodle_file = {"file_name": file_name, "file_url": file_url}
            files.append(moodle_file)
    return files


# Saves the files on disk
def save_files(token, course_name, files):
    if len(files) == 0:
        print("\tThis course has not content.")
    else:
        path = 'courses/' + course_name  # Where the files will be saved
        if not os.path.exists(path):
            os.makedirs(path)

        for moodle_file in files:
            print("\tDownloading: " + moodle_file['file_name'])
            url = moodle_file['file_url'] + '&token=' + token
            file = path + '/' + moodle_file['file_name']
            response = urllib.request.urlopen(url)
            fh = open(file, 'wb')
            fh.write(response.read())
            fh.close()


def main():
    print("##################################################################\n" +
          "# Download all the content from your courses at UC3M Aula Global #\n" +
          "##################################################################\n")
    user = input("Enter NIA: ")
    passwd = getpass.getpass(prompt="Enter password: ")
    token = get_token(user, passwd)
    userid, lang = get_user_info(token)
    courses = get_courses(token, userid, lang)
    for course in courses:
        if course is not None:
            print("\nCourse: " + course["course_name"])
            files_url = get_course_content(token, course["course_id"])
            save_files(token, course["course_name"], files_url)
    print("\nAll files were downloaded.")


if __name__ == '__main__':
    main()
