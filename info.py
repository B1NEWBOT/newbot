import telebot
import time
import os
from telebot import types
from telebot.types import Message
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

took = os.getenv("TOKEN")
bot_bssed=telebot.TeleBot(took)