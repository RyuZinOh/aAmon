import discord


def create_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    return discord.Client(intents=intents)
