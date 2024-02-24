from pyrogram import Client, filters
from pytube import YouTube
import os




@Client.on_message(filters.command(["yt"]))
async def start(client, message):
    await message.reply("Welcome! Send me a YouTube link, and I will download the video in the highest available quality for you.")

@Client.on_message(filters.regex(r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu.be/)[^\s]{11}'))
async def download_send_video(client, message):
    url = message.text
    yt = YouTube(url)

    # Get the highest resolution video that includes both audio and video
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    
    if stream:
        msg = await message.reply("Downloading video in the highest quality, please wait...")
        temp_file_path = stream.download()

        try:
            await msg.edit("Uploading video, please wait...")
            await client.send_video(message.chat.id, video=temp_file_path, caption=f"Here's your video in the highest quality available: {yt.title}")
        except Exception as e:
            await msg.edit(f"Failed to upload video: {str(e)}")
        
        os.remove(temp_file_path)
    else:
        await message.reply("Failed to download the video. The requested video might not be available in a progressive format that includes both audio and video.")

