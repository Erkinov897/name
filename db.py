import aiosqlite
from datetime import datetime, timezone

DB_NAME = "bot.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            language TEXT DEFAULT 'uz',
            referred_by INTEGER,
            joined_at TEXT,
            is_blocked INTEGER DEFAULT 0
        )""")
        await db.commit()

async def add_user(user, referrer=None):
    async with aiosqlite.connect(DB_NAME) as db:
        cur = await db.execute("SELECT user_id FROM users WHERE user_id=?", (user.id,))
        exists = await cur.fetchone()
        if not exists:
            await db.execute("""INSERT INTO users
                (user_id, username, first_name, referred_by, joined_at)
                VALUES (?, ?, ?, ?, ?)""",
                (user.id, user.username, user.first_name, referrer,
                 datetime.now(timezone.utc).isoformat()))
            await db.commit()
            return True
        await db.execute("UPDATE users SET username=?, first_name=? WHERE user_id=?",
                         (user.username, user.first_name, user.id))
        await db.commit()
        return False

async def get_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cur = await db.execute("SELECT language, is_blocked FROM users WHERE user_id=?", (user_id,))
        return await cur.fetchone()

async def set_language(user_id, lang):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET language=? WHERE user_id=?", (lang, user_id))
        await db.commit()

async def set_block(user_id, blocked):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET is_blocked=? WHERE user_id=?", (int(blocked), user_id))
        await db.commit()

async def all_active_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cur = await db.execute("SELECT user_id FROM users WHERE is_blocked=0")
        return [r[0] for r in await cur.fetchall()]

async def user_stats():
    async with aiosqlite.connect(DB_NAME) as db:
        cur = await db.execute("SELECT COUNT(*) FROM users")
        total = (await cur.fetchone())[0]
        cur = await db.execute("SELECT COUNT(*) FROM users WHERE date(joined_at)=date('now')")
        today = (await cur.fetchone())[0]
        cur = await db.execute("SELECT COUNT(*) FROM users WHERE strftime('%Y-%m', joined_at)=strftime('%Y-%m','now')")
        month = (await cur.fetchone())[0]
        cur = await db.execute("SELECT COUNT(*) FROM users WHERE is_blocked=1")
        blocked = (await cur.fetchone())[0]
        return total, today, month, blocked

async def referral_count(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cur = await db.execute("SELECT COUNT(*) FROM users WHERE referred_by=?", (user_id,))
        return (await cur.fetchone())[0]
