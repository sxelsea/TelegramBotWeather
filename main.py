
import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        return "Город не найден. Проверьте название."

    weather = data["weather"][0]["description"].capitalize()
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]

    return f"🌍 Город: {city}\n🌡 Температура: {temp}°C\n🤔 Ощущается как: {feels_like}°C\n☁️ Погода: {weather}"

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Напиши /weather Город, чтобы узнать погоду.")

async def weather(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Пожалуйста, укажите город после команды. Например: /weather Москва")
        return

    city = " ".join(context.args)
    weather_info = get_weather(city)
    await update.message.reply_text(weather_info)

async def unknown(update: Update, context: CallbackContext):
    await update.message.reply_text("Я тебя не понимаю. Напиши /weather Город, чтобы узнать погоду.")


# Запуск бота
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

    print("Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
