Certainly! Below is the updated README file with information about the OpenWeatherMap API and OpenAI API:

---

# Nova Desktop Assistant

Nova Desktop Assistant is a Python-based desktop application that acts as a virtual assistant, capable of performing various tasks such as answering questions, playing YouTube videos, fetching weather information, and more.

## Features

- **Voice Recognition**: Uses the SpeechRecognition library to recognize voice commands from the user.
- **Text-to-Speech**: Utilizes pyttsx3 library for converting text responses into speech.
- **Web Scraping**: Retrieves information from Wikipedia and other sources using web scraping techniques.
- **YouTube Integration**: Allows users to search and play YouTube videos directly from the application.
- **Weather Information**: Fetches current weather information using the OpenWeatherMap API.
- **OpenAI Integration**: Interacts with OpenAI's GPT-3 model for generating responses to user queries.

## Installation

1. Clone the repository:

    ```
    git clone [<repository_url>](https://github.com/Sahil-Khowaja/Nova-Desktop-Assistant-.git)
    ```

2. Navigate to the project directory:

    ```
    cd Nova-Desktop-Assistant
    ```

3. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

## Usage

1. Run the main script:

    ```
    python main.py
    ```

2. Click on the "Start Assistant" button to activate the assistant.
3. Speak commands or type queries in the text box provided.
4. Enjoy interacting with Nova Desktop Assistant!

## Dependencies

- PyQt5==5.15.6
- pyttsx3==2.90
- pygame==2.1.2
- speechrecognition==3.8.1
- wikipedia==1.4.0
- pywhatkit==5.1
- requests==2.26.0
- openai==0.11.2

## APIs Used

- **OpenWeatherMap API**: Used to fetch current weather information.
- **OpenAI API**: Integrated with OpenAI's GPT-3 model for generating responses.
- **Note**: Replace "Add Your API Key" with your Api Key.

## Credits

- This project was created by Sahil Khowaja.
- Special thanks to the developers of the libraries and APIs used in this project.

## License

This project is licensed under the [MIT License](LICENSE).
