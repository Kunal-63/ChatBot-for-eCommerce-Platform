# import speech_recognition as sr
# import pyttsx3 

# # Initialize the recognizer 
# recognizer = sr.Recognizer() 

# # Initialize the text-to-speech engine
# engine = pyttsx3.init()

# # Function to convert text to speech
# def speak_text(text):
#     engine.say(text) 
#     engine.runAndWait()

# # Function to recognize speech
# def recognize_speech():
#     with sr.Microphone() as source:
#         print("Listening...")
#         # Adjust for ambient noise dynamically
#         recognizer.adjust_for_ambient_noise(source)
#         try:
#             # Listen for user's input with timeout and phrase time limit
#             audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
#             return audio
#         except sr.WaitTimeoutError:
#             print("Timeout occurred while waiting for speech.")
#             return None

# # Main loop for speech recognition
# while True:
#     try:
#         # Recognize speech
#         audio_data = recognize_speech()
#         if audio_data:
#             # Using Google Speech Recognition
#             text = recognizer.recognize_google(audio_data)
#             text = text.lower()
#             print("You said:", text)
#             speak_text(text)

            
            
#         else:
#             speak_text("Sorry, I didn't catch that. Can you please repeat?")
        
#     except sr.RequestError as e:
#         print("Could not request results; {0}".format(e))
        
#     except sr.UnknownValueError:
#         print("Sorry, I couldn't understand what you said.")


import speech_recognition as sr
import pyttsx3 

# Initialize the recognizer 
recognizer = sr.Recognizer() 

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to convert text to speech
def speak_text(text):
    engine.say(text) 
    engine.runAndWait()

# Function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        # Adjust for ambient noise dynamically
        recognizer.adjust_for_ambient_noise(source)
        try:
            # Listen for user's input with timeout and phrase time limit
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            return audio
        except sr.WaitTimeoutError:
            print("Timeout occurred while waiting for speech.")
            return None

# Main loop for speech recognition
while True:
    try:
        # Recognize speech
        audio_data = recognize_speech()
        if audio_data:
            # Using Google Speech Recognition
            text = recognizer.recognize_google(audio_data,language='hi-In')
            text = text.lower()
            print("You said:", text)
            # speak_text(text)

            from translate import Translator
            translator= Translator(from_lang="hi",to_lang="en")
            translation = translator.translate(text)
            print(translation)
            
        else:
            speak_text("Sorry, I didn't catch that. Can you please repeat?")
        
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")