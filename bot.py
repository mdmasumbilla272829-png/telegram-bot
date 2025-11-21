import telebot
import json
import os
from datetime import datetime

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
    
    # Create welcome message with simple text
    welcome_text = """
╔═══════════════════════════════════════════╗
║  ✨ 🎉 WELCOME TO PROFILE BOT 🎉 ✨   ║
╚═══════════════════════════════════════════╝

👇 Click the button to see your profile 👇
    """
    
    # Create reply keyboard with buttons
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = telebot.types.KeyboardButton("👤 View Profile")
    btn2 = telebot.types.KeyboardButton("🔔 Notifications")
    markup.add(btn1, btn2)
    
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
║   📋 USER PROFILE INFORMATION 📋         ║
╚═══════════════════════════════════════════╝

👤 Username: @{username}
📝 First Name: {first_name}
📝 Last Name: {last_name}
🆔 User ID: {user.id}
✅ Account Status: Active

💰 BALANCE INFORMATION

💵 Dollar: 0.00 USD
🇩🇰 DK: 0.00 DK
💎 Diamond: 0.00 💎
🪙 Coin: 0.00 🪙

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
        show_admin_panel(message)
    elif message.text == "📊 User Statistics":
        show_user_stats(message)
    elif message.text == "💰 Total Balance":
        show_total_balance(message)
    elif message.text == "📢 Send Notification":
        send_notification_prompt(message)
    elif message.text == "🔔 Notifications":
        show_notifications(message)
    else:
        pass

def show_admin_panel(message):
    admin_text = """
╔═══════════════════════════════════════════╗
║     🛡️ ADMIN PANEL 🛡️                   ║
╚═══════════════════════════════════════════╝

Select an option below:
    """
    
    # Create reply keyboard with admin buttons
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = telebot.types.KeyboardButton("📊 User Statistics")
    btn2 = telebot.types.KeyboardButton("💰 Total Balance")
    btn3 = telebot.types.KeyboardButton("📢 Send Notification")
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(message.chat.id, admin_text, reply_markup=markup, parse_mode="Markdown")

def show_user_stats(message):
    users = load_users()
    
    # Calculate statistics
    total_users = len(users)
    active_users = len([u for u in users.values() if u.get('status') == 'active'])
    inactive_users = total_users - active_users
    
    stats_text = f"""
╔═══════════════════════════════════════════╗
║     📊 USER STATISTICS 📊                ║
╚═══════════════════════════════════════════╝

👥 Total Users: {total_users}
✅ Active Users: {active_users}
❌ Inactive Users: {inactive_users}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ Statistics loaded! ✨
    """
    
    bot.send_message(message.chat.id, stats_text, parse_mode="Markdown")

def show_total_balance(message):
    users = load_users()
    
    # Calculate total balance
    total_dollar = sum(float(u.get('dollar', 0)) for u in users.values())
    total_dk = sum(float(u.get('dk', 0)) for u in users.values())
    total_diamond = sum(float(u.get('diamond', 0)) for u in users.values())
    total_coin = sum(float(u.get('coin', 0)) for u in users.values())
    
    balance_text = f"""
╔═══════════════════════════════════════════╗
║     💰 TOTAL BALANCE 💰                  ║
╚═══════════════════════════════════════════╝

💵 Total Dollar: {total_dollar:.2f} USD
🇩🇰 Total DK: {total_dk:.2f} DK
💎 Total Diamond: {total_diamond:.2f} 💎
🪙 Total Coin: {total_coin:.2f} 🪙

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ Balance loaded! ✨
    """
    
    bot.send_message(message.chat.id, balance_text, parse_mode="Markdown")

def show_notifications(message):
    notifications = load_notifications()
    
    if notifications:
        notification_text = """
╔═══════════════════════════════════════════╗
║     🔔 NOTIFICATIONS 🔔                  ║
╚═══════════════════════════════════════════╝

📬 Admin Messages:

"""
        for i, notif in enumerate(notifications[-5:], 1):  # Last 5 notifications
            notification_text += f"{i}. {notif['message']}\n   ({notif['time']})\n\n"
        
        notification_text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n✨ Stay updated! ✨"
    else:
        notification_text = """
╔═══════════════════════════════════════════╗
║     🔔 NOTIFICATIONS 🔔                  ║
╚═══════════════════════════════════════════╝

📬 No notifications yet

Check back later for updates! ✨
"""
    
    bot.send_message(message.chat.id, notification_text, parse_mode="Markdown")

def send_notification_prompt(message):
    prompt_text = """
╔═══════════════════════════════════════════╗
║   📢 SEND NOTIFICATION 📢                ║
╚═══════════════════════════════════════════╝

Type your notification message:
(This will be sent to ALL users)

⚠️ Be careful - all users will receive this!
"""
    
    msg = bot.send_message(message.chat.id, prompt_text, parse_mode="Markdown")
    bot.register_next_step_handler(msg, broadcast_notification)

def broadcast_notification(message):
    notification_msg = message.text
    
    # Add to notifications database
    add_notification(notification_msg)
    
    # Get all users
    users = load_users()
    
    broadcast_text = f"""
╔═══════════════════════════════════════════╗
║     📢 ADMIN NOTIFICATION 📢             ║
╚═══════════════════════════════════════════╝

{notification_msg}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    # Send to all users
    sent_count = 0
    for user_id in users.keys():
        try:
            bot.send_message(int(user_id), broadcast_text, parse_mode="Markdown")
            sent_count += 1
        except:
            pass
    
    # Send confirmation to admin
    confirmation = f"""
✅ Notification sent successfully!

Sent to {sent_count} user(s)
Message: {notification_msg}
"""
    
    bot.send_message(message.chat.id, confirmation)

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

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
