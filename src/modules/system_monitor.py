#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: sytem_monitor.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""
import psutil


class SystemMonitor():
    def __init__(self,logger) -> None:
        self.logger = logger
    
    def get_all_interfaces(self) -> dict:
        return psutil.net_if_addrs()
    
    