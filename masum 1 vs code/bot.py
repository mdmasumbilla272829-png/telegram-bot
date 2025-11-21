import telebot

# Bot API Token
API_TOKEN = "8237313309:AAEXzBBsQq4dV1auo9pJN6OcM8SNyjYCgO0"
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Get user information
    user = message.from_user
    
    # Create welcome message with simple text
    welcome_text = """
╔═══════════════════════════════════════════╗
║                                           ║
║  ✨ 🎉 WELCOME TO PROFILE BOT 🎉 ✨    ║
║                                           ║
╚═══════════════════════════════════════════╝

     ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐

     👇 Click the button to see your profile 👇

     ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐
    """
    
    # Create reply keyboard with buttons
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = telebot.types.KeyboardButton("👤 View Profile")
    markup.add(btn1)
    
    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: message.text == "👤 View Profile")
def view_profile(message):
    user = message.from_user
    username = user.username if user.username else "Not Set"
    first_name = user.first_name if user.first_name else "Not Set"
    last_name = user.last_name if user.last_name else "Not Set"
    
    profile_text = f"""
╔═══════════════════════════════════════════╗
║                                           ║
║   📋 USER PROFILE INFORMATION 📋         ║
║                                           ║
╚═══════════════════════════════════════════╝

     ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐

     👤  Original Username: @{username}
     
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     
     📝  First Name: {first_name}
     
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     
     📝  Last Name: {last_name}
     
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     
     🆔  User ID: {user.id}
     
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     
     ✅  Account Status: Active

     ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐

     ✨ *Profile loaded successfully!* ✨
    """
    
    bot.send_message(
        message.chat.id,
        profile_text,
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    pass

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
