import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pywhatkit
import pyjokes
import smtplib
import time
import threading
import re  # Used for extracting numbers from voice input

# Initialize voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your voice assistant. How can I help you today?")

def take_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        listener.adjust_for_ambient_noise(source)
        audio = listener.listen(source)
    try:
        print("Recognizing...")
        command = listener.recognize_google(audio)
        command = command.lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Sorry, my service is down.")
        return ""

def tell_time():
    time_now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {time_now}")

def tell_date():
    date = datetime.datetime.now().strftime("%B %d, %Y")
    speak(f"Today's date is {date}")

def search_wikipedia(query):
    speak("Searching Wikipedia...")
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results. Please be more specific.")
    except:
        speak("I couldn't find anything on that.")

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)


def send_email(to_email, subject, content):
    sender_email = "gowrikakuckian2818@gmail.com"
    sender_password = "irkw nvtr wwih imml"  # App password

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        message = f"Subject: {subject}\n\n{content}"
        server.sendmail(sender_email, to_email, message)
        server.quit()
        speak("Email has been sent successfully.")
    except Exception as e:
        speak("Sorry, I was not able to send the email.")
        print(e)

def set_timer_reminder(message, minutes):
    def reminder():
        time.sleep(minutes * 60)
        speak(f"Reminder: {message}")

    threading.Thread(target=reminder).start()
    speak(f"Okay, I will remind you to {message} in {minutes} minutes.")

def run_voice_assistant():
    greet_user()
    while True:
        command = take_command()
        print("Recognized command is:", command)
        command = command.lower()

        if 'time' in command:
            tell_time()

        elif 'date' in command:
            tell_date()

        elif 'search wikipedia' in command:
            topic = command.replace("search wikipedia", "")
            search_wikipedia(topic)

        elif 'play' in command:
            song = command.replace("play", "")
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)

        elif 'open google' in command:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif 'joke' in command:
            tell_joke()


        elif 'send email' in command or 'email' in command or 'mail' in command or 'send a mail' in command:
            speak("Whom should I send the email to?")
            to_email = input("Enter receiver email address: ")

            speak("What is the subject of the email?")
            subject = take_command()

            speak("What should I say in the email?")
            content = take_command()

            send_email(to_email, subject, content)

        elif 'set a reminder' in command or 'remind me' in command:
            speak("What should I remind you about?")
            message = take_command()

            speak("In how many minutes?")
            try:
                time_input = take_command()
                numbers = re.findall(r'\d+', time_input)

                if numbers:
                    minutes = int(numbers[0])
                    set_timer_reminder(message, minutes)
                else:
                    speak("Sorry, I couldn’t understand the number of minutes.")
            except:
                speak("Sorry, something went wrong while setting the reminder.")

        elif 'exit' in command or 'stop' in command:
            speak("Goodbye! See you soon.")
            break

        elif command != "":
            speak("Sorry, I didn't understand that.")

# Start Assistant
run_voice_assistant()