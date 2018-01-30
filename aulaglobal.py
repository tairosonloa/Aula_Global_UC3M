# !/usr/bin/env python3
# -*- coding: utf-8 -*-


import getpass
import urllib.request
import json
import xml.etree.ElementTree as elementTree
import os

domain = "aulaglobal.uc3m.es"
webservice = "/webservice/rest/server.php"
service = "ag_mobile"


# First we need the token
def get_token(user, passwd):
    url_token = "https://" + domain + "/login/token.php?username=" \
        + user + "&password=" + passwd + "&service=" + service
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

    # Yes, is a XML
    root = elementTree.fromstring(resp)
    name = root.find("SINGLE/KEY[@name='fullname']/VALUE")  # Who am i
    user_id = root.find("SINGLE/KEY[@name='userid']/VALUE").text
    return user_id, name.text


# Just simply return a list of courses ids
def get_courses(token, user_id):
    url_courses = "https://" + domain + webservice + "?wstoken=" \
        + token + "&wsfunction=core_enrol_get_users_courses&userid=" \
        + user_id
    req = urllib.request.Request(url_courses)
    resp = urllib.request.urlopen(req).read()

    # print url_courses
    root = elementTree.fromstring(resp)
    ids = root.findall("MULTIPLE/SINGLE/KEY[@name='id']/VALUE")  # This is a list
    return ids


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
        file_name = file_content.find("KEY[@name='filename']/VALUE"
                                      ).text
        file_type = file_content.find("KEY[@name='type']/VALUE").text
        if file_type == "file":
            moodle_file = {"file_name": file_name, "file_url": file_url}
            files.append(moodle_file)

    return files


def save_files(token, course_id, files):
    # TODO crear carpetas con el nombre del curso, y no nombre ID
    path = 'cursos/' + course_id
    if not os.path.exists(path):
        os.makedirs(path)

    for moodle_file in files:
        print("Downloading: " + moodle_file['file_name'])
        url = moodle_file['file_url'] + '&token=' + token
        file = path + '/' + moodle_file['file_name']
        response = urllib.request.urlopen(url)
        fh = open(file, 'wb')
        fh.write(response.read())
        fh.close()


def main():
    user = input("Enter user: ")
    passwd = getpass.getpass(prompt="Enter password: ")
    token = get_token(user, passwd)
    userid = get_user_info(token)
    ids = get_courses(token, userid)
    for course_id in ids:
        print("Course ID:" + course_id.text)
        files_url = get_course_content(token, course_id.text)
        save_files(token, course_id.text, files_url)


# Main method to develop mode
def develop():
    print("Select an option:")
    print("\t(1) Test get_token(user, passwd)")
    print("\t(2) Test get_user_info(token)")
    print("\t(3) Test get_courses(token, userid")
    print("\t(0) Exit")
    select = input()
    if select != "0":
        user = input("Enter user: ")
        passwd = getpass.getpass(prompt="Enter password: ")
        if select == "1":
            print("Token is "+str(get_token(user, passwd)))
        if select == "2":
            user_id, name = get_user_info(get_token(user, passwd))
            print("User ID: " + user_id + ", " + name)
        if select == "3":
            token = get_token(user, passwd)
            user_id, _ = get_user_info(token)
            courses = get_courses(token, user_id)
            for c in courses:
                print(c)


if __name__ == "__main__":
    main()
    # develop()