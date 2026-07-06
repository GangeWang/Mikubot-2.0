import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_JP_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def setup_hook():
    await bot.load_extension("cogs.core")
    await bot.load_extension("cogs.time_task")
    await bot.load_extension("cogs.gacha")
    await bot.load_extension("cogs.feedback")
    await bot.load_extension("cogs.comfy_AI")

bot.run(TOKEN)