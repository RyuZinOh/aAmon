import discord

from db.session import SessionLocal
from services.user_service import get_user


async def handle_inventory(message: discord.Message, args: list[str]):
    async with SessionLocal() as session:
        user = await get_user(session, message.author.id)

    if not user:
        await message.channel.send(
            f"{message.author.mention} you are not registered. Use `register` first."
        )
        return

    item_type = None
    if "--type" in args:
        idx = args.index("--type")
        if idx + 1 < len(args):
            item_type = args[idx + 1].lower()

    if item_type is None:
        bg_count = len(user.backgrounds)
        hero_count = len(user.heroes)
        embed = discord.Embed(
            title=f"{message.author.display_name}'s Inventory",
            description=f"You own {bg_count} backgrounds and {hero_count} hero cards.\n Run `inventory --type background` or `inventory --type card` to see the details.",
            color=discord.Color.blurple(),
        )
        embed.set_thumbnail(url=message.author.display_avatar.url)
        await message.channel.send(embed=embed)
        return

    if item_type == "background":
        if not user.backgrounds:
            await message.channel.send("You  own no backgrounds.")
            return

        embed = discord.Embed(title="Your Backgrounds", color=discord.Color.green())
        for ub in user.backgrounds:
            bg = ub.background
            embed.add_field(
                name=f"`{bg.bg_id}` • {bg.bg_name} • {bg.bg_rarity}",
                value=f"\n",
                inline=False,
            )
        await message.channel.send(embed=embed)
        return

    if item_type in ("card", "hero"):
        if not user.heroes:
            await message.channel.send("You own no hero cards.")
            return
        embed = discord.Embed(title="Your Hero Cards", color=discord.Color.gold())
        for uh in user.heroes:
            hero = uh.hero
            embed.add_field(
                name=f"`{uh.user_hero_id}` • {hero.hero_image} • {hero.hero_tie}",
                value=f"\n",
                inline=False,
            )
        await message.channel.send(embed=embed)
        return
    await message.channel.send("Either user `background` or `card`.")
