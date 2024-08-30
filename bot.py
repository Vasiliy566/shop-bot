import json
from io import BytesIO
from pprint import pprint

import telebot

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile, \
    Message, CallbackQuery

from shop_api import is_user_registered, register_user, get_products, purchase

BOT_TOKEN = "7313979327:AAH6v02APjEuv4ifvcrXmDu-Hs7YCo2QktQ"

bot = telebot.TeleBot(BOT_TOKEN)

cache_dict = {}

@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    registered = is_user_registered(message.from_user.id)

    if registered:
        markup = InlineKeyboardMarkup()

        products = get_products()
        for product in products:
            cache_dict[product["id"]] = {"id": product["id"], "price": product["price"], "image": product["image"], "name": product["name"]}
            callback_button = InlineKeyboardButton(
                text=f"{product['name']}: {product['price']}",
                callback_data=product["id"])
            markup.add(callback_button)

        bot.send_message(message.chat.id, "Товары в наличии", reply_markup=markup)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        register_button = KeyboardButton('Зарегистрироваться')
        markup.row(register_button)
        bot.send_message(message.chat.id, "Необходимо зарегистрироваться.", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_text(message: Message):
    if message.text == 'Зарегистрироваться':
        register_user(message.from_user.id)
        bot.send_message(message.chat.id, "Спасибо за регистрацию.")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: CallbackQuery):
    data = cache_dict[int(call.data)]

    purchase(call.from_user.id, data["id"], data["price"])

    if len(data["image"]) > 0:
        bot.send_photo(call.message.chat.id,
                          data["image"],
                          caption=f"Вы купили {data['name']} за {data['price']}.", )
    else:
        bot.send_message(call.message.chat.id, f"Вы купили {data['name']} за {data['price']}.")


bot.polling(none_stop=True)
