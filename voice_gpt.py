import speech_recognition as sr
from gtts import gTTS
import os
from openai import OpenAI
from googletrans import Translator
import requests
import json
client = OpenAI(api_key='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')
recognizer = sr.Recognizer()
translator = Translator()

microphone = sr.Microphone()


with microphone as source:
    print("Говорите что-нибудь...")
    audio = recognizer.listen(source)


try:
    text = recognizer.recognize_google(audio, language="Ru")
    print("Вы сказали: " + text)
    text1 = text

    # translated_text = translate(text1, 'en')
    # print(translated_text)

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "user",
                "content": f"{text1}"
            }
        ],
        temperature=1,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    otvet = response.choices[0].message.content
    print(otvet)
    # translation = translate(str(otvet), 'ru')
    # voice = translation

    url = 'https://api.openai.com/v1/audio/speech'
    headers = {
        'Authorization': 'Bearer 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',
        'Content-Type': 'application/json',
    }

    data = {
        'model': 'tts-1',
        'input': f'{otvet}',
        'voice': 'onyx',
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    with open('speech.mp3', 'wb') as file:
            file.write(response.content)




    # voice = otvet
    # tts = gTTS(voice, lang='ru')
    # tts.save("output.mp3")
    os.system("mpg321 speech.mp3")


except sr.UnknownValueError:
    print("Google ASR не смог распознать аудио.")
except sr.RequestError as e:
    print(f"Ошибка при запросе к Google ASR: {e}")