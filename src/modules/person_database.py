#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: PersonDatabase.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""
import sqlite3,random,string


class PersonDatabase():
    def __init__(self,logger,db_filepath:str) -> None:
        (self.logger,self.db_filepath) = (logger,db_filepath)
        #
        self.tables:dict = {
            'persons': {
                'values': [
                    "person_id TEXT",
                    "firstname TEXT","surname TEXT","birthdate TEXT",
                    "emails TEXT","phones TEXT"
                ]
            }
        }
        self.conn = ""
        self.cursor = ""
        self.person_id_len:int = 35
        self.persons_table_name:str = list(self.tables.keys())[0]
        #
        
    def check_db_filepath(self) -> bool:
        try:
            conn = sqlite3.connect(self.db_filepath)
            conn.close()
        except Exception as _e:
            return False
        return True
    
    def create_connection(self) -> None:
        self.conn = sqlite3.connect(self.db_filepath)
        self.cursor = self.conn.cursor()    
        
    def close_conn(self) -> None:
        try:
            self.conn.close()
            self.logger.info("Closed PersonDatabase-Connection",say=True)
        except Exception as _e:
            self.logger.error(f"Couldn't close PersonDB-connection: {str(_e)}")
        
    ### WRITE / CREATE / GENERATE ###
    def generate_person_id(self) -> str:
        max_counter:int = 1000
        counter:int = 0
        while True:
            counter += 1
            generated_id:str = ""
            for i in range(0,self.person_id_len):
                if random.choice([0,1]) == 0:
                    generated_id += str(random.randint(0,9))
                else:
                    generated_id += random.choice(string.ascii_letters)
            if self.check_if_person_id_exists(person_id=generated_id) == False:
                break
            elif counter == max_counter:
                self.logger.error("Something went wrong while trying to generate person-id!")
                generated_id = "Error_#ID"
                break
        return generated_id
            
    
    def create_tables(self) -> tuple((bool,str)):
        """Create all tables.

        Returns:
            tuple((bool,str)): Returns the status (if the tables could be created) and a message.
        """
        try:
            for table in list(self.tables.keys()):    
                self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table}({','.join(self.tables[table]['values'])});")
                self.conn.commit()
            return (True,f"Created all {len(list(self.tables.keys()))} tables")
        except Exception as _e:
            return (False,str(_e))
    
    ### EDIT / CHANGE             ###
    
    
    
    ### GET / READ                ###
    def check_if_person_id_exists(self,person_id:str) -> bool:
        try:
            self.cursor.execute(f"SELECT * FROM {self.persons_table_name} WHERE person_id=?;",(
                person_id,
            ))
            persons = self.cursor.fetchall()
            self.conn.commit()
            if len(persons) > 0:
                return True
            else:
                return False
        except Exception as _e:
            self.logger.error(f"An error occured while trying to check if person-id exists: {str(_e)}")
            return True
    
    
    ### DELETE / REMOVE           ###
    
    
    