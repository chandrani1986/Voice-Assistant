# Voice Assistant Application

This is a voice assistant application built with Python, which provides various functionalities like weather updates, time, date, news, music control, and web browsing through voice commands. The assistant listens to commands, processes them, and speaks the results back to the user.

## Features

- **Speech Recognition**: The application listens to voice commands.
- **Text-to-Speech**: It speaks back responses using pyttsx3.
- **Weather Info**: Fetches weather data for a specified city using the OpenWeatherMap API.
- **News Updates**: Retrieves the latest news headlines using the NewsAPI.
- **Music Playback**: Plays songs from a local music library by recognizing song names.
- **Web Browsing**: Opens websites like Google, Facebook, YouTube, and LinkedIn based on voice commands.
- **Time and Date**: Tells the current time and date.

## Requirements

- Python 3.x
- Install the required libraries using pip:

```bash
pip install pyttsx3 SpeechRecognition requests
