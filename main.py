import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()


OPENAI_KEY = os.getenv('OPENAI_KEY')

client = OpenAI(api_key=OPENAI_KEY)


def text_to_speech(text, language='en'):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("output.mp3")


r = sr.Recognizer()


def record_text():
    while True:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=1)
                print("Jarvis: (I'm listening...)")

                audio2 = r.listen(source2)
                try:
                    my_text = r.recognize_google(audio2)
                except:
                    print("sorry, could not recognise")
                    my_text = ""
                return my_text
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("Unknown error occurred")


def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(model=model,
        messages=messages,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5)

    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message


messages = [{"role": "user", "content": "Please act like Jarvis from Iron man."}]


while True:
    text = record_text()
    messages.append({"role": "user", "content": text})
    print("You: " + str(text))
    response = send_to_chatGPT(messages)
    print("Jarvis: " + str(response))
    text_to_speech(response)
    playsound("output.mp3")
