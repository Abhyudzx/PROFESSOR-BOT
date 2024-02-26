from pyrogram import Client, filters
import yt_dlp
import os

# Your Telegram API ID, API hash, and bot token from BotFather

def download_youtube_video(url, download_path="downloads/"):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': download_path + '%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
        return filename

# Placeholder for a function to split large files into parts smaller than 2GB
def split_file_into_parts(filename):
    # This is a placeholder function. You need to implement the actual file splitting.
    # The function should return a list of filenames for the parts.
    return ["part1.mp4", "part2.mp4"]

@Client.on_message(filters.command(["yt", "search"]))
def send_welcome(client, message):
    message.reply_text("Welcome! Send me a YouTube video link, and I'll download it for you. If the video is larger than 2GB, I'll split it into parts and upload them.")

@Client.on_message(filters.text & ~filters.command)
def handle_video_download(client, message):
    url = message.text
    try:
        message.reply_text("Downloading video... Please wait.")
        filename = download_youtube_video(url)
        filesize = os.path.getsize(filename)

        if filesize > 2 * 1024 * 1024 * 1024:  # File is larger than 2GB
            message.reply_text("The file is larger than 2GB. Splitting and uploading parts. It will take time...")
            parts = split_file_into_parts(filename)
            for part in parts:
                message.reply_document(document=part)
                os.remove(part)  # Clean up after uploading
        else:
            message.reply_document(document=filename)
        
        os.remove(filename)  # Clean up the original file if it's been split or already sent

    except Exception as e:
        message.reply_text(f"An error occurred: {str(e)}")
