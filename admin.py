from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from config import ADMIN_IDS
from db import user_stats, all_active_users, set_block

router = Router()

def is_admin(user_id):
    return user_id in ADMIN_IDS

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer(
        "👨‍💻 <b>Admin panel</b>\n\n"
        "/stats — statistika\n"
        "/users — faol foydalanuvchilar soni\n"
        "/block ID — foydalanuvchini bloklash\n"
        "/unblock ID — blokdan chiqarish\n"
        "/broadcast matn — hammaga xabar yuborish"
    )

@router.message(Command("stats"))
async def stats(message: Message):
    if not is_admin(message.from_user.id):
        return
    total, today, month, blocked = await user_stats()
    await message.answer(
        f"📊 <b>Statistika</b>\nJami: {total}\nBugun: {today}\nBu oy: {month}\nBloklangan: {blocked}"
    )

@router.message(Command("users"))
async def users(message: Message):
    if not is_admin(message.from_user.id):
        return
    ids = await all_active_users()
    await message.answer(f"Faol foydalanuvchilar: {len(ids)}")

@router.message(Command("block"))
async def block(message: Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Foydalanish: /block 123456789")
        return
    await set_block(int(parts[1]), True)
    await message.answer("Foydalanuvchi bloklandi (bot ichida).")

@router.message(Command("unblock"))
async def unblock(message: Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Foydalanish: /unblock 123456789")
        return
    await set_block(int(parts[1]), False)
    await message.answer("Foydalanuvchi blokdan chiqarildi.")

@router.message(Command("broadcast"))
async def broadcast(message: Message):
    if not is_admin(message.from_user.id):
        return
    text = message.text.partition(" ")[2].strip()
    if not text:
        await message.answer("Foydalanish: /broadcast Assalomu alaykum!")
        return
    ids = await all_active_users()
    sent = 0
    failed = 0
    for user_id in ids:
        try:
            await message.bot.send_message(user_id, text)
            sent += 1
        except (TelegramForbiddenError, TelegramBadRequest):
            failed += 1
        except Exception:
            failed += 1
    await message.answer(f"Rassilka yakunlandi.\nYuborildi: {sent}\nYetkazilmadi: {failed}")
