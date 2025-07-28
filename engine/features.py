import os
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
import eel
import pyaudio
import pyautogui
import pygame
import pywhatkit as kit
import pvporcupine

from pipes import quote
from hugchat import hugchat
from engine.command import speak
from engine.config import ASSISTANT_NAME
from engine.helper import extract_yt_term, remove_words

import subprocess
import time
import pyautogui
from urllib.parse import quote
from engine.command import speak

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir = os.path.abspath("www/assets/audio/start_sound.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load(music_dir)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "").replace("open", "").lower().strip()
    app_name = query

    try:
        cursor.execute('SELECT path FROM sys_command WHERE name = ?', (app_name,))
        results = cursor.fetchall()

        if results:
            speak("Opening " + app_name)
            os.startfile(results[0][0])
        else:
            cursor.execute('SELECT url FROM web_command WHERE name = ?', (app_name,))
            results = cursor.fetchall()

            if results:
                speak("Opening " + app_name)
                webbrowser.open(results[0][0])
            else:
                speak("Opening " + app_name)
                try:
                    os.system(f'start {app_name}')
                except:
                    speak("Not found.")
    except Exception as e:
        speak("Something went wrong.")
        print(f"Error in openCommand: {e}")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing " + search_term + " on YouTube")
    kit.playonyt(search_term)

def hotword():
    porcupine = None
    paud = None
    audio_stream = None

    try:
        porcupine = pvporcupine.create(keywords=["jarvis", "alexa"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16,
                                 input=True, frames_per_buffer=porcupine.frame_length)

        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            keyword_index = porcupine.process(keyword)

            if keyword_index >= 0:
                print("Hotword detected")
                pyautogui.keyDown("win")
                pyautogui.press("j")
                time.sleep(2)
                pyautogui.keyUp("win")

    except Exception as e:
        print(f"Hotword error: {e}")
    finally:
        if porcupine:
            porcupine.delete()
        if audio_stream:
            audio_stream.close()
        if paud:
            paud.terminate()

def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove).strip().lower()

    try:
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?",
                       ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except Exception as e:
        speak('Not found in contacts')
        print(f"findContact error: {e}")
        return 0, 0

def whatsapp(mobile_no, message, flag, name):
    if flag == 'message':
        target_tab = 12
        jarvis_message = f"Message sent successfully to {name}"
    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = f"Calling {name}"
    else:
        target_tab = 6
        message = ''
        jarvis_message = f"Starting video call with {name}"

    # Encode message
    encoded_message = quote(message)

    # Use the whatsapp:// protocol only if app handles it
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
    command = f'start "" "{whatsapp_url}"'

    try:
        subprocess.run(command, shell=True)
        time.sleep(5)
        
        # Press the right number of tabs to reach the button
        pyautogui.hotkey('ctrl', 'f')
        for _ in range(1, target_tab):
            pyautogui.press('tab')
        pyautogui.press('enter')

        speak(jarvis_message)
    except Exception as e:
        speak("Something went wrong while trying to open WhatsApp.")
        print(f"Error: {e}")

@eel.expose
def chatBot(query):
    try:
        user_input = query.lower()
        chatbot = hugchat.ChatBot(cookie_path="engine/cookies.json")
        conversation_id = chatbot.new_conversation()
        chatbot.change_conversation(conversation_id)
        response = chatbot.chat(user_input)
        print(response)
        speak(response)
        return response
    except Exception as e:
        error_msg = f"Sorry, I couldn't process your request. Error: {str(e)}"
        print(error_msg)
        speak(error_msg)
        return error_msg
