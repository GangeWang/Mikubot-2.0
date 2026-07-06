import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def setup_hook():
    # 載入所有的 Cogs
    await bot.load_extension("cogs.core")
    await bot.load_extension("cogs.time_task")
    await bot.load_extension("cogs.gacha")
    await bot.load_extension("cogs.feedback")
    await bot.load_extension("cogs.comfy_AI")
    await bot.load_extension("cogs.LLM")
bot.run("")


