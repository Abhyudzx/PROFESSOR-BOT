from pyrogram import Client, filters
import yt_dlp

# Your bot token from BotFather

def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',  # Save file as "video.mp4"
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return 'video.mp4'

@Client.on_message(filters.command("yt"))
def start(client, message):
    message.reply_text("Hello! Send me a YouTube video URL to download.")

@Client.on_message(filters.text)
def echo(client, message):
    try:
        video_url = message.text
        file_name = download_video(video_url)
        message.reply_video(video=file_name, caption="Here's your video!")
    except Exception as e:
        message.reply_text("An error occurred: " + str(e))
