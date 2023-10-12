#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: web_tools.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""
import requests,fake_headers



class WEBTOOLS():
    def __init__(self,logger,proxies:dict) -> None:
        (self.logger) = (logger)
        self.proxies:dict = proxies
    
    def create_new_session(self,use_proxy:bool) -> requests.Session:
        session = requests.Session()
        session.proxies = self.proxies
        session.headers = fake_headers.firefox
        return session
    
    def get(self,url:str,use_proxy:bool=False) -> tuple((bool,object)):
        try:
            session = self.create_new_session(use_proxy)
            return (True,)
        except Exception as error:
            return (False,str(error))