#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: network_tools.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""
import socket,psutil,requests
# from scapy.all import (EtherDA)


class NETWORKTOOLS():
    def __init__(self,logger,reliable_service_host:str,reliable_service_port:int) -> None:
        (self.logger,self.reliable_service_host,self.reliable_service_port) = (logger,reliable_service_host,reliable_service_port)
        
    def get_available_interfaces(self) -> dict:
        interfaces = psutil.net_if_addrs()
        return interfaces
    
    def check_network_availability(self) -> tuple((bool,str)):
        """Check the network availablity on current device

        Returns:
            tuple((bool,str)): Returns the status of the network availablity and then a message to output
        """
        try:
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # TCP
            result = sock.connect_ex((self.reliable_service_host,self.reliable_service_port))
            sock.close()
            if result == 0:
                resp = requests.get("http://"+self.reliable_service_host+":"+str(self.reliable_service_port))
                if resp.status_code == 200:
                    return (True,f"Successfully tested the network connection at '{self.reliable_service_host}:{self.reliable_service_port}'")
                else:
                    return (False,f"Received status-code '{resp.status_code}' while trying to access '{self.reliable_service_host}:{self.reliable_service_port}'")
            else:
                return (False,f"Connection failed to: {self.reliable_service_host}:{self.reliable_service_port}")
        except Exception as e:
            return (False,str(e))