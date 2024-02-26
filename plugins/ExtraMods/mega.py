from pyrogram import Client, filters
from mega import Mega
import zipfile
import os
import math

# Your Telegram API ID, API hash, and bot token from BotFather
mega_email = 'abhyudbot@gmail.com'
mega_password = 'Abhyudshiva7'
mega = Mega()
m = mega.login()  # Login to Mega.nz

def unzip_file(zip_path, extract_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    os.remove(zip_path)  # Remove the zip file after extraction

def split_file(file_path, split_size=2000):
    # Split file into parts of split_size MB each
    # This is a placeholder function. You'll need to implement the logic to split large files
    pass

@Client.on_message(filters.command(["mg", "mega"]))
def send_welcome(client, message):
    message.reply_text("Welcome! Send me a Mega.nz link, and I'll download it for you. I can unzip zip files and handle large files by splitting them.")

@Client.on_message(filters.text & ~filters.command)
def download_from_mega(client, message):
    url = message.text
    if "mega.nz" in url:
        try:
            message.reply_text("Processing your request... Please be patient.")
            # Download file from Mega.nz
            download_path = m.download_url(url)
            # Check if the file is a zip file and unzip it
            if zipfile.is_zipfile(download_path):
                extract_dir = download_path.rsplit('.', 1)[0]
                if not os.path.exists(extract_dir):
                    os.makedirs(extract_dir)
                unzip_file(download_path, extract_dir)
                # Iterate through unzipped files, check size, and handle accordingly
                for file_name in os.listdir(extract_dir):
                    file_path = os.path.join(extract_dir, file_name)
                    # Implement logic to handle files, including splitting large files
            else:
                # Directly handle the downloaded file, including checking size and splitting if necessary
                pass
        except Exception as e:
            message.reply_text(f"An error occurred: {str(e)}")
    else:
        message.reply_text("Please send a valid Mega.nz link.")
