import asyncio
import os
import sys

# Додаємо шлях до кореня, щоб Python бачив папку core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import async_session
from core.models import User
from werkzeug.security import generate_password_hash

async def setup_admin():
    tg_id = input("Enter Telegram ID of the admin user: ")
    password = input("Enter password for the admin: ")

    async with async_session() as session:
        user = await session.scalar(
            select(User).where(User.tg_id == int(tg_id))
        )
        if user:
            user.password_hash = generate_password_hash(password)
            user.is_admin = True
            await session.commit()
            print(f"✅ Admin setup complete for user {user.full_name} (TG ID: {tg_id})")
        else:
            print("❌ User not found. Please ensure the user is registered in the bot first.")

if __name__ == "__main__":
    from sqlalchemy import select
    asyncio.run(setup_admin())