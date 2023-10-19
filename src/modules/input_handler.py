#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: input_handler.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""



class UserInputProcessor():
    def __init__(self,logger) -> None:
        self.logger = logger
        
    def process_text(self,text:str) -> tuple[bool, str]:
        
        return (False,"Hello")