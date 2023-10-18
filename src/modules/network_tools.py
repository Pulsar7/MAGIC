#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: NetworkTools.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""
import socket,psutil,requests
# from scapy.all import (EtherDA)


class NetworkTools():
    def __init__(self,logger,reliable_service_host:str,reliable_service_port:int) -> None:
        (self.logger,self.reliable_service_host,self.reliable_service_port) = (logger,reliable_service_host,reliable_service_port)
        
    def get_available_interfaces(self) -> dict:
        interfaces = psutil.net_if_addrs()
        return interfaces
    
    def check_internet_connection_availability(self) -> tuple((bool,str)):
        """Check the internet-connection availablity on current device

        Returns:
            tuple((bool,str)): Returns the status of the internet-connection availablity and then a message to output
        """
        try:
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # TCP
            result = sock.connect_ex((self.reliable_service_host,self.reliable_service_port))
            sock.close()
            if result == 0:
                resp = requests.get("http://"+self.reliable_service_host+":"+str(self.reliable_service_port))
                if resp.status_code == 200:
                    return (True,f"Successfully tested the internet-connection at '{self.reliable_service_host}:{self.reliable_service_port}'")
                else:
                    return (False,f"Received status-code '{resp.status_code}' while trying to access '{self.reliable_service_host}:{self.reliable_service_port}'")
            else:
                return (False,f"Connection failed to: {self.reliable_service_host}:{self.reliable_service_port}")
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
