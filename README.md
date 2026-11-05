# Universal Telegram Bot (Aiogram 3)

## Imkoniyatlar
- /start, /help va uch tilli interfeys (uz/ru/en)
- SQLite foydalanuvchilar bazasi
- Referal havola va takliflar soni
- Ixtiyoriy majburiy kanal obunasi
- Admin panel: statistika, bloklash/blokdan chiqarish, rassilka
- Reply va inline tugmalar

## 1. BotFather
Telegramda @BotFather orqali `/newbot` yuboring, bot nomi va username tanlang. Tokenni oling.

## 2. Muhit sozlamalari
`.env.example` faylidan nusxa olib `.env` deb nomlang. `BOT_TOKEN` qatoriga tokenni, `ADMIN_IDS` qatoriga o'zingizning Telegram raqamingizni (ID) yozing.
Kanal tekshiruvi kerak bo'lmasa `CHANNEL_ID` va `CHANNEL_LINK` qiymatlarini bo'sh qoldiring.
Majburiy obuna uchun botni kanalingizga administrator qilib qo'shing.

## 3. Windows / VS Code
Terminalni loyiha papkasida oching va quyidagilarni bajaring:

```powershell
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py main.py
```

Botni to'xtatish: `Ctrl+C`.

## 4. Admin buyruqlari
- `/admin`
- `/stats`
- `/users`
- `/block 123456789`
- `/unblock 123456789`
- `/broadcast Xabar matni`

## Muhim eslatmalar
- Bot tokenini hech kimga bermang va `.env` faylini internetga joylamang.
- `ADMIN_IDS` ichiga faqat ishonchli admin IDlarini kiriting.
- Telegram bot foydalanuvchiga birinchi bo'lib shaxsiy xabar yubora olmaydi: foydalanuvchi avval botni ishga tushirgan bo'lishi kerak.
- Click/Payme to'lovlari uchun merchant kabineti, API kalitlari va server webhooklari talab qilinadi; bu starter loyihada real to'lov qabul qilish yoqilmagan.
- Eslatma rejalashtirish, PostgreSQL va media fayllarini maxsus qayta ishlash keyingi bosqichda qo'shilishi mumkin.
