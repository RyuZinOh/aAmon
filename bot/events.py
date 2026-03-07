from bot.commands.profile import handle_profile
from bot.commands.user import handle_register

COMMANDS = {"register": handle_register, "profile": handle_profile}


def register_events(bot):
    def get_command(message):
        if bot.user is None:
            return "", []
        content = message.content
        content = content.replace(f"<@{bot.user.id}>", "")
        content = content.replace(f"<@!{bot.user.id}>", "")
        parts = content.strip().split()
        if not parts:
            return "", []
        return parts[0].lower(), parts[1:]

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

        cmd, args = get_command(message)

        handler = COMMANDS.get(cmd)
        if handler:
            await handler(message, args)
        else:
            await message.channel.send(f"Unknown {cmd}")
