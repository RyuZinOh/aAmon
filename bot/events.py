def register_events(bot):
    def get_command(message):
        if bot.user is None:
            return ""
        content = message.content
        content = content.replace(f"<@{bot.user.id}>", "")
        content = content.replace(f"<@!{bot.user.id}>", "")
        return content.strip().lower()

    @bot.event
    async def on_ready():
        if bot.user is None:
            return
        print(f"{bot.user}:{bot.user.id}")

    @bot.event
    async def on_message(message):
        if bot.user is None:
            return
        if message.author == bot.user:
            return
        if not bot.user.mentioned_in(message):
            return

        cmd = get_command(message)
        if cmd == "test":
            await message.channel.send("working")
        else:
            await message.channel.send("error command")
