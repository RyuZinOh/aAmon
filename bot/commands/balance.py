import discord

from db.session import SessionLocal
from services.user_service import get_user


async def handle_balance(message: discord.Message, args: list[str]):
    async with SessionLocal() as session:
        user = await get_user(session, message.author.id)

    if not user:
        await message.channel.send(
            f"{message.author.mention} you are not registered. Use `register` first."
        )
        return

    balance = user.chronux.balance if user.chronux else 0

    embed = discord.Embed(color=discord.Color.gold())
    embed.set_author(
        name=message.author.display_name,
        # icon_url=message.author.display_avatar.url,
    )
    embed.set_thumbnail(url=message.author.display_avatar.url)
    embed.add_field(name="Chronux", value=f"{balance}", inline=False)

    await message.channel.send(embed=embed)
