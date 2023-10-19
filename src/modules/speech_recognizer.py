#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: SpeechRecognizer.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""
import speech_recognition as sr
import pyaudio


class SpeechRecognizer():
    def __init__(self,logger) -> None:
        (self.logger) = (logger)
        self.recognizer = sr.Recognizer()
    
    def capture_microphone(self) -> tuple[bool, str]:
        """Capturing the microphone in order to convert it into text. (Using Google-API)

        Raises:
            Exception: Couldn't understand any of the audio.
            Exception: Web-API-Request-error.

        Returns:
            tuple((bool,str)): Returns the status and (if any recognized) the text.
        """
        try:
            self.logger.info("Listening to microphone",progress=True)
            with sr.Microphone(device_index=0) as source:
                audio = self.recognizer.listen(source)
            try:
                recognized_text = str(self.recognizer.recognize_google(audio))
            except sr.UnknownValueError:
                raise Exception("Google Web Speech API could not understand the audio.")
            except sr.RequestError as e:
                raise Exception(f"Could not get request results from Google Web Speech API; {e}")
            except OSError as e:
                raise Exception(f"OS-Error: {e}")
            self.logger.success()
            return (True,recognized_text)
        except Exception as error:
            self.logger.failed()
            return (False,"An error occured while Speech-Recognition: "+str(error))
    
    
    