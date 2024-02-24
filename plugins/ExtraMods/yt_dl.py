from pyrogram import Client, filters
from pytube import YouTube
import os


@Client.on_message(filters.command(["yt"]))
async def start(client, message):
    await message.reply("Welcome! Send me a YouTube link to download.")

@Client.on_message(filters.text & filters.regex(r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu.be/)[^\s]{11}'))
async def ask_quality(client, message):
    url = message.text
    yt = YouTube(url)
    stream_qualities = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
    qualities = [stream.resolution for stream in stream_qualities]
    unique_qualities = sorted(set(qualities), reverse=True)
    
    quality_msg = "Available qualities:\n" + "\n".join(unique_qualities) + "\nPlease reply with the desired quality (e.g., '720p', '1080p', '2160p')."
    await message.reply(quality_msg)

@Client.on_message(filters.reply & filters.text)
async def download_video(client, message):
    replied_message = message.reply_to_message
    if not replied_message or not replied_message.text.startswith("Available qualities:"):
        await message.reply("Please first request a video and its available qualities.")
        return
    
    url = replied_message.entities[0].url if replied_message.entities else replied_message.text.split('\n')[0]
    quality = message.text.strip()
    yt = YouTube(url)
    stream = yt.streams.filter(res=quality, progressive=True, file_extension='mp4').first()
    
    if stream:
        file_path = stream.download()
        file_name = os.path.basename(file_path)
        await message.reply_document(document=file_path, caption=f"Here's your video 🤪: {yt.title}")
        os.remove(file_path)
    else:
        await message.reply("Could not download the video in the specified quality. Please try a different quality.")
