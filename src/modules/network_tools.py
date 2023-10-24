#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: network_tools.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""
import socket,psutil,requests
# from scapy.all import (EtherDA)
from src.modules.tool import Tool
from src.modules.web_tools import WebTools


class NetworkTools(Tool):
    def __init__(self,reliable_service_url:str,web_tools:WebTools) -> None:
        (self.reliable_service_url) = (reliable_service_url)
        self.web_tools = web_tools
        
    def get_available_interfaces(self) -> dict:
        interfaces = psutil.net_if_addrs()
        return interfaces
    
    def check_internet_connection_availability(self) -> tuple[bool, str]:
        """Check the internet-connection availablity on current device

        Returns:
            tuple((bool,str)): Returns the status of the internet-connection availablity and then a message to output
        """
        try:
            (status,resp_text,status_code) = self.web_tools.get(url=self.reliable_service_url)
            if status == True:
                if status_code == 200:
                    return (True,f"Successfully tested the internet-connection at '{self.reliable_service_url}'")
                else:
                    return (False,f"Received status-code '{status_code}' while trying to access '{self.reliable_service_url}'")
            else:
                return (False,f"An error occured while trying to access '{self.reliable_service_url}': {resp_text}")
        except Exception as e:
            return (False,str(e))
    
    def check_ip_addr(self,ip_addr:str) -> bool:
        if "." in ip_addr:
            # IPv4-Address
            args:list[str] = ip_addr.split(".")
            if len(args) == 4:
                for arg in args:
                    try:
                        element = int(arg)
                        if element > 255:
                            raise Exception("Cannot be bigger than 255!")
                    except Exception as _e:
                        return False
                return True
        elif ":" in ip_addr:
            # IPv6-Address
            args:list[str] = ip_addr.split(":")
            ####################################################################
            ################# NOT ENOUGH #######################################
            ####################################################################
            return True
        return False
        
        
    def get_ip_addr_type(self,ip_addr:str) -> str:
        if "." in ip_addr:
            return "IPv4"
        elif ":" in ip_addr:
            return "IPv6"
        return "Invalid"
        
    def search_for_open_ports(self,ip_addr:str) -> dict:
        report:dict = {
            'ip_addr': ip_addr,
            'error': "",
            'ip_addr_type': ""
        }
        if self.check_ip_addr(ip_addr=ip_addr) == False:
            report['error'] = f"Invalid IP-Address!"
            return report
        report['ip_addr_type'] = self.get_ip_addr_type(ip_addr=ip_addr)
        
        
        return report
