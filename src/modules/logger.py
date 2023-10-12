#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: logger.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""
import sys,pytz
from datetime import datetime
from colorama import (Fore as f,init)
from rich import (console as cons)


init()

class LOGGER():
    def __init__(self,timezone_name:str,logger_filedir:str) -> None:
        self.timezone = pytz.timezone(timezone_name)
        self.console = cons.Console()
        self.logger_filedir:str = logger_filedir
        
    def get_now(self,date:bool=False,without_color:bool=False) -> str:
        """Get the current date & time of the specific timezone.

        Args:
            date (bool, optional): Get current date. Defaults to False.
            without_color (bool, optional): Without colorama. Defaults to False.

        Returns:
            str: Returns the current date/time as a string.
        """
        n = datetime.now(self.timezone)
        current_date:str = ""
        if date == True:
            current_date = f"<{n.day}.{n.month}.{n.year}> "
        if without_color == False:
            return f.WHITE+"("+current_date+str(n.hour)+":"+str(n.minute)+":"+str(n.second)+f.WHITE+")"+f.RESET+" "
        else:
            return "("+current_date+str(n.hour)+":"+str(n.minute)+":"+str(n.second)+") "
    
    def get_current_log_filepath(self) -> str:
        """_summary_

        Returns:
            str: Returns the current LOG-Output-Filepath.
        """
        current_date:str = self.get_now(date=True,without_color=True).strip().split(">")[0].split("<")[1]
        return self.logger_filedir+"/"+current_date+"_LOG"+".txt"
    
    def write_in_logger_file(self,log:str,log_type:str="info") -> None:
        """Writes a LOG-Message to the current LOG-File

        Args:
            log (str): The LOG-Message
            log_type (str, optional): The LOG-Type of the current line (INFO, ERROR or WARNING). Defaults to "info".
        """
        try:
            file = open(self.get_current_log_filepath(),'a')
            file.write(f"{self.get_now(date=True,without_color=True)}[{log_type.upper()}] "+log+"\n")
            file.close()
        except Exception as error:
            self.error(f"Couldn't write log-entry in logfile '{self.get_current_log_filepath()}'")
            self.error(str(error))
    
    def info(self,msg:str,progress:bool=False,write_in_file:bool=True) -> None:
        """Outputs an info-message to the CLI.

        Args:
            msg (str): Message to output
            progress (bool, optional): Print without a newline. Defaults to False.
            write_in_file (bool, optional): Write in LOG-File. Defaults to True.
        """
        if progress == False:
            print(self.get_now()+f.WHITE+"["+f.LIGHTYELLOW_EX+"INFO"+f.WHITE+"] "+f.RESET+msg)
        else:
            sys.stdout.write("\r"+self.get_now()+f.WHITE+"["+f.LIGHTYELLOW_EX+"INFO"+f.WHITE+"] "+f.RESET+msg+"...")
            sys.stdout.flush()
        if write_in_file == True:
            self.write_in_logger_file(log=msg)
            
    def error(self,msg:str,write_in_file:bool=True) -> None:
        print(self.get_now()+f.WHITE+"["+f.RED+"ERROR"+f.WHITE+"] "+f.LIGHTRED_EX+msg)
        if write_in_file == True:
            self.write_in_logger_file(log=msg,log_type="error")
    
    def warning(self,msg:str,write_in_file:bool=True) -> None:
        print(self.get_now()+f.WHITE+"["+f.YELLOW+"WARNING"+f.WHITE+"] "+f.YELLOW+msg)
        if write_in_file == True:
            self.write_in_logger_file(log=msg,log_type="warning")
        
    def success(self,msg:str="") -> None:
        if len(msg) > 0:
            print(f.LIGHTGREEN_EX+msg+f.RESET)
        else:
            print(f.LIGHTBLACK_EX+"O.K."+f.RESET)
            
    def failed(self,msg:str="") -> None:
        if len(msg) > 0:
            print(f.LIGHTRED_EX+msg+f.RESET)
        else:
            print(f.LIGHTRED_EX+"FAILED"+f.RESET)