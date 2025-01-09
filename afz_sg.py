import telebot
import cv2
import os
import ctypes
import time
from PIL import ImageGrab
from win10toast import ToastNotifier
import win32gui
import win32process
import psutil
import threading
from plyer import notification
import win32file


SETTINGS_FILE = "settings.txt"

BOT_TOKEN = ""
AUTHORIZED_USERNAME = ""
CHAT_ID = ""

last_active_window = None
last_processes = set()
last_usb_devices = set()
last_bluetooth_devices = set()


def load_settings():
    global BOT_TOKEN, AUTHORIZED_USERNAME, CHAT_ID

    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            lines = file.readlines()
            for line in lines:
                key, value = line.strip().split("=", 1)
                if key == "BOT_TOKEN":
                    BOT_TOKEN = value
                elif key == "AUTHORIZED_USERNAME":
                    AUTHORIZED_USERNAME = value
                elif key == "CHAT_ID":
                    CHAT_ID = value
    else:
        print(f"⚠️ File {SETTINGS_FILE} not found. Please create it with required values.")

def save_chat_id(chat_id):
    global CHAT_ID
    CHAT_ID = chat_id
    settings = {
        "BOT_TOKEN": BOT_TOKEN,
        "AUTHORIZED_USERNAME": AUTHORIZED_USERNAME,
        "CHAT_ID": CHAT_ID
    }
    with open(SETTINGS_FILE, "w") as file:
        for key, value in settings.items():
            file.write(f"{key}={value}\n")           
    CHAT_ID = chat_id

load_settings()

if not BOT_TOKEN or not AUTHORIZED_USERNAME:
    raise ValueError("⚠️ BOT_TOKEN and AUTHORIZED_USERNAME must be set in settings.txt")

bot = telebot.TeleBot(BOT_TOKEN)

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=5
    )

def get_active_window():
    hwnd = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    process = psutil.Process(pid)
    window_title = win32gui.GetWindowText(hwnd)
    return f"🪟 Active window: {window_title} (Process: {process.name()})"

def get_battery_status():
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        charging = "🔌 Charging" if battery.power_plugged else "🔋 On Battery"
        return f"🔋 Battery Status: {percent}% ({charging})"
    else:
        return "⚠️ Battery information not available."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global CHAT_ID

    if message.from_user.username == AUTHORIZED_USERNAME:
        if not CHAT_ID:
            save_chat_id(message.chat.id)
        bot.reply_to(message, "👋 Hi friend! Here you can control your laptop. Try the buttons below!")
        show_main_menu(message.chat.id)
    else:
        bot.reply_to(message, "❌ Unauthorized access! You cannot use this bot.")

def show_main_menu(chat_id):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('/screenshot 📸', '/camera_photo 📷')
    markup.row('/lock_screen 🔒', '/unlock_screen 🔓')
    markup.row('/active_window 👓', '/send_notification 💬')
    markup.row('/shutdown 🔌', '/restart 🔄')
    markup.row('/battery_status 🔋', '/list_processes 📋')
    bot.send_message(chat_id, "🔽 Choose a button:", reply_markup=markup)

@bot.message_handler(commands=['screenshot'])
def take_screenshot(message):
    bot.reply_to(message, "⌛")
    bot.send_message(message.chat.id, "📸 Taking screenshot...")
    if message.from_user.username == AUTHORIZED_USERNAME:
        try:
            screenshot = ImageGrab.grab()
            screenshot.save('screenshot.png')
            with open('screenshot.png', 'rb') as img:
                bot.send_chat_action(message.chat.id, "upload_photo")
                bot.send_photo(message.chat.id, img)
            os.remove('screenshot.png')
            bot.reply_to(message, "✅ Screenshot taken successfully! 🖼️")
        except Exception as e:
            bot.reply_to(message, f'problem to take screenshot: {e}')
    else:
        bot.reply_to(message, "❌ Unauthorized access!")

@bot.message_handler(commands=['camera_photo'])
def take_camera_photo(message):
    bot.reply_to(message, "⏳")
    bot.send_message(message.chat.id, "📷 Taking camera photo...")
    if message.from_user.username == AUTHORIZED_USERNAME:
        try:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                cv2.imwrite('photo.png', frame)
                with open('photo.png', 'rb') as img:
                    bot.send_photo(message.chat.id, img)
                os.remove('photo.png')
                bot.reply_to(message, "📸 Camera photo captured successfully!")
            else:
                bot.reply_to(message, "⚠️ Failed to capture photo. Try again.")
            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            bot.reply_to(message, f'problem to take camera photo: {e}')
    else:
        bot.reply_to(message, "❌ Unauthorized access!")

@bot.message_handler(commands=['lock_screen'])
def lock_screen(message):
    if message.from_user.username == AUTHORIZED_USERNAME:
        try:
            ctypes.windll.user32.LockWorkStation()
            bot.reply_to(message, "🔒 Laptop locked.")
        except Exception as e:
            bot.reply_to(message, f'problem to lock screen: {e}')
    else:
        bot.reply_to(message, "❌ Unauthorized access!")

@bot.message_handler(commands=['unlock_screen'])
def unlock_screen(message):
    if message.from_user.username == AUTHORIZED_USERNAME:
        bot.reply_to(message, "🔓 Unlocking requires manual password input.")
    else:
        bot.reply_to(message, "❌ Unauthorized access!")

@bot.message_handler(commands=['active_window'])
def report_active_window(message):
    if message.from_user.username == AUTHORIZED_USERNAME:
        try:
            active_window = get_active_window()
            bot.reply_to(message, active_window)
        except Exception as e:
            bot.reply_to(message, f'problem to get active window: {e}')
    else:
        bot.reply_to(message, "❌ Unauthorized access!")

@bot.message_handler(commands=['send_notification'])
def send_windows_notification(message):
    if message.from_user.username == AUTHORIZED_USERNAME:
        # bot.reply_to(message, "💬 Send me the text for the notification.")
        # bot.register_next_step_handler(message, get_notification_text)
        bot.reply_to(message, "soon....")
    else:
        bot.reply_to(message, "❌ Unauthorized access!")

# def get_notification_text(message):
#     if message.from_user.username == AUTHORIZED_USERNAME:
#         # send_notification("🔔", message.text)
#         # bot.reply_to(message, "✅ Notification sent! 🎉")
#         bot.reply_to(message, "soon....")
#     else:
#         bot.reply_to(message, "❌ Unauthorized access!")

@bot.message_handler(commands=['shutdown'])
def shutdown_system(message):
    if message.from_user.username == AUTHORIZED_USERNAME:
        try:
            bot.reply_to(message, "⚡ Shutting down the system! 🖥️")
            os.system("shutdown /s /t 1")
        except Exception as e:
            bot.reply_to(message, f'problem to shutdown the system: {e}')
    else:
        bot.reply_to(message, "❌ Unauthorized access!")

@bot.message_handler(commands=['restart'])
def restart_system(message):
    if message.from_user.username == AUTHORIZED_USERNAME:
        try:
            bot.reply_to(message, "🔄 Restarting the system! 💻")
            os.system("shutdown /r /t 1")
        except Exception as e:
            bot.reply_to(message, f'problem to restart the system: {e}')
    else:
        bot.reply_to(message, "❌ Unauthorized access!")

@bot.message_handler(commands=['battery_status'])
def battery_status(message):
    if message.from_user.username == AUTHORIZED_USERNAME:
        try:
            status = get_battery_status()
            bot.reply_to(message, status)
        except Exception as e:
            bot.reply_to(message, f'problem to get battery status: {e}')
    else:
        bot.reply_to(message, "❌ Unauthorized access!")

@bot.message_handler(commands=['list_processes'])
def list_processes(message):
    if message.from_user.username == AUTHORIZED_USERNAME:
        processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                processes.append(f"{proc.info['name']} (PID: {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if processes:
            processes_list = "\n".join(processes[:50])
            bot.reply_to(message, f"🔍 لیست برنامه‌های فعال:\n\n{processes_list}")
        else:
            bot.reply_to(message, "⚠️ برنامه‌ای در حال اجرا پیدا نشد.")
    else:
        bot.reply_to(message, "❌ Unauthorized access!")
            
def get_active_window():
    try:
        hwnd = win32gui.GetForegroundWindow()
        window_title = win32gui.GetWindowText(hwnd)
        return window_title
    except Exception as e:
        return f'cannot get active window: {e}'

def get_usb_devices():
    try:
        drives = win32file.GetLogicalDrives()
        usb_drives = []
        for drive_letter in range(26):
            if drives & (1 << drive_letter):
                drive = chr(65 + drive_letter) + ":\\"
                drive_type = win32file.GetDriveType(drive)
                if drive_type == win32file.DRIVE_REMOVABLE:
                    usb_drives.append(drive)
        return set(usb_drives)
    except Exception as e:
        return f'cannot get usb drives: {e}'


def monitor_system():
    global last_active_window, last_processes, last_usb_devices, last_bluetooth_devices

    while True:
        if CHAT_ID:
            # Check active window
            active_window = get_active_window()
            if active_window != last_active_window:
                last_active_window = active_window
                bot.send_message(CHAT_ID, f"🪟 Active Window Changed: {active_window}")

            # Check running processes
            # current_processes = set(proc.info['name'] for proc in psutil.process_iter(['name']))
            # new_processes = current_processes - last_processes
            # if new_processes:
            #     for process in new_processes:
            #         bot.send_message(CHAT_ID, f"🔄 New Process Started: {process}")
            # last_processes = current_processes

            # Check USB devices
            current_usb_devices = get_usb_devices()
            added_usb = current_usb_devices - last_usb_devices
            removed_usb = last_usb_devices - current_usb_devices
            if added_usb:
                for device in added_usb:
                    bot.send_message(CHAT_ID, f"🔌 USB Connected: {device}")
            if removed_usb:
                for device in removed_usb:
                    bot.send_message(CHAT_ID, f"⚠️ USB Disconnected: {device}")
            last_usb_devices = current_usb_devices

            time.sleep(1)
        else:
            print("⚠️ Chat ID not set. Please start the bot with /start command.")
            time.sleep(2)

# Start monitoring in a separate thread
monitor_thread = threading.Thread(target=monitor_system, daemon=True)
monitor_thread.start()

print("🤖 Bot is running and ready! 🚀")
bot.polling(timeout=60, long_polling_timeout=60)