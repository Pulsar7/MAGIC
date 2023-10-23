#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: wifi_tools.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""
# from scapy.all import (Ether,ARP)
from src.modules.tool import Tool

class WifiTools(Tool):
    def __init__(self) -> None:
        pass
        
    def get_wifi_able_interfaces(self) -> dict:
        all_interfaces:dict = self.system_monitor.get_all_interfaces()
        wifi_ifaces:dict = {}
        for iface in all_interfaces:
            pass
        return wifi_ifaces
    
    