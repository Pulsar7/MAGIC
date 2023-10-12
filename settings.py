#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: settings.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""
import os
from dotenv import load_dotenv


load_dotenv()
###### Loading values from the .env-File ######

### Speak


### Person-Database
PERSON_DB_HOST:str = os.environ.get("PERSON_DB_HOSTNAME")
PERSON_DB_PWD:str = os.environ.get("PERSON_DB_PWD")
PERSON_DB_USER:str = os.environ.get("PERSON_DB_USER")
PERSON_DB_NAME:str = os.environ.get("PERSON_DB_NAME")

### Logging
LOGGER_FILEDIR:str = os.environ.get("LOGGER_FILEDIR")
TIMEZONE_NAME:str = os.environ.get("TIMEZONE_NAME")

### WebTools
PROXIE_URL:str = os.environ.get("PROXIE_URL")

