#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: speech_recognizer.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""
import speech_recognition as sr


class SPEECH_RECOGNIZER():
    def __init__(self,logger) -> None:
        (self.logger) = (logger)
        self.recognizer = sr.Recognizer()
    
    def capture_microphone(self) -> tuple((bool,str)):
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source)
            try:
                recognized_text = self.recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                raise Exception("Google Web Speech API could not understand the audio.")
            except sr.RequestError as e:
                raise Exception(f"Could not request results from Google Web Speech API; {e}")
            return (True,recognized_text)
        except Exception as error:
            return (False,str(error))
    
    
    