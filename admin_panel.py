import telebot
from datetime import datetime

# Import database functions from bot.py
# We'll pass these as parameters or import them

def show_admin_panel(message, bot, load_users_func):
    """Display admin panel"""
    admin_text = """
╔═══════════════════════════════════════════╗
║  🛡️  ADMIN PANEL  🛡️                    ║
╚═══════════════════════════════════════════╝

👑 Authorized Admin Access

🎯 Admin Controls:
  📊 View User Statistics
  💰 Check Total Balance
  📢 Send Notifications to All Users
  🔍 Search User & Manage Balance
  🗑️ Delete Notification History

⚠️ Admin Access - Use with Caution!

✨ Select an option below ✨
    """
    
    # Create reply keyboard with admin buttons
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = telebot.types.KeyboardButton("🔍 Search User")
    btn2 = telebot.types.KeyboardButton("📊 User Statistics")
    btn3 = telebot.types.KeyboardButton("💰 Total Balance")
    btn4 = telebot.types.KeyboardButton("📢 Send Notification")
    btn5 = telebot.types.KeyboardButton("🗑️ Delete Notifications")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    
    bot.send_message(message.chat.id, admin_text, reply_markup=markup, parse_mode="Markdown")

def show_user_stats(message, bot, load_users_func):
    """Display user statistics"""
    users = load_users_func()
    
    # Calculate statistics
    total_users = len(users)
    active_users = len([u for u in users.values() if u.get('status') == 'active'])
    inactive_users = total_users - active_users
    
    active_rate = ((active_users/total_users*100) if total_users > 0 else 0)
    progress_bar = "█" * int(active_rate / 10) + "░" * (10 - int(active_rate / 10))
    
    stats_text = f"""
╔═══════════════════════════════════════════╗
║  📊  USER STATISTICS  📊                 ║
╚═══════════════════════════════════════════╝

👥 User Overview:
  📈 Total Users:     {total_users} 👤
  ✅ Active Users:    {active_users} 🟢
  ❌ Inactive Users:  {inactive_users} 🔴

📊 Activity Ratio:
  Active Rate: {active_rate:.1f}% [{progress_bar}]

✨ Statistics loaded successfully! ✨
    """
    
    bot.send_message(message.chat.id, stats_text, parse_mode="Markdown")

def show_total_balance(message, bot, load_users_func):
    """Display total balance"""
    users = load_users_func()
    
    # Calculate total balance
    total_dollar = sum(float(u.get('dollar', 0)) for u in users.values())
    total_dk = sum(float(u.get('dk', 0)) for u in users.values())
    total_diamond = sum(float(u.get('diamond', 0)) for u in users.values())
    total_coin = sum(float(u.get('coin', 0)) for u in users.values())
    
    total_assets = total_dollar + total_dk + total_diamond + total_coin
    
    balance_text = f"""
╔═══════════════════════════════════════════╗
║  💰  TOTAL BALANCE  💰                   ║
╚═══════════════════════════════════════════╝

💵 Currency Breakdown:
  💵 Dollar:  ${total_dollar:,.2f} USD
  🇩🇰 DK:     {total_dk:,.2f} DK
  💎 Diamond: {total_diamond:,.2f} 💎
  🪙 Coin:    {total_coin:,.2f} 🪙

📊 Summary:
  💰 Total Assets: ${total_assets:,.2f}

✨ Balance loaded successfully! ✨
    """
    
    bot.send_message(message.chat.id, balance_text, parse_mode="Markdown")

def send_notification_prompt(message, bot, load_users_func, load_notifications_func, add_notification_func):
    """Prompt admin to send notification"""
    prompt_text = """
╔═══════════════════════════════════════════╗
║  📢  SEND NOTIFICATION  📢               ║
╚═══════════════════════════════════════════╝

📝 Instructions:
  Type your notification message below
  This will be sent to ALL users!

⚠️ Warning:
  🔴 All users will receive this message
  🔴 This action cannot be undone
  🔴 Make sure your message is correct!

👇 Type your message now 👇
"""
    
    msg = bot.send_message(message.chat.id, prompt_text, parse_mode="Markdown")
    bot.register_next_step_handler(msg, lambda m: broadcast_notification(m, bot, load_users_func, add_notification_func))

def broadcast_notification(message, bot, load_users_func, add_notification_func):
    """Broadcast notification to all users"""
    notification_msg = message.text
    
    # Add to notifications database
    add_notification_func(notification_msg)
    
    # Get all users
    users = load_users_func()
    
    broadcast_text = f"""
╔═══════════════════════════════════════════╗
║  📢  ADMIN NOTIFICATION  📢              ║
╚═══════════════════════════════════════════╝

📝 Message:
{notification_msg}

⏰ Details:
  📅 Date: {datetime.now().strftime("%Y-%m-%d")}
  🕐 Time: {datetime.now().strftime("%H:%M:%S")}

✨ Stay tuned for more updates! ✨
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
╔═══════════════════════════════════════════╗
║  ✅  NOTIFICATION SENT!  ✅              ║
╚═══════════════════════════════════════════╝

📊 Delivery Status:
  ✅ Successfully sent to: {sent_count} user(s)
  📝 Message: {notification_msg}
  ⏰ Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

✨ All users have been notified! ✨
"""
    
    bot.send_message(message.chat.id, confirmation)

def search_user_prompt(message, bot, load_users_func, save_users_func, load_notifications_func, add_notification_func):
    """Prompt admin to search for a user"""
    search_text = """
╔═══════════════════════════════════════════╗
║  🔍  SEARCH USER  🔍                     ║
╚═══════════════════════════════════════════╝

📝 Instructions:
  Enter username (without @) or User ID
  Example: Tasklora or 6351343802

👇 Type username or ID to search 👇
"""
    msg = bot.send_message(message.chat.id, search_text, parse_mode="Markdown")
    bot.register_next_step_handler(msg, lambda m: search_user_handler(m, bot, load_users_func, save_users_func, load_notifications_func, add_notification_func))

def search_user_handler(message, bot, load_users_func, save_users_func, load_notifications_func, add_notification_func):
    """Handle user search"""
    search_query = message.text.strip()
    users = load_users_func()
    
    found_user = None
    found_user_id = None
    
    # Search by user ID
    if search_query.isdigit():
        if search_query in users:
            found_user = users[search_query]
            found_user_id = search_query
    else:
        # Search by username
        search_query_lower = search_query.lower()
        for user_id, user_data in users.items():
            username = str(user_data.get('username', '')).lower()
            if search_query_lower in username or search_query_lower == username.replace('@', ''):
                found_user = user_data
                found_user_id = user_id
                break
    
    if found_user and found_user_id:
        # Display user details
        display_user_details(message, bot, found_user_id, found_user, load_users_func, save_users_func, load_notifications_func, add_notification_func)
    else:
        error_text = f"""
╔═══════════════════════════════════════════╗
║  ❌  USER NOT FOUND  ❌                  ║
╚═══════════════════════════════════════════╝

❌ No user found for: "{search_query}"

💡 Try searching with:
  • Username (without @)
  • User ID

🔍 Search again or go back to admin panel
"""
        bot.send_message(message.chat.id, error_text, parse_mode="Markdown")

def display_user_details(message, bot, user_id, user_data, load_users_func, save_users_func, load_notifications_func, add_notification_func):
    """Display user details with balance management options"""
    username = user_data.get('username', 'Not Set')
    first_name = user_data.get('first_name', 'Not Set')
    last_name = user_data.get('last_name', 'Not Set')
    dollar = float(user_data.get('dollar', 0))
    dk = float(user_data.get('dk', 0))
    diamond = float(user_data.get('diamond', 0))
    coin = float(user_data.get('coin', 0))
    status = user_data.get('status', 'active')
    joined = user_data.get('joined', 'N/A')
    
    user_details = f"""
╔═══════════════════════════════════════════╗
║  👤  USER DETAILS  👤                   ║
╚═══════════════════════════════════════════╝

👤 Personal Information:
  🆔 Username: @{username}
  📝 First Name: {first_name}
  📝 Last Name: {last_name}
  🔢 User ID: {user_id}
  ✅ Status: {status}
  📅 Joined: {joined}

💰 Current Balance:
  💵 Dollar:  ${dollar:.2f} USD
  🇩🇰 DK:     {dk:.2f} DK
  💎 Diamond: {diamond:.2f} 💎
  🪙 Coin:    {coin:.2f} 🪙

✨ Select an action below ✨
"""
    
    # Create reply keyboard for balance management
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = telebot.types.KeyboardButton(f"➕ Add Balance: {user_id}")
    btn2 = telebot.types.KeyboardButton(f"➖ Remove Balance: {user_id}")
    btn3 = telebot.types.KeyboardButton("🔙 Back to Admin Panel")
    markup.add(btn1, btn2)
    markup.add(btn3)
    
    bot.send_message(message.chat.id, user_details, reply_markup=markup, parse_mode="Markdown")

# Callback handlers removed - now using reply keyboard buttons

def select_balance_type(message, bot, user_id, action_type, load_users_func, save_users_func, load_notifications_func, add_notification_func):
    """Let admin select balance type"""
    action_text = "Add" if action_type == "add" else "Remove"
    action_emoji = "➕" if action_type == "add" else "➖"
    
    text = f"""
╔═══════════════════════════════════════════╗
║  {action_emoji}  {action_text.upper()} BALANCE  {action_emoji}            ║
╚═══════════════════════════════════════════╝

👤 User ID: {user_id}

💰 Select Balance Type:

👇 Choose which balance to {action_text.lower()} 👇
"""
    
    # Create reply keyboard for balance type selection
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = telebot.types.KeyboardButton(f"💵 Dollar {action_text}: {user_id}")
    btn2 = telebot.types.KeyboardButton(f"🇩🇰 DK {action_text}: {user_id}")
    btn3 = telebot.types.KeyboardButton(f"💎 Diamond {action_text}: {user_id}")
    btn4 = telebot.types.KeyboardButton(f"🪙 Coin {action_text}: {user_id}")
    btn5 = telebot.types.KeyboardButton("🔙 Back to Admin Panel")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

# Balance type callback handler removed - now using reply keyboard buttons

def get_balance_amount(message, bot, user_id, action_type, balance_type, load_users_func, save_users_func, load_notifications_func, add_notification_func):
    """Get amount from admin"""
    try:
        amount = float(message.text.strip())
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        # Store amount and ask for reason
        action_text = "Add" if action_type == "add" else "Remove"
        balance_emoji = {"dollar": "💵", "dk": "🇩🇰", "diamond": "💎", "coin": "🪙"}[balance_type]
        balance_name = balance_type.capitalize()
        
        text = f"""
╔═══════════════════════════════════════════╗
║  📝  ENTER REASON  📝                    ║
╚═══════════════════════════════════════════╝

👤 User ID: {user_id}
💰 Balance Type: {balance_name}
💵 Amount: {amount}

📝 Step 2: Enter Reason
  Why are you {action_text.lower()}ing this balance?
  (This message will be sent to user)

👇 Type the reason/message now 👇
"""
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
        
        # Store context and get reason
        bot.register_next_step_handler(
            message,
            lambda m: get_balance_reason(m, bot, user_id, action_type, balance_type, amount, load_users_func, save_users_func, load_notifications_func, add_notification_func)
        )
    except ValueError:
        error_text = """
╔═══════════════════════════════════════════╗
║  ❌  INVALID AMOUNT  ❌                  ║
╚═══════════════════════════════════════════╝

❌ Invalid amount entered!

💡 Please enter a valid number
   Example: 100 or 50.5

🔍 Try again
"""
        bot.send_message(message.chat.id, error_text, parse_mode="Markdown")

def get_balance_reason(message, bot, user_id, action_type, balance_type, amount, load_users_func, save_users_func, load_notifications_func, add_notification_func):
    """Get reason and process balance update"""
    reason = message.text.strip()
    
    # Load users and update balance
    users = load_users_func()
    
    if user_id not in users:
        bot.send_message(message.chat.id, "❌ User not found!")
        return
    
    user_data = users[user_id]
    current_balance = float(user_data.get(balance_type, 0))
    
    action_text = "Added" if action_type == "add" else "Removed"
    balance_emoji = {"dollar": "💵", "dk": "🇩🇰", "diamond": "💎", "coin": "🪙"}[balance_type]
    balance_name = balance_type.capitalize()
    
    # Update balance
    if action_type == "add":
        new_balance = current_balance + amount
    else:
        new_balance = max(0, current_balance - amount)  # Don't go below 0
    
    user_data[balance_type] = new_balance
    users[user_id] = user_data
    save_users_func(users)
    
    # Send notification ONLY to the specific user (NOT to global notification database)
    # This ensures the message goes only to the user whose balance was updated
    try:
        user_notification = f"""
╔═══════════════════════════════════════════╗
║  💰  BALANCE UPDATE  💰                  ║
╚═══════════════════════════════════════════╝

{balance_emoji} {balance_name}: {action_text} {amount}

📝 Reason: {reason}

💰 New Balance: {new_balance:.2f}

⏰ Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

✨ Thank you! ✨
"""
        bot.send_message(int(user_id), user_notification, parse_mode="Markdown")
    except Exception as e:
        # If user blocked the bot or other error, just pass
        pass
    
    # Send confirmation to admin
    confirmation = f"""
╔═══════════════════════════════════════════╗
║  ✅  BALANCE UPDATED!  ✅                ║
╚═══════════════════════════════════════════╝

👤 User ID: {user_id}
💰 Balance Type: {balance_name}
💵 Amount: {amount} ({action_text})

📝 Reason: {reason}

💰 Previous Balance: {current_balance:.2f}
💰 New Balance: {new_balance:.2f}

✅ Balance updated successfully!
📬 Notification sent to user!

✨ Done! ✨
"""
    bot.send_message(message.chat.id, confirmation, parse_mode="Markdown")

# Notification delete password
DELETE_PASSWORD = "Mo321321"

def show_delete_notifications_menu(message, bot, load_notifications_func, save_notifications_func):
    """Show delete notifications menu"""
    menu_text = """
╔═══════════════════════════════════════════╗
║  🗑️  DELETE NOTIFICATIONS  🗑️          ║
╚═══════════════════════════════════════════╝

⚠️ Warning: This action cannot be undone!

🎯 Delete Options:
  📅 Delete by Date Range
  🗑️ Delete All Notifications

🔐 Password Required: Mo321321

✨ Select an option below ✨
"""
    
    # Create reply keyboard
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = telebot.types.KeyboardButton("📅 Delete by Date Range")
    btn2 = telebot.types.KeyboardButton("🗑️ Delete All Notifications")
    btn3 = telebot.types.KeyboardButton("🔙 Back to Admin Panel")
    markup.add(btn1, btn2)
    markup.add(btn3)
    
    bot.send_message(message.chat.id, menu_text, reply_markup=markup, parse_mode="Markdown")

def delete_by_date_range_prompt(message, bot, load_notifications_func, save_notifications_func):
    """Prompt for password and date range"""
    prompt_text = """
╔═══════════════════════════════════════════╗
║  📅  DELETE BY DATE RANGE  📅           ║
╚═══════════════════════════════════════════╝

🔐 Step 1: Enter Password
  Password: Mo321321

⚠️ This will delete notifications between dates

👇 Enter password to continue 👇
"""
    msg = bot.send_message(message.chat.id, prompt_text, parse_mode="Markdown")
    bot.register_next_step_handler(msg, lambda m: verify_password_for_date_range(m, bot, load_notifications_func, save_notifications_func))

def verify_password_for_date_range(message, bot, load_notifications_func, save_notifications_func):
    """Verify password for date range delete"""
    if message.text.strip() != DELETE_PASSWORD:
        error_text = """
╔═══════════════════════════════════════════╗
║  ❌  WRONG PASSWORD  ❌                  ║
╚═══════════════════════════════════════════╝

❌ Incorrect password!

🔐 Password: Mo321321

🔙 Go back and try again
"""
        bot.send_message(message.chat.id, error_text, parse_mode="Markdown")
        return
    
    # Password correct, ask for start date
    date_text = """
╔═══════════════════════════════════════════╗
║  📅  ENTER DATE RANGE  📅                ║
╚═══════════════════════════════════════════╝

✅ Password verified!

📅 Step 2: Enter Start Date
  Format: YYYY-MM-DD
  Example: 2025-11-20

👇 Enter start date (YYYY-MM-DD) 👇
"""
    msg = bot.send_message(message.chat.id, date_text, parse_mode="Markdown")
    bot.register_next_step_handler(msg, lambda m: get_start_date(m, bot, load_notifications_func, save_notifications_func))

def get_start_date(message, bot, load_notifications_func, save_notifications_func):
    """Get start date"""
    start_date_str = message.text.strip()
    
    try:
        # Validate date format
        datetime.strptime(start_date_str, "%Y-%m-%d")
        
        # Ask for end date
        date_text = f"""
╔═══════════════════════════════════════════╗
║  📅  ENTER END DATE  📅                  ║
╚═══════════════════════════════════════════╝

📅 Start Date: {start_date_str}

📅 Step 3: Enter End Date
  Format: YYYY-MM-DD
  Example: 2025-11-22

👇 Enter end date (YYYY-MM-DD) 👇
"""
        msg = bot.send_message(message.chat.id, date_text, parse_mode="Markdown")
        bot.register_next_step_handler(msg, lambda m: get_end_date(m, bot, start_date_str, load_notifications_func, save_notifications_func))
    except ValueError:
        error_text = """
╔═══════════════════════════════════════════╗
║  ❌  INVALID DATE FORMAT  ❌             ║
╚═══════════════════════════════════════════╝

❌ Invalid date format!

💡 Use format: YYYY-MM-DD
   Example: 2025-11-20

🔙 Try again
"""
        bot.send_message(message.chat.id, error_text, parse_mode="Markdown")

def get_end_date(message, bot, start_date_str, load_notifications_func, save_notifications_func):
    """Get end date and delete notifications"""
    end_date_str = message.text.strip()
    
    try:
        # Validate date format
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        
        if end_date < start_date:
            error_text = """
╔═══════════════════════════════════════════╗
║  ❌  INVALID DATE RANGE  ❌              ║
╚═══════════════════════════════════════════╝

❌ End date must be after start date!

🔙 Try again
"""
            bot.send_message(message.chat.id, error_text, parse_mode="Markdown")
            return
        
        # Load notifications
        notifications = load_notifications_func()
        
        # Filter notifications by date range
        deleted_count = 0
        remaining_notifications = []
        
        for notif in notifications:
            try:
                notif_date_str = notif.get('time', '').split(' ')[0]  # Get date part
                notif_date = datetime.strptime(notif_date_str, "%Y-%m-%d")
                
                if start_date <= notif_date <= end_date:
                    deleted_count += 1
                else:
                    remaining_notifications.append(notif)
            except:
                # If date parsing fails, keep the notification
                remaining_notifications.append(notif)
        
        # Save remaining notifications
        save_notifications_func(remaining_notifications)
        
        # Send confirmation
        confirmation = f"""
╔═══════════════════════════════════════════╗
║  ✅  NOTIFICATIONS DELETED!  ✅          ║
╚═══════════════════════════════════════════╝

📅 Date Range:
  From: {start_date_str}
  To: {end_date_str}

🗑️ Deleted: {deleted_count} notification(s)
📊 Remaining: {len(remaining_notifications)} notification(s)

✅ Deletion completed successfully!

✨ Done! ✨
"""
        bot.send_message(message.chat.id, confirmation, parse_mode="Markdown")
        
    except ValueError:
        error_text = """
╔═══════════════════════════════════════════╗
║  ❌  INVALID DATE FORMAT  ❌             ║
╚═══════════════════════════════════════════╝

❌ Invalid date format!

💡 Use format: YYYY-MM-DD
   Example: 2025-11-22

🔙 Try again
"""
        bot.send_message(message.chat.id, error_text, parse_mode="Markdown")

def delete_all_notifications_prompt(message, bot, load_notifications_func, save_notifications_func):
    """Prompt for password to delete all notifications"""
    prompt_text = """
╔═══════════════════════════════════════════╗
║  🗑️  DELETE ALL NOTIFICATIONS  🗑️       ║
╚═══════════════════════════════════════════╝

⚠️ WARNING: This will delete ALL notifications!
⚠️ This action CANNOT be undone!

🔐 Password Required: Mo321321

👇 Enter password to confirm deletion 👇
"""
    msg = bot.send_message(message.chat.id, prompt_text, parse_mode="Markdown")
    bot.register_next_step_handler(msg, lambda m: verify_password_delete_all(m, bot, load_notifications_func, save_notifications_func))

def verify_password_delete_all(message, bot, load_notifications_func, save_notifications_func):
    """Verify password and delete all notifications"""
    if message.text.strip() != DELETE_PASSWORD:
        error_text = """
╔═══════════════════════════════════════════╗
║  ❌  WRONG PASSWORD  ❌                  ║
╚═══════════════════════════════════════════╝

❌ Incorrect password!

🔐 Password: Mo321321

🔙 Go back and try again
"""
        bot.send_message(message.chat.id, error_text, parse_mode="Markdown")
        return
    
    # Password correct, delete all
    notifications = load_notifications_func()
    total_count = len(notifications)
    
    # Delete all notifications
    save_notifications_func([])
    
    # Send confirmation
    confirmation = f"""
╔═══════════════════════════════════════════╗
║  ✅  ALL NOTIFICATIONS DELETED!  ✅      ║
╚═══════════════════════════════════════════╝

🗑️ Deleted: {total_count} notification(s)

✅ All notifications have been deleted!

✨ Done! ✨
"""
    bot.send_message(message.chat.id, confirmation, parse_mode="Markdown")

