#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: network_tools.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""
import socket


class NETWORKTOOLS():
    def __init__(self,logger) -> None:
        (self.logger) = (logger)
        
    def get_available_interfaces(self) -> dict:
        pass
    
    def check_network_availability(self) -> bool:
        return False