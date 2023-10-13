#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: speaker.py
Author: Benedikt Fichtner
Python-Version: 3.10.12
"""
from gtts import gTTS
import tempfile
from playsound import playsound
from pydub import AudioSegment


class SPEAKER():
    def __init__(self) -> None:
        pass
        
    def say(self,text:str) -> None:
        # Create a temporary audio file to store the speech
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as temp_audio:
            tts = gTTS(text, lang="en-uk",slow=False)
            tts.save(temp_audio.name)
            # Play the audio file
            audio = AudioSegment.from_mp3(temp_audio.name)
            adjusted_audio = audio.speedup(playback_speed=1.45)
            adjusted_audio.export(temp_audio.name, format="mp3")
            playsound(sound=temp_audio.name)
        