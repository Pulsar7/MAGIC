#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: calculator.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""
import array
import ctypes


class CALCULATOR():
    def __init__(self,logger) -> None:
        (self.logger) = (logger)
        #
        self.c_files:dict = {
            'check_if_prime_number': "src/c_src/check_if_prime_number.so",
            'matrices_calculator': "src/c_src/matrices_calcs.so"
        }
        #
    
    def check_if_number_is_prime_number(self,number:int) -> bool:
        myc = ctypes.CDLL(self.c_files['check_if_prime_number'])
        if myc.check(number) == 1:
            return True
        else:
            return False
        
    def multiply_matrices(self,matrix_A,matrix_B) -> list[object]:
        myc = ctypes.CDLL(self.c_files['check_if_prime_number'])
        if len(matrix_A) == len(matrix_B):
            
            # if integer-matrices
            array1 = (ctypes.c_int * len(matrix_A))(a for a in matrix_A)
            array2 = (ctypes.c_int * len(matrix_A))(b for b in matrix_B)    
            result_matrix = myc.multiply_integer_matrices(array1,array2,len(matrix_A))
            

        return ["Both should have the same length"]
    