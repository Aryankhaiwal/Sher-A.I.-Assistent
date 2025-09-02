from ast import Return
import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from winotify import Notification
import pyautogui
import wikipedia
import pywhatkit as pwk
import conf
import smtplib, ssl
import gemini_request as ai
import mtranslate
import sys

# --- Fix printing for Hindi (UTF-8) ---
sys.stdout.reconfigure(encoding='utf-8')

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty("rate", 150)


# --- Speak function (multi-language) ---
def speak(Audio, lang="en"):
    try:
        if lang == "hi":
            text = mtranslate.translate(Audio, to_language='hi', from_language='en')
            print("Speaking (Hindi):", text)
            engine.say(text)
        else:
            print("Speaking (English):", Audio)
            engine.say(Audio)
        engine.runAndWait()
    except UnicodeEncodeError:
        print("<<Non-English text skipped>>")


# --- Listen and detect Hindi/English ---
def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        # Try English first
        content = r.recognize_google(audio, language='en-IN')
        lang = "en"
    except:
        try:
            # Fallback to Hindi
            content = r.recognize_google(audio, language='hi-IN')
            lang = "hi"
        except Exception as e:
            print("Say again!", e)
            return "", "en"

    print("Original Speech:", content.encode("utf-8", errors="ignore").decode("utf-8"))

    # Translate to English for command processing
    translated = mtranslate.translate(content, to_language='en', from_language='auto')
    print("Translated to English:", translated)

    return translated.lower() if translated else "", lang


# --- Main Process ---
def main_process():
    while True:
        request, lang = command()
        request = request.lower()

        if "hello" in request:
            speak("How can I help you?", lang)

        elif "play music" in request:
            speak("Playing music", lang)
            song = random.randint(1, 3)
            if song == 1:
                webbrowser.open("https://www.youtube.com/watch?v=PSJzUYbpHX0")
            elif song == 2:
                webbrowser.open("https://www.youtube.com/watch?v=Llav5_-5idA")
            elif song == 3:
                webbrowser.open("https://www.youtube.com/watch?v=vPF3Fl5LeY8")

        elif "say time" in request:
            curr_time = datetime.datetime.now().strftime("%H:%M")
            speak("Current time is " + curr_time, lang)

        elif "say date" in request:
            curr_date = datetime.datetime.now().strftime("%d:%m")
            speak("Today's date is " + curr_date, lang)

        elif "new" in request:
            task = request.replace("new", "").strip()
            if task != "":
                speak("Adding task " + task, lang)
                with open("todo.txt", "a", encoding="utf-8") as file:
                    file.write(task + "\n")

        elif "speak d" in request:
            with open("todo.txt", "r", encoding="utf-8") as file:
                speak("Work I do today: " + file.read(), lang)

        elif "so work" in request:
            try:
                with open("todo.txt", "r", encoding="utf-8") as file:
                    tasks = file.readlines()

                if not tasks:
                    tasks_text = "No tasks found!"
                else:
                    tasks_text = " • ".join([t.strip() for t in tasks if t.strip()])

                toast = Notification(
                    app_id="My Assistant",
                    title="Today Work",
                    msg=tasks_text,
                    duration="short"
                )
                toast.show()
                speak("I have shown your tasks in notification", lang)
            except FileNotFoundError:
                speak("No todo file found yet", lang)

        elif "open youtube" in request:
            webbrowser.open("www.youtube.com")

        elif "open" in request:
            query = request.replace("open", "")
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press("enter")

        elif "wikipedia" in request:
            request = request.replace("sher", "").replace("search wikipedia", "")
            result = wikipedia.summary(request, sentences=2)
            print(result)
            speak(result, lang)

        elif "search google" in request:
            request = request.replace("sher", "").replace("search google", "")
            webbrowser.open("https://www.google.com/search?q=" + request)

        elif "send whatsapp" in request:
            pwk.sendwhatmsg_instantly("+918273581494", "hi", wait_time=15, tab_close=True, close_time=3)

        elif "send email" in request:
            a = smtplib.SMTP('smtp.gmail.com', 587)
            a.starttls()
            a.login('aryankhaiwal94@gmail.com', conf.gmail_pass)
            message = "How are you"
            a.sendmail('aryankhaiwal94@gmail.com', 'aryankhaiwal94@gmail.com', message)
            a.quit()
            speak("Email sent", lang)

        elif "chat" in request:
            request = request.replace("sher", "").replace("chat", "").strip()
            print("User query:", request)

            response = ai.send_request(request)
            print("Gemini Response:", response)

            sentences = response.split(".")
            short_response = ". ".join(sentences[:2]).strip()

            speak(short_response if short_response else "Sorry, I didn't get a response.", lang)


if __name__ == "__main__":
    main_process()

