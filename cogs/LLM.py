import discord
from discord.ext import commands
import aiohttp
import json

class LLM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 用字典保存每個使用者的對話歷史
        self.histories = {}

    @discord.app_commands.command(name="ask", description="有記憶的 AI 回覆")
    async def ask(self, interaction: discord.Interaction, prompt: str):
        user_id = interaction.user.id

        # 初始化使用者歷史
        if user_id not in self.histories:
            self.histories[user_id] = []

        # 把新的問題加入歷史
        self.histories[user_id].append({"role": "user", "content": prompt})

        # 只保留最近 5 條
        history = self.histories[user_id][-5:]

        # 拼接成 prompt
        context = "\n".join([f"{h['role']}: {h['content']}" for h in history])
        final_prompt = f"{context}\nassistant:"

        await interaction.response.defer()
        await interaction.edit_original_response(content="正在生成回覆...")

        url = "http://100.111.80.10:8008/api/generate"
        data = {
            "model": "gpt-oss:20b",
            "prompt": f"請用繁體中文回答：{final_prompt}",
            "stream": True
        }

        answer = ""
        buffer = ""

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as resp:
                async for line in resp.content:
                    if line:
                        try:
                            chunk = json.loads(line.decode("utf-8"))
                            if "response" in chunk:
                                text = chunk["response"]
                                answer += text
                                buffer += text

                                # 每 10 個字更新一次
                                if len(buffer) >= 10:
                                    await interaction.edit_original_response(content=answer)
                                    buffer = ""
                        except Exception:
                            continue

        # 最後更新完整答案
        if answer.strip():
            await interaction.edit_original_response(content=answer)
            # 把 AI 回覆也加入歷史
            self.histories[user_id].append({"role": "assistant", "content": answer})
        else:
            await interaction.edit_original_response(content=":warning: 沒有收到模型回覆")

async def setup(bot: commands.Bot):
    await bot.add_cog(LLM(bot))