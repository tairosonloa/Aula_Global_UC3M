#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2018 Aitor Alonso at aalonso@aalonso.eu
# This script is under MIT license
#
# Version: 2019.10.30
# You can find new versions and fixes of this script over the time at
# https://github.com/tairosonloa/Aula_Global_UC3M

import http.cookiejar as cookielib
from bs4 import BeautifulSoup as bs
import cgi
import mechanize
import os
import getpass


BASE_URL = "https://aulaglobal.uc3m.es"

# Set the browser for the web crawler
br = mechanize.Browser()
cookiejar = cookielib.LWPCookieJar()
br.set_cookiejar(cookiejar)

br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 1)
br.addheaders = [( 'User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36' )]
br.open(BASE_URL)

# Ask for NIA and password
print("##################################################################\n" +
        "# Download all the content from your courses at UC3M Aula Global #\n" +
        "##################################################################\n")
user = input("Enter NIA: ")
passwd = getpass.getpass(prompt="Enter password: ")

# Submit login form
print("Login in...")
br.select_form(nr=0)
br.form['adAS_username'] = user
br.form['adAS_password'] = passwd
br.submit(id="submit_ok")

# Check if success
url = br.open(BASE_URL)
login = url.get('X-Frame-Options', None)
status, _ = cgi.parse_header(login)
if status.upper() == "DENY":
    print("Login failed. Check your NIA and password and try again")
    exit(1)


# Inspect home page for courses and save them on a set
print("Checking for courses...")
courses = set()
soup = bs(url, "html.parser")
for link in soup.findAll("a"):
    href = link.get("href")
    if href is not None and "/course/view.php" in href:
        courses.add(href)

# Check every course page
for course in courses:
    url = br.open(course)
    soup = bs(url, "html.parser")
    h1 = soup.find("h1").text

    # Don't check Sala de Estudiantes nor Secretaría
    if not "Sala de Estudiantes" in h1 and not "Secretaría" in h1:

        # Create folder where files will be downloaded
        path = os.path.join("courses/", h1.replace("/","."))
        print("\nChecking for files in " + h1)
        if not os.path.exists(path):
            os.makedirs(path)
        
        # Check for files to download
        for link in soup.findAll("a"):
            href = link.get("href")
            if href is not None and "/mod/resource/view.php" in href:

                # Donwload file and get filename from response header
                response = br.open(href)
                cdheader = response.get('Content-Disposition', None)
                value, params = cgi.parse_header(cdheader)
                file  = os.path.join(path, params["filename"].encode("latin-1").decode("utf-8"))
                print("\tDownloading: " + params["filename"].encode("latin-1").decode("utf-8"))
                fh = open(file, 'wb')
                fh.write(response.read())
                fh.close()
