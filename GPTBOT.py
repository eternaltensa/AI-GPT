import telebot
from openai import OpenAI

client = OpenAI(api_key='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')
TOKEN = '6906645359:AAFziGT6rd4_YPe60S_FoOf8PEIK7dpERBs'
bot = telebot.TeleBot(TOKEN)


chat_history = {}


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я GPT чат-бот, работающий на модели gpt-4-turbo.")


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id

    user_messages = chat_history.get(chat_id, [])
    user_messages.append(message.text)

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "user",
                "content": f"{msg}"
            } for msg in user_messages[-2:]
        ],
        temperature=1,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    chat_history[chat_id] = user_messages

    otvet = response.choices[0].message.content
    print(otvet)
    bot.send_message(chat_id, otvet)


if __name__ == "__main__":
    bot.polling(none_stop=True)
