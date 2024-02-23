from pyrogram import Client, filters
from pytube import YouTube
import os

# Use your own values here


# Create the client and connect

@Client.on_message(filters.command(["yt", "youtube"]))
async def start(client, message):
    await message.reply("Welcome! Send me a YouTube link, and I'll download it for you. Reply to this message with the desired quality (e.g., '720p', '1080p').")

@Client.on_message(filters.text & filters.regex(r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+'))
async def download_youtube_video(client, message):
    url = message.text
    yt = YouTube(url)
    stream = None
    
    # Assuming the user wants the highest resolution available
    # Modify this part to allow the user to choose a specific resolution
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    
    if stream:
        download_message = await message.reply("Downloading video, please wait...")
        file_path = stream.download()
        file_name = os.path.basename(file_path)
        
        await download_message.edit("Uploading video...")
        await client.send_video(message.chat.id, video=file_path, caption=f"Here's your video: {yt.title}")
        
        # Clean up after sending the video
        os.remove(file_path)
        await download_message.delete()
    else:
        await message.reply("Could not find a suitable stream to download. Please try a different video or quality.")

# Run the bot
app.run()
