import discord

from db.session import SessionLocal
from services.user_service import register_user


async def handle_register(message: discord.Message, args: list[str]):
    async with SessionLocal() as session:
        user, created = await register_user(
            session,
            discord_id=message.author.id,
            username=str(message.author),
        )
    if created:
        await message.channel.send(
            f"Welcome {message.author.mention}, you are now registered!"
        )
    else:
        await message.channel.send(
            f"You are already registered, {message.author.mention}."
        )
