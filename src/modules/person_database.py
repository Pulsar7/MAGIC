#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: person_database.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""
import psycopg2


class PERSON_DATABASE():
    def __init__(self,db_host:str,db_pwd:str,db_username:str,db_name:str,logger) -> None:
        self.db_params = {
            'dbname': db_name,
            'user': db_username,
            'password': db_pwd,
            'host': db_host
        }
        self.logger = logger
        
    ### WRITE / CREATE / GENERATE ###
    
    
    ### EDIT / CHANGE             ###
    
    
    ### GET / READ                ###
    
    
    ### DELETE / REMOVE           ###
    
    
    