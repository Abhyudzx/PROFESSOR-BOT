from pyrogram import Client, filters
from mega import Mega
import os

# Fill in your details

mega_email = 'abhyudbot@gmail.com'
mega_password = 'Abhyudshiva7'


mega = Mega()
m = mega.login(mega_email, mega_password)

@Client.on_message(filters.command(["mega", "mg"]))
async def start(client, message):
    await message.reply("Welcome! Send me a Mega.nz link, and I will attempt to download and send the file back to you.")

@Client.on_message(filters.text)
async def handle_link(client, message):
    if "mega.nz" in message.text:
        try:
            # Attempt to download the file from the Mega.nz link
            info = m.get_public_url_info(message.text)
            filename = info['name']
            temp_download_path = m.download_url(message.text)
            
            # Send the file back to the user
            await message.reply_document(document=temp_download_path, caption=f"Here's your file: {filename}")
            
            # Remove the file after sending it
            os.remove(temp_download_path)
        except Exception as e:
            await message.reply(f"Failed to download: {str(e)}")
    else:
        await message.reply("Please send a valid Mega.nz link.")
