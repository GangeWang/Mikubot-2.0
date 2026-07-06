from discord.ext import commands

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"已登入為 {self.bot.user}")
        print(f"目前加入了 {len(self.bot.guilds)} 個伺服器")
        '''for guild in self.bot.guilds:
            allowed = [1223275274951463006, 675695004101902366,948513995348910140,]  # 允許的 guild ID
            if guild.id not in allowed:
                print(f"離開未知伺服器: {guild.name} ({guild.id})")
                await guild.leave()'''
        try:
            synced = await self.bot.tree.sync()
            print(f"成功同步 {len(synced)} 個指令")
        except Exception as e:
            print(f"同步指令時出錯: {e}")

    @commands.Cog.listener()
    async def on_message(self, msg):
        if "114514" in msg.content:
            await msg.channel.send("<:Yaju_Senpai_Shouting:1251549282679394356>")

async def setup(bot):
    await bot.add_cog(Core(bot))
