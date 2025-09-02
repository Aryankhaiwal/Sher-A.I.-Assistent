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


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty("rate",150) 


def speak(Audio):
    hindi_text = mtranslate.translate(Audio, to_language='hi', from_language='en')
    print("Speaking:", hindi_text)
    engine.say(hindi_text)
    engine.runAndWait()
def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        # Try recognizing (supports Hindi + English)
        content = r.recognize_google(audio, language='hi-IN')
        print("Original Speech:", content.encode("utf-8", errors="ignore").decode("utf-8"))


        # Translate → English for processing
        translated = mtranslate.translate(content, to_language='en', from_language='auto')
        print("Translated to English:", translated)

        # Return safe lowercase string
        return translated.lower() if translated else ""
    except Exception as e:
        print("Say again!", e)
        return ""   # Always return string (not None)


def main_process():
    while True:
        request = command().lower()
        if "hello" in request:
            speak("how i can help you")
        elif "play music" in request:
            speak("playing music")
            song=random.randint(1,3)
            if song==1:
                webbrowser.open("https://www.youtube.com/watch?v=PSJzUYbpHX0&list=RDPSJzUYbpHX0&start_radio=1&pp=ygULdGFnZGUga2FyYW2gBwE%3D")
            elif song==2:
                webbrowser.open("https://www.youtube.com/watch?v=Llav5_-5idA&list=RDLlav5_-5idA&start_radio=1&pp=ygUQZ2hhbmUgZ2FuZGUgc29uZ6AHAdIHCQmyCQGHKiGM7w%3D%3D")
            elif song ==3:
                webbrowser.open("https://www.youtube.com/watch?v=vPF3Fl5LeY8&list=RDvPF3Fl5LeY8&start_radio=1&pp=ygUQcmFpbCBzdW1pdCBwYXJ0YaAHAQ%3D%3D")
        elif "say time" in request:
            curr_time=datetime.datetime.now().strftime("%H:%M")
            speak("current time is " + curr_time)
        elif "say date" in request:
            curr_date=datetime.datetime.now().strftime("%d:%m")
            speak("current time is " + curr_date)
        elif "new" in request:
            task=request.replace("new","")
            task=task.strip()
            if task !="":
                speak("adding task " + task)
                with open("todo.txt","a") as file:
                    file.write(task + "\n")
        elif "speak d" in request:
            with open("todo.txt","r") as file:
                speak("work i do today" + file.read())
        elif "so work" in request:
            try:
                with open("todo.txt", "r") as file:
                    tasks = file.readlines()

                if not tasks:
                    tasks_text = "No tasks found!"
                else:
            # Join tasks with commas or newlines
                    tasks_text = " • ".join([t.strip() for t in tasks if t.strip()])

                toast = Notification(
                    app_id="My Assistant",
                    title="Today Work",
                    msg=tasks_text,
                    duration="short"
        )
                toast.show()
                speak("I have shown your tasks in notification")
            except FileNotFoundError:
                speak("No todo file found yet")
            
        elif "open youtube" in request:
            webbrowser.open("www.youtube.com")

        elif "open" in request:
            query=request.replace("open","")
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press("enter")
        elif "wikipedia" in request:
            request=request.replace("sher","")
            request=request.replace("search wikipedia","")
            result=wikipedia.summary(request,sentences=2)
            print(result)
            speak(result)

        elif "search google" in request:
            request=request.replace("sher","")
            request=request.replace("search google","")
            webbrowser.open("https://www.google.com/search?q= " + request)
        
        elif "send whatsapp" in request:
            pwk.sendwhatmsg_instantly("+918273581494" , "hi" , wait_time=15,tab_close=True, close_time=3)
        
        #elif "send gmail" in request:
        #   pwk.send_mail("aryankhaiwal94@gmail.com",conf.gmail_pass,"Hello","How are you","aryankhaiwal94@gmail.com")
       
        elif "send email" in request:
           a=smtplib.SMTP('smtp.gmail.com',587)
           a.starttls()
           a.login('aryankhaiwal94@gmail.com',conf.gmail_pass)
           message=""" How are you"""
           a.sendmail('aryankhaiwal94@gmail.com','aryankhaiwal94@gmail.com',message)
           a.quit()
           speak("email send")

        elif "bol" in request:
            request = request.replace("sher", "")
            request = request.replace("bol", "")
            request = request.strip()
            print("User query:", request)

            response = ai.send_request(request)
            print("Gemini Response:", response)

    
            sentences = response.split(".")
            short_response = ". ".join(sentences[:2]).strip()

            speak(short_response if short_response else "Sorry, I didnt get a response.")





main_process()



# voice("how are you,i am waiting for you")