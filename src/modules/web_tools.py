#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: web_tools.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""
import requests
from src.modules.tool import Tool
from fake_headers import Headers


class WebTools(Tool):
    def __init__(self,proxies:dict,request_timeout:float) -> None:
        self.proxies:dict = proxies
        self.request_timeout:float = request_timeout
    
    def create_new_session(self,use_proxy:bool) -> requests.Session:
        session = requests.Session()
        if use_proxy:
            session.proxies = self.proxies
        session.headers = Headers(headers=False).generate()
        return session
    
    def get(self,url:str,use_proxy:bool=False) -> tuple[bool,str,int]:
        """HTTP-GET-Request with the 'requests' module

        Returns:
            tuple[bool,str,int]: Returns a status (if an exception occured or not) and the requests-response
        """
        try:
            session = self.create_new_session(use_proxy)
            resp = session.get(url,timeout=self.request_timeout)
            session.close()
            return (True,"",resp.status_code)
        except Exception as _error:
            return (False,str(_error),000)
        
    def post(self,url:str,data:dict,use_proxy:bool=False) -> tuple[bool,str,int]:
        """HTTP-POST-Request with the 'requests' module

        Returns:
            tuple[bool,str,int]: Returns a status (if an exception occured or not) and the requests-response
        """
        try:
            session = self.create_new_session(use_proxy)
            resp = session.post(url=url,data=data)
            session.close()
            return (True,"",resp.status_code)
        except Exception as _error:
            return (False,str(_error),000)
        