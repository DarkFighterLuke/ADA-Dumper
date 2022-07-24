# ADA-Dumper
A Python script to dump courses resources from ADA e-learning platform @ DIB UniBa.

## Usage
```
main.py [-h] [-d SAVE_PATH] [-c CONF_PATH]

options:
  -h, --help            show this help message and exit
  -d SAVE_PATH, --save-path SAVE_PATH
                        Base path to save dumped resources
  -c CONF_PATH, --conf-path CONF_PATH
                        Configuration file
```

## Requirements
In order to use this script some dependencies are needed.<br>
The first one is the `chromedriver`, see https://chromedriver.chromium.org/downloads.<br>
The other dependecies are listed in the `requirements.txt` file and can be obtained by running `pip install -r requirements.txt`.

## Why to use
ADA e-learning platform is frequently facing issues, making it unaccessible to students who needs to access resources it hosts. Using this script (and maybe a cron on the system) all resources will be (periodically, if you use a cron) dumped, mitigating the downtime consequences.<br>
<br>
However, the main goal this script has been developed for is to dump the resources from all the courses considering a possible account deletion after graduation.

## How it works
The script leverages Selenium features. Even if it is a module used for automated testing, the use of Selenium grants the absence of needing a JS interpreter to parse the required JS code, so it has been choosen for quickness of developing.


