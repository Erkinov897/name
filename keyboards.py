from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from locales import TEXT

def main_menu(lang="uz"):
    labels = {
        "uz": ["ℹ️ Bot haqida", "🌐 Tilni o‘zgartirish", "👥 Do‘st taklif qilish"],
        "ru": ["ℹ️ О боте", "🌐 Изменить язык", "👥 Пригласить друзей"],
        "en": ["ℹ️ About", "🌐 Change language", "👥 Invite friends"]
    }
    a, b, c = labels.get(lang, labels["uz"])
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=a)],
        [KeyboardButton(text=b), KeyboardButton(text=c)]
    ], resize_keyboard=True)

def language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🇺🇿 O‘zbekcha", callback_data="lang:uz"),
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
        InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en")
    ]])

def subscription_keyboard(link):
    rows = []
    if link:
        rows.append([InlineKeyboardButton(text="📢 Kanalga obuna bo‘lish", url=link)])
    rows.append([InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check_sub")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
