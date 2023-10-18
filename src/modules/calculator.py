#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: calculator.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""
import ctypes


class CALCULATOR():
    def __init__(self,logger) -> None:
        (self.logger) = (logger)
        #
        self.c_files:dict = {
            'check_if_prime_number': "src/c_src/check_if_prime_number.so"
        }
        #
    
    def check_if_number_is_prime_number(self,number:int) -> bool:
        myc = ctypes.CDLL(self.c_files['check_if_prime_number'])
        if myc.check(number) == 1:
            return True
        else:
            return False
    