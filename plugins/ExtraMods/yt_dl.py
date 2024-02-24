from pyrogram import Client, filters
from pytube import YouTube
import os



@Client.on_message(filters.command(["yt"]))
async def start(client, message):
    await message.reply("Welcome! Send me a YouTube link, and I will provide you with quality options for download.")

@Client.on_message(filters.regex(r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu.be/)[^\s]{11}'))
async def send_qualities(client, message):
    url = message.text
    yt = YouTube(url)
    stream_qualities = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')
    qualities = [f"{stream.resolution}" for stream in stream_qualities]
    unique_qualities = sorted(set(qualities), reverse=True)
    await message.reply("Available qualities:\n" + "\n".join(unique_qualities) + "\nReply with the desired quality.")

@Client.on_message(filters.text & filters.incoming)
async def download_send_video(client, message):
    if message.reply_to_message and "Available qualities:" in message.reply_to_message.text:
        requested_quality = message.text
        url = message.reply_to_message.entities[0].url if message.reply_to_message.entities else message.reply_to_message.text.split('\n')[0]
        yt = YouTube(url)
        stream = yt.streams.filter(res=requested_quality, progressive=True, file_extension='mp4').first()
        if stream:
            temp_file_path = stream.download()
            await client.send_video(message.chat.id, video=temp_file_path, caption=f"Here's your video: {yt.title}")
            os.remove(temp_file_path)
        else:
            await message.reply("The requested quality is not available. Please choose another quality.")
    else:
        await message.reply("Please reply to the message with available qualities to select the desired quality.")

