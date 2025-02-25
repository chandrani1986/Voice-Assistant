import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
import sys
import requests
import musicLibrary  # Import the musicLibrary module

engine = pyttsx3.init()

API_KEY = "ef1b76462bbc81aa101962e5794d0272"
newsapi = "8e4a4c75935d49e3988cdf5bc8990cbd"

# Function to speak text
def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {e}")

# Function to listen for a command
def listen_command(timeout=5, phrase_time_limit=5):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            command = recognizer.recognize_google(audio).lower()
            print("You said:", command)
            return command
    except sr.UnknownValueError:
        print("Didn't catch that.")
        return ""
    except sr.RequestError:
        print("Check your internet.")
        return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""

# Function to get the current date
def date():
    current_date = datetime.datetime.now().strftime("%A, %Y-%m-%d")
    speak(current_date)

# Function to get the current time
def time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(current_time)

# Function to get the current weather
def weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            main = data["main"]
            weather_description = data["weather"][0]["description"]
            temperature = main["temp"]
            humidity = main["humidity"]
            city_name = data["name"]

            weather_report = (f"The weather in {city_name} is currently {weather_description}. "
                              f"The temperature is {temperature}°C with a humidity of {humidity}%.")
            speak(weather_report)
        else:
            speak("Sorry, I couldn't get the weather information.")
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry, I couldn't fetch the weather data at the moment.")

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ", 1)[1]  # Capture everything after "play"
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            webbrowser.open(link)
            speak(f"Playing {song}")
        else:
            speak("Sorry, I couldn't find that song in the library.")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
                  
            for article in articles:
                speak(article['title'])

    elif 'date' in c.lower():
        date()
    elif 'time' in c.lower():
        time()
    elif 'weather' in c.lower():
        speak("Which city would you like to know the weather for?")
        city = listen_command()
        if city:
            weather(city)
        else:
            speak("I didn't catch the city name.")

    elif 'exit' in c.lower() or 'quit' in c.lower():
        speak("Goodbye!")
        sys.exit()
    else:
        speak("Sorry, I didn't understand that.")

if __name__ == "__main__":
    while True:
        command = listen_command()
        processCommand(command)
