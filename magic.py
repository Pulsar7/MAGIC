#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: magic.py
Author: Benedikt Fichtner
Python-Version: 3.10.12

@Multi-functional Assistant for General Information and Control
"""
import os,time,argparse
# own modules
from settings import * # load settings for database,logger,...
from src.modules.logger import LOGGER
from src.modules.person_database import PERSON_DATABASE
from src.modules.web_tools import WEBTOOLS
from src.modules.wifi_tools import WIFITOOLS
from src.modules.network_tools import NETWORKTOOLS
#


class MAGIC():
    def __init__(self,logger,person_db,webtools,wifitools,networktools) -> None:
        (self.logger,self.person_db,self.webtools,
            self.wifitools,self.networktools) = (logger,person_db,webtools,wifitools,networktools)
        #
        #
        
    def get_os(self) -> str:
        """
        Get the OS-Name
        Returns:
            str: Returns the possible name of the current OS
        """
        if os.name == 'posix':
            system_name = "Unix-Based"
        elif os.name == 'nt':
            system_name = "Windows"
        else:
            system_name = "Unknown"
        return system_name
    
    def clear_screen(self) -> None:
        """
            Clears the CLI
        """
        os_name:str = self.get_os()
        if "unix" in os_name.lower():
            os.system('clear')
        elif "windows" in os_name.lower():
            os.system("cls")
        else:
            print('\n' * 100)  # A simple alternative for other system
        
    def check_if_root(self) -> bool:
        return os.geteuid() == 0
    
    def check_all(self) -> bool:
        """Checks all available tools and services.

        Returns:
            bool: Return a Boolean in order to return the operation status after the "CheckUp".
        """
        self.logger.console.rule()
        self.logger.info("Started ALL-Checkup")
        self.logger.info(f"Current-Logger-Filepath: '{self.logger.get_current_log_filepath()}'",write_in_file=False)
        self.logger.info("Checking root-permissions",progress=True)
        if self.check_if_root():
            self.logger.ok()
        else:
            self.logger.failed()
            self.logger.error("I need root-priviliges in order to operate properly!")
            # return False
        self.logger.info("Checking the network-availablity",progress=True)
        if self.networktools.check_network_availability():
            self.logger.success()
        else:
            self.logger.failed()
            self.logger.warning("Looks like I have no available internet-connection!")
        self.logger.console.rule()
        return True
    
    def run(self) -> None:
        """
            The RUN-Method where the program starts.
        """
        self.clear_screen()
        self.logger.info("Started.")
        self.logger.info(f"Running on a {self.get_os()}-System ({os.name})")
        start:float = time.time()
        
        ### Start procedure
        if self.check_all():
            pass
        ###
        self.logger.info(f"Closed. (Runtime={time.time()-start} Seconds)")
        
        

# ArgumentParser
parser = argparse.ArgumentParser()
"""parser.add_argument(
    '-l','--logger_filepath'
)"""
args = parser.parse_args()

# Logger
logger = LOGGER(timezone_name=TIMEZONE_NAME,logger_filedir=LOGGER_FILEDIR)
# Person-Database
person_db = PERSON_DATABASE(
    db_host=PERSON_DB_HOST,db_pwd=PERSON_DB_PWD,db_username=PERSON_DB_USER,db_name=PERSON_DB_NAME,
    logger=logger
)
# WebTools
webtools = WEBTOOLS(
    logger=logger,
    proxies={
        'http':PROXIE_URL,
        'https':PROXIE_URL,
        'socks5':PROXIE_URL
    }
)
# WifiTools
wifitools = WIFITOOLS(
    logger=logger
)
# NetworkTools
networktools = NETWORKTOOLS(
    logger=logger
)

if __name__ == '__main__':
    magic = MAGIC(
        person_db=person_db,
        logger=logger,
        webtools=webtools,
        wifitools=wifitools,
        networktools=networktools
    )
    magic.run()