#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: osint_tool.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""
from src.modules.tool import Tool
from src.modules.person_database import PersonDatabase


class OsintTool(Tool):
    def __init__(self,person_db:PersonDatabase) -> None:
        self.person_db = person_db
    
    