import telebot
import json
import os
from datetime import datetime
from admin_panel import (
    show_admin_panel, show_user_stats, show_total_balance, 
    send_notification_prompt, broadcast_notification,
    search_user_prompt, select_balance_type, get_balance_amount,
    show_delete_notifications_menu, delete_by_date_range_prompt, delete_all_notifications_prompt
)

# Bot API Token
API_TOKEN = "8024197741:AAGmDSi41XljyEmB2DcnauNtRU0lTBiXStg"
bot = telebot.TeleBot(API_TOKEN)

# Admin Password
ADMIN_PASSWORD = "Mo321321@@###"

# Database file
DB_FILE = "users_data.json"
NOTIFICATIONS_FILE = "notifications.json"

# Initialize database
def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({}, f)
    if not os.path.exists(NOTIFICATIONS_FILE):
        with open(NOTIFICATIONS_FILE, 'w') as f:
            json.dump([], f)

# Load users data
def load_users():
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

# Save users data
def save_users(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Load notifications
def load_notifications():
    try:
        with open(NOTIFICATIONS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

# Save notifications
def save_notifications(data):
    with open(NOTIFICATIONS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Add notification
def add_notification(message_text):
    notifications = load_notifications()
    notifications.append({
        "message": message_text,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_notifications(notifications)

# Add or update user
def add_user(user_id, username, first_name, last_name):
    users = load_users()
    if str(user_id) not in users:
        users[str(user_id)] = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "status": "active",
            "dollar": 0.0,
            "dk": 0.0,
            "diamond": 0.0,
            "coin": 0.0,
            "joined": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_users(users)

init_db()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Get user information
    user = message.from_user
    
    # Save user to database
    add_user(user.id, user.username, user.first_name, user.last_name)
    
    # Create welcome message with ultra unique design
    welcome_text = f"""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃                                                       ┃
┃     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    ┃
┃     ░  ██████╗ ██████╗ ████████╗███████╗██╗  ██╗ ░   ┃
┃     ░  ██╔══██╗██╔═══██╗╚══██╔══╝██╔════╝╚██╗██╔╝ ░   ┃
┃     ░  ██████╔╝██║   ██║   ██║   █████╗   ╚███╔╝  ░   ┃
┃     ░  ██╔══██╗██║   ██║   ██║   ██╔══╝   ██╔██╗  ░   ┃
┃     ░  ██║  ██║╚██████╔╝   ██║   ███████╗██╔╝ ██╗ ░   ┃
┃     ░  ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝ ░   ┃
┃     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    ┃
┃                                                       ┃
┃  ═══════════════════════════════════════════════════  ┃
┃                                                       ┃
┃     ✨ ═══ ✨ ═══ ✨ ═══ ✨ ═══ ✨ ═══ ✨              ┃
┃                                                       ┃
┃        🎊  W E L C O M E  🎊                        ┃
┃                                                       ┃
┃     ✨ ═══ ✨ ═══ ✨ ═══ ✨ ═══ ✨ ═══ ✨              ┃
┃                                                       ┃
┃  ═══════════════════════════════════════════════════  ┃
┃                                                       ┃
┃     🌟━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🌟     ┃
┃                                                       ┃
┃        👋  Hello, {user.first_name or 'User'}!  👋              ┃
┃                                                       ┃
┃     🌟━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🌟     ┃
┃                                                       ┃
┃  ═══════════════════════════════════════════════════  ┃
┃                                                       ┃
┃  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ┃
┃  ▓                                                   ▓  ┃
┃  ▓  🎯  W H A T   Y O U   C A N   D O  🎯          ▓  ┃
┃  ▓                                                   ▓  ┃
┃  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ┃
┃                                                       ┃
┃     ▸ 👤  View Your Amazing Profile                  ┃
┃     ▸ 🔔  Check Latest Notifications                 ┃
┃     ▸ 💎  Manage Your Balance                        ┃
┃     ▸ ⚡  Fast & Secure                               ┃
┃                                                       ┃
┃  ═══════════════════════════════════════════════════  ┃
┃                                                       ┃
┃     💫━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━💫     ┃
┃                                                       ┃
┃        🚀  Use Buttons Below to Start!  🚀          ┃
┃                                                       ┃
┃     💫━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━💫     ┃
┃                                                       ┃
┃  ═══════════════════════════════════════════════════  ┃
┃                                                       ┃
┃     ❤️━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━❤️     ┃
┃                                                       ┃
┃        Made with 💖  for Amazing People              ┃
┃                                                       ┃
┃     ❤️━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━❤️     ┃
┃                                                       ┃
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
    """
    
    # Create reply keyboard with beautiful buttons
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = telebot.types.KeyboardButton("👤 View Profile")
    btn2 = telebot.types.KeyboardButton("🔔 Notifications")
    btn3 = telebot.types.KeyboardButton("ℹ️ Help")
    markup.add(btn1, btn2)
    markup.add(btn3)
    
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
    
    users = load_users()
    user_data = users.get(str(user.id), {})
    
    dollar = user_data.get('dollar', 0.0)
    dk = user_data.get('dk', 0.0)
    diamond = user_data.get('diamond', 0.0)
    coin = user_data.get('coin', 0.0)
    joined_date = user_data.get('joined', 'N/A')
    
    profile_text = f"""
╔═══════════════════════════════════════════╗
║  📋  YOUR PROFILE  📋                    ║
╚═══════════════════════════════════════════╝

👤 Personal Information:
  🆔 Username: @{username}
  📝 First Name: {first_name}
  📝 Last Name: {last_name}
  🔢 User ID: `{user.id}`
  ✅ Status: 🟢 Active
  📅 Joined: {joined_date}

💰 Your Balance:
  💵 Dollar:  ${dollar:.2f} USD
  🇩🇰 DK:     {dk:.2f} DK
  💎 Diamond: {diamond:.2f} 💎
  🪙 Coin:    {coin:.2f} 🪙

✨ Profile loaded successfully! ✨
    """
    
    bot.send_message(
        message.chat.id,
        profile_text,
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    # Check for admin password
    if message.text == ADMIN_PASSWORD:
        show_admin_panel(message, bot, load_users)
    elif message.text == "📊 User Statistics":
        show_user_stats(message, bot, load_users)
    elif message.text == "💰 Total Balance":
        show_total_balance(message, bot, load_users)
    elif message.text == "📢 Send Notification":
        send_notification_prompt(message, bot, load_users, load_notifications, add_notification)
    elif message.text == "🔔 Notifications":
        show_notifications(message)
    elif message.text == "🔍 Search User":
        search_user_prompt(message, bot, load_users, save_users, load_notifications, add_notification)
    elif message.text == "🗑️ Delete Notifications":
        show_delete_notifications_menu(message, bot, load_notifications, save_notifications)
    elif message.text == "📅 Delete by Date Range":
        delete_by_date_range_prompt(message, bot, load_notifications, save_notifications)
    elif message.text == "🗑️ Delete All Notifications":
        delete_all_notifications_prompt(message, bot, load_notifications, save_notifications)
    elif message.text == "🔙 Back to Admin Panel":
        show_admin_panel(message, bot, load_users)
    elif message.text and message.text.startswith("➕ Add Balance: "):
        # Extract user_id from button text
        user_id = message.text.split(": ")[1]
        from admin_panel import select_balance_type
        select_balance_type(message, bot, user_id, "add", load_users, save_users, load_notifications, add_notification)
    elif message.text and message.text.startswith("➖ Remove Balance: "):
        # Extract user_id from button text
        user_id = message.text.split(": ")[1]
        from admin_panel import select_balance_type
        select_balance_type(message, bot, user_id, "remove", load_users, save_users, load_notifications, add_notification)
    elif message.text and ("Add: " in message.text or "Remove: " in message.text):
        # Handle balance type selection (💵 Dollar Add: user_id, etc.)
        parts = message.text.split(": ")
        if len(parts) == 2:
            balance_part = parts[0]
            user_id = parts[1]
            
            # Extract balance type and action
            if "💵 Dollar" in balance_part:
                balance_type = "dollar"
                action_type = "add" if "Add" in balance_part else "remove"
            elif "🇩🇰 DK" in balance_part:
                balance_type = "dk"
                action_type = "add" if "Add" in balance_part else "remove"
            elif "💎 Diamond" in balance_part:
                balance_type = "diamond"
                action_type = "add" if "Add" in balance_part else "remove"
            elif "🪙 Coin" in balance_part:
                balance_type = "coin"
                action_type = "add" if "Add" in balance_part else "remove"
            else:
                balance_type = None
                action_type = None
            
            if balance_type and action_type:
                from admin_panel import get_balance_amount
                # Show prompt for amount
                action_text = "Add" if action_type == "add" else "Remove"
                balance_emoji = {"dollar": "💵", "dk": "🇩🇰", "diamond": "💎", "coin": "🪙"}[balance_type]
                balance_name = balance_type.capitalize()
                
                text = f"""
╔═══════════════════════════════════════════╗
║  {balance_emoji}  {action_text.upper()} {balance_name.upper()}  {balance_emoji}        ║
╚═══════════════════════════════════════════╝

👤 User ID: {user_id}
💰 Balance Type: {balance_name}

📝 Step 1: Enter Amount
  Enter the amount to {action_text.lower()}
  (Only numbers, e.g., 100 or 50.5)

👇 Type the amount now 👇
"""
                msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
                bot.register_next_step_handler(
                    msg,
                    lambda m: get_balance_amount(m, bot, user_id, action_type, balance_type, load_users, save_users, load_notifications, add_notification)
                )
    elif message.text == "ℹ️ Help":
        show_help(message)
    else:
        error_text = """
╔═══════════════════════════════════════════╗
║  ❌  UNKNOWN COMMAND  ❌                  ║
╚═══════════════════════════════════════════╝

❌ Unknown command!
💡 Please use buttons below or /start
"""
        bot.send_message(
            message.chat.id,
            error_text,
            parse_mode="Markdown"
        )

# Admin panel functions moved to admin_panel.py

def show_notifications(message):
    notifications = load_notifications()
    
    if notifications:
        notification_text = """
╔═══════════════════════════════════════════╗
║  🔔  NOTIFICATIONS  🔔                   ║
╚═══════════════════════════════════════════╝

📬 Latest Admin Messages:

"""
        for i, notif in enumerate(notifications[-5:], 1):  # Last 5 notifications
            notification_text += f"{i}. 📝 {notif['message']}\n   ⏰ {notif['time']}\n\n"
        
        notification_text += "✨ Stay updated! ✨"
    else:
        notification_text = """
╔═══════════════════════════════════════════╗
║  🔔  NOTIFICATIONS  🔔                   ║
╚═══════════════════════════════════════════╝

📬 No notifications yet

📭 Your notification inbox is empty
⏳ Check back later for updates!

✨ We'll notify you soon! ✨
"""
    
    bot.send_message(message.chat.id, notification_text, parse_mode="Markdown")

# Notification functions moved to admin_panel.py

def search_prompt(message):
    search_text = """
╔═══════════════════════════════════════════╗
║     🔍 SEARCH USER 🔍                    ║
╚═══════════════════════════════════════════╝

Enter a username to search:
(Type the username without @)

Example: Mo321321

Type your search query below:
    """
    
    msg = bot.send_message(message.chat.id, search_text, parse_mode="Markdown")
    bot.register_next_step_handler(msg, search_user)

def show_help(message):
    help_text = """
╔═══════════════════════════════════════════╗
║  ℹ️  HELP & GUIDE  ℹ️                     ║
╚═══════════════════════════════════════════╝

🎯 Available Commands:
  /start - Start bot & see welcome
  👤 View Profile - Check profile & balance
  🔔 Notifications - View admin messages

💡 Tips:
  • Use buttons for easy navigation
  • Your profile is automatically saved
  • Check notifications regularly

🆘 Need Help?
  Contact admin for any issues or questions

✨ We're here to help! ✨
"""
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

def search_user(message):
    search_query = message.text.lower()
    users = load_users()
    
    results = []
    for user_id, user_data in users.items():
        if search_query in str(user_data.get('username', '')).lower() or \
           search_query in str(user_data.get('first_name', '')).lower():
            results.append(user_data)
    
    if results:
        result_text = f"""
╔═══════════════════════════════════════════╗
║     🔍 SEARCH RESULTS 🔍                 ║
╚═══════════════════════════════════════════╝

Found {len(results)} result(s):

"""
        for i, user in enumerate(results, 1):
            result_text += f"""
{i}. Username: @{user.get('username', 'N/A')}
   Name: {user.get('first_name', 'N/A')} {user.get('last_name', 'N/A')}
   Status: {user.get('status', 'active')}
   
"""
        result_text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    else:
        result_text = f"""
╔═══════════════════════════════════════════╗
║     🔍 SEARCH RESULTS 🔍                 ║
╚═══════════════════════════════════════════╝

No users found for: "{search_query}"

Try searching with another term!
"""
    
    bot.send_message(message.chat.id, result_text, parse_mode="Markdown")

# Callback query handler removed - now using reply keyboard buttons

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
