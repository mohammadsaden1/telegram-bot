import os
from google import genai
import telebot

# خواندن توکن و کلیدها از متغیرهای محیطی (برای امنیت بیشتر در هاست ابری)
TELEGRAM_TOKEN = os.environ.get(
    "TELEGRAM_TOKEN", "8883313715:AAEQSVqy6VEBXZ-Kn-POUGouwGDVaVd07ws"
)
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
  print("ربات روی هاست ابری آماده به کار شد...")
  bot.infinity_polling()
