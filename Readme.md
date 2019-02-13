# Python client to UC3M Aula Global
This is a modern and updated python3 fork from my friend yagop's python3 repository at https://github.com/yagop/AGClient

This small python script allows you to download all the content from your [UC3M Aula Global](http://aulaglobal.uc3m.es) courses (.pdf, .docx, .pptx, etc.)

To achieve user authentication, I use the Moodle API that involves making an https request that sends the student password as a parameter in the URL.
## Usage
Download the repository as zip, clone it with git, or just use curl to get only the script. On GNU/Linux or MacOS:
```
curl -o aulaglobal.py "https://raw.githubusercontent.com/tairosonloa/Aula_Global_UC3M/master/aulaglobal.py"
python3 aulaglobal.py
```
## Requirements
Python version 3.5 or above is required to run the script.
Most of GNU/Linux distributions call the package "python3". To install it on Debian based GNU/Linux distros (Ubuntu, Linux Mint, ...):
```
sudo apt-get install python3
```
To install python 3 on MacOS:
```
xcode-select --install
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install python3
```
## License
This script is under [MIT license](https://github.com/tairosonloa/Aula_Global_UC3M/blob/master/LICENSE).
