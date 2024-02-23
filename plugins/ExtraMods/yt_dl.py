import os
from pyrogram import Client, filters
import subprocess
import re

# Exact Code

@Client.on_message(filters.command(["yt", "youtube"]))
async def start(client, message):
    await message.reply("Welcome! Send me a YouTube link, and reply to my message with the desired quality (e.g., '720p', 'best', 'worst').")

@Client.on_message(filters.text & filters.regex(r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+'))
async def handle_link(client, message):
    yt_link = message.text
    chat_id = message.chat.id
    await message.reply("Received your link! Please reply with the desired quality (e.g., '720p', '480p', 'best', 'worst').", quote=True)

    # Wait for quality reply
    @Client.on_message(filters.text & filters.reply & filters.user(chat_id))
    async def download_video(client, message):
        quality = message.text
        temp_file_name = f"{chat_id}_video.mp4"
        
        # Using youtube-dl to download the video
        cmd = ['youtube-dl', '-f', quality, yt_link, '-o', temp_file_name]
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if process.returncode == 0:
            await message.reply_document(document=temp_file_name, caption="Here's your video!")
            os.remove(temp_file_name)
        else:
            await message.reply("Failed to download video. Please check the link or try a different quality.", quote=True)

