import os
import re
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import instaloader


TELEGRAM_TOKEN = '7359662963:AAHJJ-VWfTG1pl385irJI-tpAqWZ9JRoqYU'
CHANNEL_ID = '@Joozitrade'  

# تنظیمات instaloader.
L = instaloader.Instaloader()

def is_user_in_channel(bot: Bot, user_id: int) -> bool:
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    bot = context.bot
    
    if is_user_in_channel(bot, user_id):
        update.message.reply_text("سلام! لینک پست اینستاگرام را برای من بفرستید.")
    else:
        update.message.reply_text("لطفاً ابتدا عضو کانال ما شوید: @Joozitrade")

def download_instagram_video(url: str) -> str:
    try:
        # استخراج شناسه پست از URL
        shortcode = re.search(r'(?:https?:\/\/www\.instagram\.com\/(?:p|tv|reel)\/)([A-Za-z0-9_-]+)', url).group(1)
        
        # دانلود پست اینستاگرام
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        # بررسی وجود ویدیو در پست
        if post.is_video:
            L.download_post(post, target=shortcode)
            
            # پیدا کردن فایل ویدیو
            video_file = None
            for file in os.listdir(shortcode):
                if file.endswith('.mp4'):
                    video_file = os.path.join(shortcode, file)
                    break
            
            return video_file
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    bot = context.bot
    text = update.message.text
    
    if is_user_in_channel(bot, user_id):
        if 'instagram.com' in text:
            update.message.reply_text("در حال دانلود ویدیو، لطفا صبر کنید...")
            
            try:
                video_file = download_instagram_video(text)
                
                if video_file:
                    with open(video_file, 'rb') as video:
                        update.message.reply_video(video=video)
       
                else:
                    update.message.reply_text("خطایی در دانلود ویدیو رخ داد یا این پست ویدیویی ندارد.")
            except Exception as e:
                update.message.reply_text(f"خطایی رخ داد: {e}")
        else:
            update.message.reply_text("لطفا یک لینک معتبر اینستاگرام ارسال کنید.")
    else:
        update.message.reply_text("لطفاً ابتدا عضو کانال ما شوید: Joozitrade")

