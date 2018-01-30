# Python client to UC3M Aula Global
This is a fork from my friend yagop's repository at https://github.com/yagop/AGClient

This small python script allows you to download all the content from your [Aula Global](http://aulaglobal.uc3m.es) courses (.pdf, .docx, .pptx, etc.)

To achieve user authentication, I use the Moodle API that involves making an https request that sends the student password as a parameter in the URL.
## Usage
Download the repository as zip, clone it with git, or just use wget to get only the script.
```
wget https://raw.githubusercontent.com/tairosonloa/Aula_Global_UC3M/master/aulaglobal.py
python3 aulaglobal.py
```
## Requirements
Python version 3.5 or above is required to run the script.
To install it on debian and ubuntu:
```
# apt-get install python3
```
Most of GNU/Linux distributions call the package as "python3"
## License
This script is under [MIT license](https://github.com/tairosonloa/Aula_Global_UC3M/blob/master/LICENSE).
