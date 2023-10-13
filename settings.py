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

### Speech-Recognition


### Person-Database
PERSON_DB_FILEPATH:str = os.environ.get("PERSON_DB_FILEPATH")

### Logging
LOGGER_FILEDIR:str = os.environ.get("LOGGER_FILEDIR")
TIMEZONE_NAME:str = os.environ.get("TIMEZONE_NAME")

### WebTools
PROXY_URL:str = os.environ.get("PROXIE_URL")

### NetworkTools
RELIABLE_SERVICE_HOST:str = os.environ.get("RELIABLE_SERVICE_HOST")
RELIABLE_SERVICE_PORT:int = os.environ.get("RELIABLE_SERVICE_PORT")

