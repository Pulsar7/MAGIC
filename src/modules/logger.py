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
from rich.tree import Tree
from rich import print as rprint


init()

class LOGGER():
    def __init__(self,timezone_name:str,logger_filedir:str,speaker,speak_to_me_status:bool) -> None:
        self.timezone = pytz.timezone(timezone_name)
        self.console = cons.Console()
        self.logger_filedir:str = logger_filedir
        self.speaker = speaker
        self.speak_to_me_status:bool = speak_to_me_status
        
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
        """Get current LOG-filepath.

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
    
    def info(self,msg:str,progress:bool=False,write_in_file:bool=True,say:bool=False,cli_output:bool=True) -> None:
        """
        
        """    
        if progress == False and cli_output == True:
            print(self.get_now()+f.WHITE+"["+f.LIGHTYELLOW_EX+"INFO"+f.WHITE+"] "+f.RESET+msg)
        elif progress == True and cli_output == True:
            sys.stdout.write("\r"+self.get_now()+f.WHITE+"["+f.LIGHTYELLOW_EX+"INFO"+f.WHITE+"] "+f.RESET+msg+"...")
            sys.stdout.flush()
        if write_in_file == True:
            self.write_in_logger_file(log=msg)
        if say == True and self.speak_to_me_status == True:
            self.speaker.say(msg)
            
    def error(self,msg:str,write_in_file:bool=True,say:bool=False,cli_output:bool=True) -> None:
        if cli_output == True:
            print(self.get_now()+f.WHITE+"["+f.RED+"ERROR"+f.WHITE+"] "+f.LIGHTRED_EX+msg+f.RESET)
        if write_in_file == True:
            self.write_in_logger_file(log=msg,log_type="error")
        if say == True and self.speak_to_me_status == True:
            self.speaker.say("ERROR: "+msg)
    
    def warning(self,msg:str,write_in_file:bool=True,say:bool=False,cli_output:bool=True) -> None:
        if cli_output == True:
            print(self.get_now()+f.WHITE+"["+f.YELLOW+"WARNING"+f.WHITE+"] "+f.YELLOW+msg+f.RESET)
        if write_in_file == True:
            self.write_in_logger_file(log=msg,log_type="warning")
        if say == True and self.speak_to_me_status == True:
            self.speaker.say("WARNING: "+msg)
        
    def success(self,msg:str="") -> None:
        if len(msg) > 0:
            print(f.LIGHTGREEN_EX+msg+f.RESET)
        else:
            print(f.LIGHTGREEN_EX+"O.K."+f.RESET)
            
    def failed(self,msg:str="") -> None:
        if len(msg) > 0:
            print(f.LIGHTRED_EX+msg+f.RESET)
        else:
            print(f.LIGHTRED_EX+"FAILED"+f.RESET)
            
    def found(self,msg:str,brackets_text:str="+",write_in_file:bool=True) -> None:
        """_summary_

        Args:
            msg (str): The output-msg
            brackets_text (str, optional): Object before message. Defaults to "+".
            write_in_file (bool, optional): Write in LOG-File. Defaults to True.
        """
        print(self.get_now()+f.WHITE+"["+f.LIGHTBLUE_EX+brackets_text+f.WHITE+"] "+f.WHITE+msg+f.RESET)
        if write_in_file == True:
            self.write_in_logger_file(log=msg) # LOG as 'info'
            
    def colored_input(self) -> str:
        return input(f.WHITE+"#"+f.YELLOW+"$"+f.LIGHTGREEN_EX+"> "+f.RESET)