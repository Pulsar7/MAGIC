<div style="text-align:center;">
    <h1>M.A.G.I.C.</h1>
    <h3>Multi-functional Assistant for General Information and Control.</h3>
    <h5><em>by Benedikt Fichtner</em></h5>
</div>

<h2>Table of contents</h2>

- [Explanation](#explanation)
- [Usage](#usage)
- [Speech Recognition](#speech-recognition)
- [Text-To-Speech](#text-to-speech)
- [Person-Database](#person-database)
- [Ctypes](#ctypes)

## Explanation



## Usage

    chmod +x run.sh && bash run.sh

If you need an overview of the program-parameters, type:

    bash run.sh --help

## Speech Recognition

In order to access the microphone and process its input the program needs the python-modules `SpeechRecognition`, `pyaudio` & `pocketsphinx`. Because of the free availablity of the Google-API, this program needs a functional internet-connection in order to use speech-recognition. <br>
You can deactivate the **Speech-Recognition** by running the script like this:

    bash run.py -ws


## Text-To-Speech

The Program uses two TTS-Modules from python:

- [Google-Text-To-Speech](https://codelabs.developers.google.com/codelabs/cloud-text-speech-python3/#0)
- [pyttsx3](https://pypi.org/project/pyttsx3/)

Because of the neccessity of a functional internet-connection while using **gTTS**, there is also another *Offline-Version* - way worse of course - that's using the python-module **pyttsx3**. 

## Person-Database

The **Person-Database** uses a *SQLITE3-Database* which is stored in the `src/dbs/`-Folder.


## Ctypes

In order to compute more efficient, `ctypes` is implemented in the *calculator*.