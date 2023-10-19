#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: web_tools.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""
import requests,fake_headers


class WebTools():
    def __init__(self,logger,proxies:dict) -> None:
        (self.logger) = (logger)
        self.proxies:dict = proxies
    
    def create_new_session(self,use_proxy:bool) -> requests.Session:
        session = requests.Session()
        if use_proxy:
            session.proxies = self.proxies
        # session.headers = fake_headers.firefox ! NO FAKE HEADERS
        return session
    
    def get(self,url:str,use_proxy:bool=False) -> tuple[bool, object]:
        """HTTP-GET-Request with the 'requests' module

        Returns:
            tuple((bool,object)): Returns a status (if an exception occured or not) and the requests-response
        """
        try:
            session = self.create_new_session(use_proxy)
            resp = session.get(url)
            session.close()
            return (True,resp)
        except Exception as _error:
            return (False,str(_error))
        
    def post(self,url:str,data:dict,use_proxy:bool=False) -> tuple[bool, object]:
        """HTTP-POST-Request with the 'requests' module

        Returns:
            tuple((bool,object)): Returns a status (if an exception occured or not) and the requests-response
        """
        try:
            session = self.create_new_session(use_proxy)
            resp = session.post(url=url,data=data)
            session.close()
            return (True,resp)
        except Exception as _error:
            return (False,str(_error))