#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: input_handler.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""
import numpy


class UserInputProcessor():
    def __init__(self,logger,magic_instance) -> None:
        self.logger = logger
        self.magic_instance = magic_instance
        
    def process_text(self,text:str) -> tuple[bool, str]:
        try:
            for command in list(self.magic_instance.COMMANDS.keys()):
                if command in text:
                    return (True,self.magic_instance.COMMANDS[command]['function']())
                for other_command in self.magic_instance.COMMANDS[command]['possible_commands']:
                    if other_command in text:
                        return (True,self.magic_instance.COMMANDS[command]['function']())
            return (False,"Invalid command")
        except Exception as _error:
            return (False,str(_error))