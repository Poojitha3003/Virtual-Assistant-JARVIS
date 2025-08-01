import pyttsx3
import speech_recognition as sr
import eel
import time
import datetime
import engine.features
from engine.voice import speak



def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
       
    except Exception as e:
        return ""
    
    return query.lower()

@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:

        if "open" in query:
            openCommand(query)
        elif "on youtube" in query:
            PlayYoutube(query)
        elif 'time' in query:
                    strTime = datetime.datetime.now().strftime("%I:%M %p")
                    speak(f"sir , The time is {strTime}")
        elif 'date' in query:
                    today = datetime.date.today()
                    print("Today date is: ", today)
                    speak(f"sir , Today date is {today}")
                    
        elif "send message" in query or "phone call" in query or "video call" in query:
            flag = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "send message" in query:
                    flag = 'message'
                    speak("what message to send")
                    query = takecommand()
                    
                elif "phone call" in query:
                    flag = 'call'
                else:
                    flag = 'video call'
                    
                whatsApp(contact_no, query, flag, name)
        else:
            chatBot(query)
    except Exception as e:
        print(f"error: {e}")
    
    eel.ShowHood()