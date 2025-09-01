import telebot
from telebot import types
from config import TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

# Доступные валюты
CURRENCIES = {
    "доллар": "USD",
    "евро": "EUR",
    "рубль": "RUB",
    "юань": "CNY"

}


@bot.message_handler(commands=['start', 'help'])
def send_help(message):
    help_text = """
💱 *Конвертер валют* 💱

📌 *Формат запроса:*
`<валюта 1> <валюта 2> <количество>`

📌 *Пример:*
`доллар рубль 100` — узнает, сколько 100 долларов в рублях.

📌 *Доступные команды:*
/start, /help — инструкция
/values — список валют
"""
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")


@bot.message_handler(commands=['values'])
def send_values(message):
    values_text = "📊 *Доступные валюты:*\n" + "\n".join(
        f"- {name} ({code})" for name, code in CURRENCIES.items()
    )
    bot.send_message(message.chat.id, values_text, parse_mode="Markdown")


@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            raise APIException("Неверный формат! Используйте: <валюта1> <валюта2> <количество>")

        base, quote, amount = parts
        amount = float(amount)

        if base.lower() not in CURRENCIES:
            raise APIException(f"Валюта {base} не поддерживается!")
        if quote.lower() not in CURRENCIES:
            raise APIException(f"Валюта {quote} не поддерживается!")

        base_code = CURRENCIES[base.lower()]
        quote_code = CURRENCIES[quote.lower()]

        result = CurrencyConverter.get_price(base_code, quote_code, amount)
        bot.reply_to(message, f"💵 {amount} {base_code} = {result} {quote_code}")

    except ValueError:
        bot.reply_to(message, "❌ Ошибка: количество должно быть числом!")
    except APIException as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")
    except Exception as e:
        bot.reply_to(message, f"⚠ Неизвестная ошибка: {e}")


if __name__ == "__main__":
    bot.polling(none_stop=True)