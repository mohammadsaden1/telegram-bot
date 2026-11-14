
import os
from threading import Thread
from flask import Flask
from google import genai
import telebot

app = Flask(__name__)


@app.route("/")
def home():
  return "Robot is running!"


def run_flask():
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)


TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)


@bot.message_handler(func=lambda message: True)
def handle_ai_chat(message):
  user_text = message.text
  print(f"پیام دریافتی: {user_text}")
  try:
    # تغییر نام مدل به نسخه جدید و پیشنهادی خود گوگل
    response = client.models.generate_content(
        model="gemini-3.8-flash", contents=user_text
    )
    reply_text = response.text
  except Exception as e:
    print(f"خطا: {e}")
    reply_text = f"خطا در ارتباط با هوش مصنوعی: {e}"

  bot.reply_to(message, reply_text)


if __name__ == "__main__":
  t = Thread(target=run_flask)
  t.start()
  print("ربات و وب‌سرور آماده به کار شدند...")
  bot.infinity_polling()
