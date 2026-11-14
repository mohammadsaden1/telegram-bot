import os
from threading import Thread
from flask import Flask
from google import genai
import telebot

# مقداردهی وب‌سرور فلاسْک برای راضی کردن رندر
app = Flask(__name__)


@app.route("/")
def home():
  return "Robot is running!"


def run_flask():
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)


# تنظیمات ربات تلگرام
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)


@bot.message_handler(func=lambda message: True)
def handle_ai_chat(message):
  user_text = message.text
  try:
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=user_text
    )
    reply_text = response.text
  except Exception as e:
    reply_text = "متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید."

  bot.reply_to(message, reply_text)


if __name__ == "__main__":
  # اجرای وب‌سرور در پس‌زمینه برای داشتن پورت فعال
  t = Thread(target=run_flask)
  t.start()

  print("ربات و وب‌سرور آماده به کار شدند...")
  bot.infinity_polling()
