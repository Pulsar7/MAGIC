#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: magic.py
Author: Benedikt Fichtner
Python-Version: 3.10.12

@Multi-functional Assistant for General Information and Control
"""
import os,time,argparse
from settings import * # load local-environmet variables/default variables
from src.modules.logger import LOGGER
from src.modules.person_database import PersonDatabase
from src.modules.web_tools import WebTools
from src.modules.wifi_tools import WifiTools
from src.modules.network_tools import NetworkTools
from src.modules.speech_recognizer import SpeechRecognizer
from src.modules.speaker import SPEAKER
from src.modules.calculator import CALCULATOR
from src.modules.input_handler import UserInputProcessor
from src.modules.system_monitor import SystemMonitor
from src.modules.osint_tool import OsintTool


class MAGIC():
    def __init__(self,logger:LOGGER,person_db:PersonDatabase,web_tools:WebTools,wifi_tools:WifiTools,networktools:NetworkTools,speech_recognizer:SpeechRecognizer,use_speech_recognition:bool,speaker:SPEAKER,calc:CALCULATOR,osint_tool:OsintTool) -> None:
        self.logger = logger
        self.person_db = person_db
        self.web_tools = web_tools
        self.wifi_tools = wifi_tools
        self.networktools = networktools
        self.speech_recognizer = speech_recognizer
        self.speaker = speaker
        self.calc = calc
        self.osint_tool = osint_tool
        # Status-Variables
        self.network_availability:bool = False
        self.use_speech_recognition:bool = use_speech_recognition
        self.running:bool = True
        self.COMMANDS:dict = {
            'help': {
                'possible_commands': ["commands"],
                'descr': "Shows all possible commands",
                'function': self.show_help
            },
            
            'exit': {
                'possible_commands': ["close","quit"],
                'descr': "Closes the program",
                'function': self.close_program
            },
            
            'search for network': {
                'possible_commands': ["scan for specific network"],
                'descr': "Scans for a specific network in your area",
                'function': self.search_for_specific_network
            }
        }
        self.errors:int = 0
        #
        self.user_input_processor = UserInputProcessor(logger=logger,magic_instance=self)
        
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
        self.logger.info(f"Timeout for HTTP-GET and HTTP-POST requests: {self.web_tools.request_timeout} Seconds")
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
            self.speaker.use_offline_tts = True # Not using GTTS
        # Check person-database
        self.logger.info("Check PersonDB-Filepath",progress=True)
        if self.person_db.check_db_filepath():
            self.logger.success()
        else:
            self.logger.failed()
            self.logger.error("Please check the Person-Database filepath!")
            self.running = False
        self.logger.info("Finished Complete-Checkup",write_in_file=False)
        self.logger.console.rule()
        return True
    
    ###### Command - Functions ######
    
    
    def close_program(self) -> str:
        """Closes the program.

        Returns:
            str: Returns a response as String.
        """
        self.running = False
        return "User sent the exit-signal."
    
    def show_help(self) -> str:
        """Shows help-message

        Returns:
            str: Returns a response as String.
        """
        all_commands_overview:str = "All available commands:\n "
        for command in self.COMMANDS:
            all_commands_overview += f"""\
                '{command}' {self.COMMANDS[command]['descr'][0].lower()+self.COMMANDS[command]['descr'][1:]}
                But you can also type or say the following commands: {';'.join(self.COMMANDS[command]['possible_commands'])}\n
            """
        self.logger.info(msg=all_commands_overview,write_in_file=False,say=True,cli_output=False)
        self.logger.console.print(self.COMMANDS)
        return "Showed all available commands."
    
    def search_for_specific_network(self) -> str:
        cli_input_append_text:str = "SearchForNetwork"
        self.logger.info("Do you want to search for a specific BSSID or a SSID?",say=True,write_in_file=False)
        time.sleep(3) # waits for 3 seconds
        user_input:str = self.get_user_input(cli_input_append_text)
        bssid_keywords:list[str] = ["bssid", "basic service set identifier"]
        ssid_keywords:list[str] = ["ssid", "service set identifier"]
        if len(user_input) > 0:
            user_input = user_input.lower().strip()
            if any(keyword in user_input for keyword in bssid_keywords):
                target_bssid:str = ""
                args:list[str] = []
                for keyword in bssid_keywords:
                    if keyword in user_input:
                        args = user_input.split(keyword)
                        break
                if len(args) > 1 and len(args[1]) > 0:
                    target_bssid = args[1]
                else:
                    self.logger.info("Please tell me the specific BSSID-Address",say=True,write_in_file=False)
                    user_input:str = self.get_user_input(cli_input_append_text)
                    if len(user_input) > 0:
                        target_bssid = user_input
                    else:
                        self.logger.info("Sorry, but I need the BSSID of the network",say=True)
                        return ""
                ######################
                # CHECK TARGET-BSSID #
                ######################
            if any(keyword in user_input for keyword in ssid_keywords):
                target_ssid:str = ""
                args:list[str] = []
                for keyword in ssid_keywords:
                    if keyword in user_input:
                        args = user_input.split(keyword)
                        break
                if len(args) > 1:
                    target_ssid = args[1]
                else:
                    self.logger.info("Please tell me the specific SSID",say=True,write_in_file=False)
                    user_input:str = self.get_user_input()
                    if len(user_input) > 0:
                        target_ssid = user_input
                    else:
                        self.logger.info("Sorry, but I need the SSID of the network",say=True)
                        return ""
                #####################
                # CHECK TARGET-SSID #
                #####################
            if any(keyword in user_input for keyword in ["break", "close", "abort"]):
                self.logger.info("Aborted the search for a specific network",say=True)
        else:
            pass
        return ""
    
    
    ######                     ######
    
    def get_user_input(self,cli_input_append_text:str="") -> str:
        """Captures a microphone or reads the CLI-Input.

        Args:
            cli_input_append_text (str): Text before the CLI-Input. Defaults to "".

        Returns:
            str: Returns the user-input-text as a string
        """
        user_input:str = ""
        if self.use_speech_recognition == True:
            (status,text) = self.speech_recognizer.capture_microphone()
            if status == True:
                user_input = text
            else:
                self.logger.error(text)
                self.errors += 1
        else:
            user_input:str = self.logger.colored_input(cli_input_append_text)
        return user_input
    
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
                self.logger.warning("Cannot use Google-Text-To-Speech without an internet-connection!",say=True)
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
            user_input:str = ""
            while (self.running):
                try:
                    try:
                        user_input:str = self.get_user_input()
                        if len(user_input) > 0:
                            (status,resp) = self.user_input_processor.process_text(text=user_input)
                            if status == True:
                                if len(resp) > 0:
                                    self.logger.info(resp)
                            else:
                                self.errors += 1
                                if "invalid command" not in resp.lower():
                                    self.logger.error("An error occured while trying to process user-input",say=True)
                                    self.logger.error(resp) # If the error is complex, the text-to-speech-engine shouldn't say that.
                                else:
                                    self.logger.error(resp,say=True,write_in_file=False)
                        if self.errors >= 5:
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
    '-ru','--reliable-service-url',help=f"Reliable service-URL (Default={RELIABLE_SERVICE_URL})",
    type=str,default=RELIABLE_SERVICE_URL
)

WebTools_group = parser.add_argument_group(title="WebTools",description="Configure WebTools")
WebTools_group.add_argument(
    '-sp','--socks-proxy-url',help=f"Socks-Proxy-URL (Default={PROXY_URL})",
    type=str,default=PROXY_URL
)
WebTools_group.add_argument(
    '-wt','--web-request-timeout',help=f"Timeout in seconds for HTTP-GET & HTTP-POST requests (Default={WEB_REQUEST_TIMEOUT})",
    type=str,default=WEB_REQUEST_TIMEOUT
)

args = parser.parse_args()
#######

# Speaker
speaker = SPEAKER()
# Logger
logger = LOGGER(timezone_name=args.timezone,logger_filedir=args.logger_filedir,speaker=speaker,speak_to_me_status=args.speak_to_me)
# Person-Database
person_db = PersonDatabase(
    db_filepath=PERSON_DB_FILEPATH,
    logger=logger
)
# SystemMonitor
system_monitor = SystemMonitor(
    logger=logger
)
# WebTools
web_tools = WebTools(
    proxies={
        'http':args.socks_proxy_url,
        'https':args.socks_proxy_url,
        'socks5':args.socks_proxy_url
    },
    request_timeout=args.web_request_timeout
)
# WifiTools
wifi_tools = WifiTools()
# NetworkTools
networktools = NetworkTools(
    reliable_service_url=args.reliable_service_url,
    web_tools=web_tools
)
# SpeechRecognizer
speech_recognizer = SpeechRecognizer(
    logger=logger
)
# Calculator
calc = CALCULATOR(
    logger=logger
)
# OSINT-Tool
osint_tool = OsintTool(
    person_db=person_db
)

if __name__ == "__main__":
    magic = MAGIC(
        person_db=person_db,
        logger=logger,
        web_tools=web_tools,
        wifi_tools=wifi_tools,
        networktools=networktools,
        speech_recognizer=speech_recognizer,
        use_speech_recognition=not args.without_speech_recognition,
        speaker=speaker,
        calc=calc,
        osint_tool=osint_tool
    )
    magic.run()