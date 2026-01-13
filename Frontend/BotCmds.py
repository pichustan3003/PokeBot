import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

import sqlite3

conn = sqlite3.connect('../Backend/pokemon.db')
c = conn.cursor()

class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # REQUIRED for prefix commands

        super().__init__(
            command_prefix="!",
            intents=intents
        )

        self.add_commands()

    def add_commands(self):
        @self.command(name="ping")
        async def ping(ctx: commands.Context):
            await ctx.send("Pong!")

        @self.command(name="echo")
        async def echo(ctx: commands.Context, *, message: str):
            await ctx.send(message)

        @self.command(name="DataExists")
        async def doesRowExist(ctx, name):
            c.execute("SELECT * FROM pokemon WHERE Species = ?", (name,))
            if c.fetchone():
                await ctx.send("Pokemon exists!")
            else:
                await ctx.send("Pokemon does not exist!")

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")


def main():
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")

    if not token:
        raise RuntimeError("DISCORD_TOKEN not set in .env")

    bot = DiscordBot()
    bot.run(token)


if __name__ == "__main__":
    main()
