from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from config import CHANNEL_ID, CHANNEL_LINK
from db import add_user, get_user, set_language, referral_count
from keyboards import main_menu, language_keyboard, subscription_keyboard
from locales import TEXT

router = Router()

async def get_lang(user_id):
    row = await get_user(user_id)
    return row[0] if row and row[0] in TEXT else "uz"

async def is_subscribed(bot, user_id):
    if not CHANNEL_ID:
        return True
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception:
        return False

async def subscription_gate(message: Message):
    if await is_subscribed(message.bot, message.from_user.id):
        return True
    lang = await get_lang(message.from_user.id)
    await message.answer(TEXT[lang]["subscribe"],
                         reply_markup=subscription_keyboard(CHANNEL_LINK))
    return False

@router.message(CommandStart())
async def start(message: Message):
    args = message.text.split(maxsplit=1)
    referrer = None
    if len(args) > 1 and args[1].startswith("ref_"):
        try:
            candidate = int(args[1][4:])
            if candidate != message.from_user.id:
                referrer = candidate
        except ValueError:
            pass
    await add_user(message.from_user, referrer)
    lang = await get_lang(message.from_user.id)
    if not await subscription_gate(message):
        return
    await message.answer(TEXT[lang]["welcome"].format(name=message.from_user.first_name),
                         reply_markup=main_menu(lang))
    await message.answer(TEXT[lang]["menu"])

@router.callback_query(F.data == "check_sub")
async def check_sub(callback: CallbackQuery):
    if await is_subscribed(callback.bot, callback.from_user.id):
        lang = await get_lang(callback.from_user.id)
        await callback.message.answer(TEXT[lang]["menu"], reply_markup=main_menu(lang))
        await callback.answer("Obuna tasdiqlandi!")
    else:
        lang = await get_lang(callback.from_user.id)
        await callback.answer(TEXT[lang]["not_sub"], show_alert=True)

@router.message(Command("help"))
async def help_cmd(message: Message):
    if not await subscription_gate(message):
        return
    lang = await get_lang(message.from_user.id)
    await message.answer(TEXT[lang]["help"])

@router.message(Command("language"))
@router.message(F.text.in_({"🌐 Tilni o‘zgartirish", "🌐 Изменить язык", "🌐 Change language"}))
async def language_cmd(message: Message):
    await message.answer(TEXT[await get_lang(message.from_user.id)]["language"],
                         reply_markup=language_keyboard())

@router.callback_query(F.data.startswith("lang:"))
async def language_set(callback: CallbackQuery):
    lang = callback.data.split(":")[1]
    if lang not in TEXT:
        await callback.answer("Noto‘g‘ri til")
        return
    await set_language(callback.from_user.id, lang)
    await callback.message.answer("✅", reply_markup=main_menu(lang))
    await callback.answer("Til o‘zgartirildi")

@router.message(Command("referral"))
@router.message(F.text.in_({"👥 Do‘st taklif qilish", "👥 Пригласить друзей", "👥 Invite friends"}))
async def referral(message: Message):
    me = await message.bot.get_me()
    count = await referral_count(message.from_user.id)
    lang = await get_lang(message.from_user.id)
    link = f"https://t.me/{me.username}?start=ref_{message.from_user.id}"
    await message.answer(TEXT[lang]["ref"].format(link=link, count=count))

@router.message(F.text.in_({"ℹ️ Bot haqida", "ℹ️ О боте", "ℹ️ About"}))
async def about(message: Message):
    lang = await get_lang(message.from_user.id)
    await message.answer(TEXT[lang]["about"])

@router.message()
async def fallback(message: Message):
    if not await subscription_gate(message):
        return
    await message.answer("Xabaringiz qabul qilindi. Tez orada yangi bo‘limlar qo‘shiladi.")
