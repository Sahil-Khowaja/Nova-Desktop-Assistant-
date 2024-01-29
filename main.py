import sys
import os
import time
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QMainWindow , QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QTextCursor
import pyttsx3
import os
import speech_recognition as sr
import wikipedia
import pywhatkit
import webbrowser
import requests
import json
import openai


weather_api_key = "Your OpenWeatherMap API Key"
openai.api_key = "Your Open AI API Key"

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[4].id)
newVoiceRate = 145
engine.setProperty('rate', newVoiceRate)

weather_api_key = "f6d124c444e309197021cb3079b1f617"
openai.api_key = "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"


def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": weather_api_key,
        "units": "metric"  # You can use "imperial" for Fahrenheit
    }

    try:
        response = requests.get(base_url, params=params)
        data = json.loads(response.text)

        if response.status_code == 200:
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            return f"The weather in {city} is {weather_description}. The temperature is {temperature} degrees Celsius."
        else:
            return "Unable to fetch weather information."

    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while fetching weather information."


def ask_openai_gpt3(prompt):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=150
    )
    generated_response = response['choices'][0]['text'].strip()
    return generated_response





def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-pk").lower()
        print(f"User Said: {query}\n")

        if query == 'none':
            print("Say that again, please.....")
            return "None"

        return query

    except sr.UnknownValueError:
        print("No speech detected. Say that again, please.....")
        return "None"

    except Exception as e:
        print(f"Error: {e}")
        print("Say that again, please.....")
        return "None"


class Signal(QObject):
    text_signal = pyqtSignal(str)
    button_label_signal = pyqtSignal(str)


class NovaAssistant(QWidget):
    def __init__(self):
        super().__init__()

        self.signal = Signal()
        self.signal.text_signal.connect(self.update_text)
        self.signal.button_label_signal.connect(self.update_button_label)

        self.assistant_running = False

        self.init_ui()


    def init_ui(self):
        self.setWindowTitle('Nova Assistant')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Add a QLabel for the heading
        heading_label = QLabel('Nova Desktop Assistant', self)
        heading_label.setAlignment(Qt.AlignCenter)
        heading_label.setStyleSheet('''
            color: Black;
            font-size: 30px;
            background-color:#00ADB5;
            font-family: monospace;
            Padding: 10px;
            height: 100%;
            color: White;
        ''')
        layout.addWidget(heading_label)

        # Add a QTextEdit for displaying text
        self.text_edit = QTextEdit(self)
        self.text_edit.setStyleSheet('''
            background-color: #393E46;
            color: #EEEEEE;
            margin: 1px;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ccc;
        ''')
        layout.addWidget(self.text_edit)

        # Add a QPushButton for starting/exit assistant
        self.start_button = QPushButton('Start Assistant', self)
        self.start_button.clicked.connect(self.toggle_assistant)
        self.start_button.setStyleSheet('''
            background-color: #00ADB5;
            color: white;
            border: none;
            padding: 10px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 20px;
            margin: 10px;
            cursor: pointer;
            border-radius: 4px;
        ''')
        layout.addWidget(self.start_button)

        self.setLayout(layout)

        # Apply styles to the main widget
        self.setStyleSheet('''
            background-color: #B4B8C5;
            color: #333;
            font-size: 14px;
        ''')

        self.show()
            
            
        self.text_edit.setStyleSheet('''
                background-color: #393E46;
                color: #EEEEEE;
                margin: 1px;
                padding:10px;
                font-size: 20px;
                spacing: 20px;
                border: 1px solid #ccc;
            ''')
        self.start_button.setStyleSheet('''
                background-color: #00ADB5;
                color: white;
                border: none;
                padding: 10px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 20px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 4px;

            ''')

    def toggle_assistant(self):
        if not self.assistant_running:
            self.assistant_thread = Thread(target=self.assistant_loop)
            self.assistant_thread.start()
            self.start_button.setText('Exit Assistant')
        else:
            self.assistant_running = False
            self.assistant_thread.join()  # Wait for the thread to finish
            self.start_button.setText('Start Assistant')
            sys.exit()  # Exit the application

    def assistant_loop(self):
        self.signal.button_label_signal.emit('Exit Assistant')
        self.assistant_running = True
        webbrowser.register('brave', None, webbrowser.BackgroundBrowser("C:\Program Files\BraveSoftware\Brave-Browser\Application/brave.exe"))

        # Greet the user
        self.wishme()

        while True:
            query = takeCommand().lower()

            if query == "none":
                continue

            if not self.assistant_running:
                break

            if "exit" in query:
                self.signal.text_signal.emit("Nova: Goodbye!")
                speak("Goodbye")
                
                time.sleep(1)
                self.signal.button_label_signal.emit('Start Assistant')
                self.assistant_running = False
                break

            self.signal.text_signal.emit(f'User: {query}\n')

            if "wikipedia" in query:
                speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "")
                try:
                    results = wikipedia.summary(query, sentences=2)
                    self.signal.text_signal.emit(f'Nova: {results}\n')
                    speak("According to Wikipedia")
                    speak(results)
                except wikipedia.exceptions.DisambiguationError as e:
                    self.signal.text_signal.emit(f"Multiple results found. Please be more specific. {e}")
                    speak(f"Multiple results found. Please be more specific. {e}")
                except wikipedia.exceptions.PageError as e:
                    self.signal.text_signal.emit(f"No results found. {e}")
                    speak(f"No results found. {e}")
                    
            elif "made you" in query or "programmed you" in query or "developed you" in query:
                self.signal.text_signal.emit("Nova: I am devoloped by Sahil Khowaja\n")
                speak("I am developed by Sahil Khowaja")

            elif "open youtube" in query:
                url = "youtube.com"
                webbrowser.get('brave').open(url)
                speak("opening youtube")

            elif "open facebook" in query:
                url = "facebook.com"
                webbrowser.get('brave').open(url)
                speak("opening facebook")

            elif "open google" in query:
                url = "google.com"
                webbrowser.get('brave').open(url)
                speak("opening google")
            elif "open instagram" in query:
                url = "instagram.com"
                webbrowser.get('brave').open(url)
                speak("opening instagram")
                

            elif "time" in query:
                strTime = datetime.datetime.now().strftime("%I:%M %p")
                speak("Sir, the time is " + strTime)

            elif "date" in query:
                current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                speak(f"Today's date is {current_date}")

            elif "open adobe acrobat" in query:
                acrobatPath = "C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe"
                os.startfile(acrobatPath)
                speak("opening adobe acrobat")
            elif "open word" in query:
                wordPath = "C:\Program Files\Microsoft Office\Office16\WINWORD.EXE"
                os.startfile(wordPath)
                speak("opening microsoft word")
            elif "open excel" in query:
                excelPath = "C:\Program Files\Microsoft Office\Office16\EXCEL.EXE"
                os.startfile(excelPath)
                speak("opening microsoft excel")
            elif "open powerpoint" in query:
                pptPath = "C:\Program Files\Microsoft Office\Office16\POWERPNT.EXE"
                os.startfile(pptPath)
                speak("opening microsoft powerpoint")

            elif "open chrome" in query:
                chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
                os.startfile(chromePath)
                speak("opening google chrome")
                
            elif "play" in query and "on youtube" in query:
                # Play a Video on YouTube
                video_query = query.replace("play on youtube", "").strip()
                pywhatkit.playonyt(video_query)
                speak(f"playing{video_query} on  YouTube")
                

            elif "weather" in query:
                speak("Sure, please say the city name.")
                city = takeCommand().lower()
                weather_info = get_weather(city)
                self.signal.text_signal.emit(weather_info)
                speak(weather_info)

            elif "search" in query or "open website" in query:
                if "search" in query:
                    search_query = query.replace("search", "").strip()
                    search_url = f"https://www.google.com/search?q={search_query}"
                    webbrowser.get('brave').open(search_url)
                    speak(f"Searching {search_query} on Google.")
                elif "open website" in query:
                    website_name = query.replace("open website", "").strip()
                    if website_name:
                        url = f"https://www.{website_name.lower()}  "
                        webbrowser.get('brave').open(url)
                        speak(f"Opening {website_name} website.")
                    else:
                        speak("Please specify a website name after 'open website'.")
                        

            else:
                gpt3_response = ask_openai_gpt3(f"User: {query}\nNova:")
                self.signal.text_signal.emit(f'Nova: {gpt3_response}\n')
                time.sleep(0.5)  # Wait for a short time before speaking
                speak(gpt3_response)

            time.sleep(1)

        self.signal.button_label_signal.emit('Start Assistant')

    def update_text(self, text):
        self.text_edit.append(text)
        self.text_edit.moveCursor(QTextCursor.End)
        self.text_edit.ensureCursorVisible()



    def update_button_label(self, label):
        self.start_button.setText(label)

    def wishme(self):
        hour = int(datetime.datetime.now().hour)
        if 0 <= hour < 12:
            greeting = "Good Morning, Sir! . I am Nova, How may i help you?"
        elif 12 <= hour < 18:
            greeting = "Good Afternoon, Sir!. I am Nova, How may i help you?"
        else:
            greeting = "Good Evening, Sir!. I am Nova, How may i help you?"

        self.signal.text_signal.emit(f'Nova: {greeting}\n')
        speak(greeting)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    nova_app = NovaAssistant()
    nova_app.show()
    sys.exit(app.exec_())
