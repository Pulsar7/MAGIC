#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: speaker.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""
from gtts import gTTS
import tempfile,pyttsx3,time
from playsound import playsound
from pydub import AudioSegment


class SPEAKER():
    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        self.use_offline_tts:bool = False
        self.currently_speaking:bool = False
        self.seconds_to_wait_until_next_speak_attempt:float = 0.5
        
    def say(self,text:str) -> None:
        """Uses two Text-To-Speech-Modules in order to speak text.

        Args:
            text (str): The text to speak.
        """
        if self.currently_speaking == False:
            self.currently_speaking = True # Speaking is now blocked until this text is finished
            if self.use_offline_tts == False: # ONLINE-Mode
                # Create a temporary audio file to store the speech
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as temp_audio:
                    tts = gTTS(text, lang="en-uk",slow=False)
                    tts.save(temp_audio.name)
                    # Play the audio file
                    audio = AudioSegment.from_mp3(temp_audio.name)
                    adjusted_audio = audio.speedup(playback_speed=1.45)
                    adjusted_audio.export(temp_audio.name, format="mp3")
                    playsound(sound=temp_audio.name)
            else: # OFFLINE-Mode
                self.engine.setProperty('voice', 'english')
                self.engine.setProperty('rate', 150)  # Speed of speech
                self.engine.setProperty('volume', 1.0)
                self.engine.say(text)
                self.engine.runAndWait()
            self.currently_speaking = False
        else:
            time.sleep(self.seconds_to_wait_until_next_speak_attempt) # Waits
            self.say(text)