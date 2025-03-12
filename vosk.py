import telebot
from gtts import gTTS
from vosk import Model, KaldiRecognizer
from googletrans import Translator
import io

TOKEN = 'token'


bot = telebot.TeleBot(TOKEN)


model = Model("vosk-model-small-en-us-0.15")

@bot.message_handler(content_types=['voice'])
def voice_to_text(message):
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    file = bot.download_file(file_info.file_path)

    audio_bytes_io = io.BytesIO(file)

    rec = KaldiRecognizer(model, 16000)
    rec.AcceptWaveform(audio_bytes_io.read())
    text = rec.Result()

    try:
        result = text[text.index('result')+10 : text.index(']')]
        text = result.strip().strip('"')

   
        translator = Translator()
        translated_text = translator.translate(text, src='en', dest='ru').text  
        bot.send_message(message.chat.id, text=translated_text)
     
        tts = gTTS(text=translated_text, lang='ru') 
        tts.save('translated_voice.ogg')
        bot.send_voice(message.chat.id, open('translated_voice.ogg', 'rb'))

    except ValueError:
        bot.send_message(message.chat.id, 'Не удалось распознать речь.')

if __name__ == "__main__":
    bot.polling()
