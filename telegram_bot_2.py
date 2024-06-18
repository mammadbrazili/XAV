from telegram import Update, ChatMember
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
from pytube import YouTube
import ssl
import os

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = '7431841859:AAFfJvXcI2ADSNq2XhngU-rG2FnFuFvbFPg'
CHANNEL_ID = '@Joozitrade'  # Replace with your channel's username

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # Check if the user is a member of the channel
    member_status = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
    if member_status.status in ['member', 'administrator', 'creator']:
        await update.message.reply_text('خب خوش اومدی! سریع لینک رو بفرست بیاد!')
    else:
        await update.message.reply_text(f'برای استفاده از ربات ابتدا باید عضو کانال شوید. پس از عضویت، دستور /start را دوباره ارسال کنید.\n {CHANNEL_ID}')

def download_youtube_video(url, save_path='.'):
    try:
        # Set default SSL context to use certifi's CA bundle
        ssl._create_default_https_context = ssl._create_unverified_context
        
        # Create YouTube object
        yt = YouTube(url)

        # Get the highest resolution stream available
        stream = yt.streams.get_lowest_resolution()

        # Download the video
        print(f'دارم دانلود میکنم: {yt.title}')
        video_path = stream.download(save_path)
        print(f'خب دانلود تموم شد. میرم برای آپلود {yt.title}')
        return video_path

    except Exception as e:
        print(f'An error occurred: {e}')
        return None

async def download_video(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    member_status = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
    
    if member_status.status not in ['member', 'administrator', 'creator']:
        await update.message.reply_text(f'برای استفاده از ربات ابتدا باید عضو کانال شوید.\n {CHANNEL_ID}')
        return
    
    url = update.message.text
    chat_id = update.message.chat_id
    try:
        await update.message.reply_text('دارم دانلود میکنم...')
        await context.bot.send_chat_action(chat_id=chat_id, action='upload_video')
        
        video_path = download_youtube_video(url)
        
        if video_path:
            await update.message.reply_text('دارم اپلود میکنم...')
            await context.bot.send_chat_action(chat_id=chat_id, action='upload_video')
            await context.bot.send_video(chat_id=chat_id, video=open(video_path, 'rb'))
            os.remove(video_path)  # Clean up the downloaded file
        else:
            await update.message.reply_text('Failed to download the video. Please try again.')
            
    except Exception as e:
        await update.message.reply_text(f'An error occurred: {e}')

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    application.run_polling()

if __name__ == '__main__':
    main()