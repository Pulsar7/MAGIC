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
from src.modules.speech_recognizer import SPEECH_RECOGNIZER
from src.modules.speaker import SPEAKER
#


class MAGIC():
    def __init__(self,logger:LOGGER,person_db:PERSON_DATABASE,webtools:WEBTOOLS,wifitools:WIFITOOLS,networktools:NETWORKTOOLS,speech_recognizer:SPEECH_RECOGNIZER,use_speech_recognition:bool,speaker:SPEAKER) -> None:
        (self.logger,self.person_db,self.webtools,
            self.wifitools,self.networktools,self.speech_recognizer,self.speaker) = (logger,person_db,webtools,wifitools,networktools,speech_recognizer,speaker)
        # Status-Variables
        self.network_availability:bool = False
        self.use_speech_recognition:bool = use_speech_recognition
        self.running:bool = True
        self.COMMANDS:dict = { ################################ ?
            'help': {
                'possible_commands': ["hilfe","help me"],
                'desrc': "Shows all possible commands"
            },
            'exit': {
                'possible_commands': ["close","quit"],
                'descr': "Closes the program"
            }
        }
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
    
    def check_all(self) -> bool:
        """Checks all available tools and services.

        Returns:
            bool: Return a Boolean in order to return the operation status after the "CheckUp".
        """
        self.logger.console.rule()
        self.logger.info("Started Complete-Checkup")
        self.logger.info(f"Current-Logger-Filepath: '{self.logger.get_current_log_filepath()}'",write_in_file=False)
        # Get interfaces
        available_interfaces:dict = self.networktools.get_available_interfaces()
        self.logger.info(f"I can register {len(list(available_interfaces.keys()))} available interfaces")
        for iface in available_interfaces:
            self.logger.found(msg=iface,write_in_file=False)
        # Check internet-connection
        self.logger.info("Checking the internet-connection-availablity",progress=True)
        (netw_avail_status,resp) = self.networktools.check_internet_connection_availability()
        if netw_avail_status:
            self.logger.success()
            self.logger.info(resp)
            self.network_availability = True
        else:
            self.logger.failed()
            self.logger.error(resp)
            self.logger.warning("Looks like I have no available internet-connection!")
        # Check person-database
        self.logger.info("Check PersonDB-Filepath",progress=True)
        if self.person_db.check_db_filepath():
            self.logger.success()
        else:
            self.logger.failed()
            self.logger.error("Please check the Person-Database filepath!")
            self.running = False
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
        if self.check_all(): # All tools/services are probably good.
            self.logger.info("Checked all services",say=True,cli_output=False)
            if self.network_availability == False:
                self.logger.warning("Cannot use Speech-Recognition without an internet-connection!",say=True)
                self.use_speech_recognition = False
            elif self.use_speech_recognition == False:
                self.logger.warning("Not using Speech-Recognition",say=True)
            if self.running == True:
                self.person_db.create_connection()
                self.logger.info("Creating/Checking PersonDB-Tables",progress=True)
                (status,resp) = self.person_db.create_tables()
                if status == True:
                    self.logger.success()
                    self.logger.info(resp)
                else:
                    self.logger.failed()
                    self.logger.error(resp)
                    self.running = False
            else:
                self.logger.warning("Skipped creating/checking the PersonDB-Tables")
            ###### MAIN-Loop ######
            errors:int = 0
            user_input:str = ""
            while (self.running):
                try:
                    try:
                        if self.use_speech_recognition == True:
                            (status,text) = self.speech_recognizer.capture_microphone()
                            if status == True:
                                user_input = text
                            else:
                                self.logger.error(text)
                                errors += 1
                        else:
                            user_input:str = self.logger.colored_input()
                        self.logger.info(f"Sorry but I didn't understand '{user_input}'",say=True,cli_output=False,write_in_file=False)
                        ###############################################################
                        self.running = False #######!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        ###############################################################
                        #### HANDLE USER INPUT!
                        if errors >= 5:
                            self.logger.error("Too many errors!",say=True)
                            self.running = False
                    except KeyboardInterrupt:
                        raise Exception("Detected Keyboard-Interruption")
                except Exception as _error:
                    self.logger.error(f"An error occured: {str(_error)}")
                    self.running = False
            ######
        self.logger.info(f"Closed. (Runtime={time.time()-start} Seconds)")
        self.person_db.close_conn()
        
        

####### ArgumentParser
parser = argparse.ArgumentParser(description="M.A.G.I.C.")
speaker_group = parser.add_argument_group(title="Speaker",description="Configure the Speaker")
speaker_group.add_argument(
    '-s','--speak-to-me',help=f"Speak to me with a voice",
    action="store_true",default=False
)

speech_recognition_group = parser.add_argument_group(title="Speech Recognition",description="Configure the Speech-Recognizer")
speech_recognition_group.add_argument(
    '-ws','--without-speech-recognition',help="Deactivates the speech-recognizer.",
    action="store_true",default=False
)

logger_group = parser.add_argument_group(title="LOGGER",description="Configure the LOGs")
logger_group.add_argument(
    '-l','--logger-filedir',help=f"The LOG-File-Directory (Default={LOGGER_FILEDIR})",
    type=str,default=LOGGER_FILEDIR
)
logger_group.add_argument(
    '-t','--timezone',help=f"Timezone-name (Default={TIMEZONE_NAME})",
    type=str,default=TIMEZONE_NAME
)

networktools_group = parser.add_argument_group(title="NetworkTools",description="Configure NetworkTools")
networktools_group.add_argument(
    '-rh','--reliable-service-host',help=f"Reliable service HOST (Default={RELIABLE_SERVICE_HOST})",
    type=str,default=RELIABLE_SERVICE_HOST
)
networktools_group.add_argument(
    '-rp','--reliable-service-port',help=f"Reliable service PORT (Default={RELIABLE_SERVICE_PORT})",
    type=int,default=RELIABLE_SERVICE_PORT
)

webtools_group = parser.add_argument_group(title="WebTools",description="Configure WebTools")
webtools_group.add_argument(
    '-sp','--socks-proxy-url',help=f"Socks-Proxy-URL (Default={PROXY_URL})",
    type=str,default=PROXY_URL
)

args = parser.parse_args()
#######

# Speaker
speaker = SPEAKER()
# Logger
logger = LOGGER(timezone_name=args.timezone,logger_filedir=args.logger_filedir,speaker=speaker,speak_to_me_status=args.speak_to_me)
# Person-Database
person_db = PERSON_DATABASE(
    db_filepath=PERSON_DB_FILEPATH,
    logger=logger
)
# WebTools
webtools = WEBTOOLS(
    logger=logger,
    proxies={
        'http':args.socks_proxy_url,
        'https':args.socks_proxy_url,
        'socks5':args.socks_proxy_url
    }
)
# WifiTools
wifitools = WIFITOOLS(
    logger=logger
)
# NetworkTools
networktools = NETWORKTOOLS(
    logger=logger,
    reliable_service_host=args.reliable_service_host,
    reliable_service_port=args.reliable_service_port
)
# SpeechRecognizer
speech_recognizer = SPEECH_RECOGNIZER(
    logger=logger
)

if __name__ == '__main__':
    magic = MAGIC(
        person_db=person_db,
        logger=logger,
        webtools=webtools,
        wifitools=wifitools,
        networktools=networktools,
        speech_recognizer=speech_recognizer,
        use_speech_recognition=not args.without_speech_recognition,
        speaker=speaker
    )
    magic.run()