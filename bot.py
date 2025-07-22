import os
import traceback
import discord
from discord.ext import commands
import yt_dlp
from dotenv import load_dotenv
from collections import deque

load_dotenv()

# -------- CONFIG --------
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
PREFIX = "/"
INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.voice_states = True

bot = commands.Bot(command_prefix=PREFIX, intents=INTENTS)
queues = {}  # 每個伺服器的播放佇列
now_playing = {}  # 目前播放中的歌曲

# -------- AUDIO FUNCTION --------
def get_audio_source(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'cookiefile': 'cookies.txt',
        'default_search': 'ytsearch1:',
        'extract_flat': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        if 'entries' in info:
            if not info['entries']:
                raise Exception("❌ 找不到搜尋結果。")
            info = info['entries'][0]

        audio_url = info['url']
        title = info.get('title', '未知標題')

    ffmpeg_opts = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }

    return discord.FFmpegPCMAudio(audio_url, **ffmpeg_opts), title

def ensure_queue(guild_id):
    if guild_id not in queues:
        queues[guild_id] = deque()

async def play_next(ctx):
    guild_id = ctx.guild.id
    ensure_queue(guild_id)

    if queues[guild_id]:
        source, title = queues[guild_id].popleft()
        now_playing[guild_id] = title
        vc = ctx.voice_client
        vc.play(source, after=lambda e: bot.loop.create_task(play_next(ctx)))
        await ctx.send(f"🎵 現在播放：**{title}**")
    else:
        now_playing[guild_id] = None

# -------- COMMANDS --------
@bot.event
async def on_ready():
    print(f'✅ Bot 上線：{bot.user.name}')

@bot.command(name="join")
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        await ctx.send("📡 已加入語音頻道！")
    else:
        await ctx.send("⚠️ 你必須先加入一個語音頻道。")

@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 已離開語音頻道。")

@bot.command(name="play")
async def play(ctx, *, url: str):
    if not ctx.author.voice:
        await ctx.send("⚠️ 你需要先加入一個語音頻道。")
        return

    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()

    try:
        source, title = get_audio_source(url)
        ensure_queue(ctx.guild.id)
        queues[ctx.guild.id].append((source, title))

        if not ctx.voice_client.is_playing():
            await play_next(ctx)
        else:
            await ctx.send(f"✅ 已加入佇列：**{title}**")
    except Exception as e:
        traceback.print_exc()
        await ctx.send(f"❌ 播放失敗：{str(e)}")

@bot.command(name="skip")
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏭️ 已跳過歌曲。")

@bot.command(name="pause")
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸️ 已暫停播放。")

@bot.command(name="resume")
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("▶️ 已繼續播放。")

@bot.command(name="stop")
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        queues[ctx.guild.id].clear()
        now_playing[ctx.guild.id] = None
        await ctx.send("⏹️ 已停止播放，佇列已清空。")

@bot.command(name="np")
async def np(ctx):
    title = now_playing.get(ctx.guild.id)
    if title:
        await ctx.send(f"🎶 現在播放：**{title}**")
    else:
        await ctx.send("⚠️ 沒有正在播放的歌曲。")

# -------- MAIN --------
bot.run(TOKEN)
