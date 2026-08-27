# link_shortener_bot.py - Advanced Link Bypass Bot with Hex OSINT UI

import logging
import asyncio
import aiohttp
import json
import os
import sys
import subprocess
import random
import string
import re
from datetime import datetime, timedelta
from io import BytesIO

# ---- SUPPRESS TELEHTHON INFO LOGS ----
logging.getLogger('telethon').setLevel(logging.WARNING)
logging.getLogger('telethon.network').setLevel(logging.WARNING)
logging.getLogger('telethon.client').setLevel(logging.WARNING)

try:
    from telethon import TelegramClient, events, functions
    from telethon.tl.types import (
        KeyboardButton, KeyboardButtonRow, ReplyKeyboardMarkup,
        KeyboardButtonStyle, KeyboardButtonCallback, ReplyInlineMarkup,
        KeyboardButtonUrl, InputFile
    )
    from telethon.tl.functions.channels import GetParticipantRequest
    from telethon.errors import UserNotParticipantError, ChannelPrivateError
    HAS_BUTTON_STYLE = True
except ImportError:
    print("Installing Telethon...")
    subprocess.run([sys.executable, "-m", "pip", "install", "git+https://github.com/LonamiWebs/Telethon.git"])
    from telethon import TelegramClient, events, functions
    from telethon.tl.types import (
        KeyboardButton, KeyboardButtonRow, ReplyKeyboardMarkup,
        KeyboardButtonStyle, KeyboardButtonCallback, ReplyInlineMarkup,
        KeyboardButtonUrl, InputFile
    )
    from telethon.tl.functions.channels import GetParticipantRequest
    from telethon.errors import UserNotParticipantError, ChannelPrivateError
    HAS_BUTTON_STYLE = True

# ---- CONFIGURATION ----
API_ID = int(os.environ.get('API_ID', '37996037'))
API_HASH = os.environ.get('API_HASH', '47ee9fa07b5eeb865edb3d79ada726a5')
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8687617595:AAFF6FP5XWr92RFhM0wco6UHutB7UGUpFFA')
ADMIN_ID = int(os.environ.get('ADMIN_ID', '7898928200'))

CHANNEL_1_ID = int(os.environ.get('CHANNEL_1_ID', '-1003240507339'))
CHANNEL_2_ID = int(os.environ.get('CHANNEL_2_ID', '-1003806004135'))

LINK_1 = os.environ.get('LINK_1', 'https://t.me/+dP7xLb3AoE1jNmRl')
LINK_2 = os.environ.get('LINK_2', 'https://t.me/+9vuPcr9LJ8piODdl')

FOOTER = "\n\n⚡ ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr ⭐"
SEP = "━━━━━━━━━━━━━━━━━━━"

# ---- EMOJI IDs ----
PE = lambda eid, fallback: f'<tg-emoji emoji-id="{eid}">{fallback}</tg-emoji>'

# Link Shortener Emojis (Your IDs)
E_LINK_ORIGINAL = PE("6122648774356504384", "🔗")
E_LINK_BYPASS = PE("5456140674028019486", "⚡")
E_LINK_TIME = PE("5776213190387961618", "⏱️")
E_LINK_ID = PE("5877465816030515018", "🔗")

# System Emojis (Same as Hex OSINT)
E_DIAMOND = PE("6314557546753440004", "💎")
E_LION = PE("5802980697886954454", "🦁")
E_HAPPY = PE("6154369208076470797", "🥹")
E_WALLET = PE("5256186332669035163", "👛")
E_CROWN = PE("6267128480601741166", "👑")
E_CAMERA = PE("6008258140108231117", "📸")
E_ARROW = PE("5875450995332353523", "➡️")
E_DIAMOND2 = PE("4961143940817355662", "💠")
E_STAR = PE("5289898724976240966", "⭐")
E_BOLT = PE("5377834924776627189", "⚡")
E_POWERED = PE("6176952682989754426", "⚡")
E_SEARCH = PE("5231012545799666522", "🔍")
E_CHECK = PE("6267008582294705964", "✅")
E_CROSS = PE("6267000941547885720", "❌")
E_WARN = PE("6267039884016358504", "⚠️")
E_LOCK = PE("5316522278056399236", "🔒")
E_USERS = PE("5244933196230972438", "👥")
E_CREDIT = PE("6267068789146260253", "💰")
E_CLOCK = PE("5382194935057372936", "⏱️")
E_GIFT = PE("5203996991054432397", "🎁")
E_TICKET = PE("5285515895534278367", "🎫")
E_TOOLS = PE("5462921117423384478", "🛠️")
E_HOME = PE("5280955052582785391", "🏠")
E_SPARKLE = PE("5467683093693354332", "✨")
E_ROCKET = PE("5195033767969839232", "🚀")
E_STAR2 = PE("6266969287638913443", "🌟")
E_LINK = PE("5271604874419647061", "🔗")
E_GEAR = PE("5462921117423384478", "⚙️")
E_WELCOME = PE("6266969287638913443", "✨")

E_LINE = PE("6329854094252970694", "➿")
E_VERTICAL_LINE = PE("5319053559981959471", "🪭")
E_STORE_START = PE("5438401999534039253", "💎")
E_STORE_END = PE("6010095381088571985", "🛍")
E_GREET_START = PE("5773659712071409251", "🥹")
E_GREET_END = PE("6336972134962697188", "👑")
E_DASHBOARD = PE("6010080507616826629", "📊")
E_BALANCE_ICON = PE("6147767796097884213", "💰")
E_ROLE_ICON = PE("6147528944376618702", "👑")
E_CHATID_ICON = PE("6010280773351904888", "✉️")
E_BOLT_WELCOME = PE("6176952682989754426", "⚡")

# ---- ICON IDs ----
ICON_BYPASS = 5456140674028019486
ICON_ORIGINAL = 6122648774356504384
ICON_TIME = 5776213190387961618
ICON_LINK = 5877465816030515018
ICON_INVITE = 6048721430730773527
ICON_UPGRADE = 5251422397893989847
ICON_ADMIN = 5406711411541823609
ICON_JOIN1 = 5802980697886954454
ICON_JOIN2 = 6154369208076470797
ICON_VERIFY = 5289898724976240966
ICON_NEXT = 5260450573768990626

# ---- LOGGING ----
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ---- INIT BOT ----
client = TelegramClient('link_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# ---- CONSTANTS ----
BYPASS_API = "https://link-shorter-hex-production.up.railway.app/bypass?link="
AUTO_DELETE_TIME = 60
DAILY_FREE_CREDITS = 10
INVITE_CREDITS = 3

USERS_FILE = os.path.join(os.getcwd(), "users.json")
REDEEM_FILE = os.path.join(os.getcwd(), "redeem_codes.json")
SETTINGS_FILE = os.path.join(os.getcwd(), "settings.json")

ADMIN_STATE = {}
processed_messages = set()
processing_lock = asyncio.Lock()

# ---- 💾 DATA FUNCTIONS ----

def load_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_json(filename, data):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except:
        pass

def get_user(user_id):
    users = load_json(USERS_FILE)
    uid = str(user_id)
    today = datetime.now().strftime("%Y-%m-%d")
    if uid not in users:
        users[uid] = {
            "credits": DAILY_FREE_CREDITS,
            "total_queries": 0,
            "daily_queries": 0,
            "last_reset": today,
            "invite_code": f"HEX-{''.join(random.choices(string.ascii_uppercase+string.digits, k=8))}",
            "invites": 0,
            "verified": False,
            "premium": False,
            "started": False
        }
        save_json(USERS_FILE, users)
    elif users[uid].get("last_reset") != today:
        users[uid]["credits"] = DAILY_FREE_CREDITS
        users[uid]["daily_queries"] = 0
        users[uid]["last_reset"] = today
        save_json(USERS_FILE, users)
    return users[uid]

def save_user(uid, data):
    users = load_json(USERS_FILE)
    users[str(uid)] = data
    save_json(USERS_FILE, users)

def add_credits(uid, amount):
    users = load_json(USERS_FILE)
    uid = str(uid)
    if uid in users:
        users[uid]["credits"] = users[uid].get("credits", 0) + amount
        save_json(USERS_FILE, users)
        return users[uid]["credits"]
    return 0

def use_credit(uid):
    users = load_json(USERS_FILE)
    uid = str(uid)
    if uid in users and users[uid].get("credits", 0) > 0:
        users[uid]["credits"] -= 1
        users[uid]["total_queries"] = users[uid].get("total_queries", 0) + 1
        users[uid]["daily_queries"] = users[uid].get("daily_queries", 0) + 1
        save_json(USERS_FILE, users)
        return True
    return False

def process_invite(inviter_id, new_id):
    users = load_json(USERS_FILE)
    inviter = str(inviter_id)
    new = str(new_id)
    if inviter in users:
        users[inviter]["credits"] = users[inviter].get("credits", 0) + INVITE_CREDITS
        users[inviter]["invites"] = users[inviter].get("invites", 0) + 1
    if new in users:
        users[new]["credits"] = users[new].get("credits", 0) + INVITE_CREDITS
        users[new]["invited_by"] = inviter
    save_json(USERS_FILE, users)
    return INVITE_CREDITS

def generate_redeem_code(credits):
    code = f"HEX-{''.join(random.choices(string.ascii_uppercase+string.digits, k=10))}"
    codes = load_json(REDEEM_FILE)
    codes[code] = {"credits": credits, "used": False, "created": datetime.now().isoformat()}
    save_json(REDEEM_FILE, codes)
    return code

def redeem_code(uid, code):
    codes = load_json(REDEEM_FILE)
    code = code.upper().strip()
    if code not in codes:
        return False, f"{E_CROSS} ɪɴᴠᴀʟɪᴅ ᴄᴏᴅᴇ"
    if codes[code].get("used"):
        return False, f"{E_CROSS} ᴀʟʀᴇᴀᴅʏ ᴜꜱᴇᴅ"
    cr = codes[code]["credits"]
    codes[code]["used"] = True
    codes[code]["used_by"] = str(uid)
    save_json(REDEEM_FILE, codes)
    bal = add_credits(uid, cr)
    return True, f"{E_CHECK} +{cr} ᴄʀᴇᴅɪᴛꜱ ᴀᴅᴅᴇᴅ!\n{E_CREDIT} ʙᴀʟᴀɴᴄᴇ: {bal}"

def get_settings():
    try:
        return load_json(SETTINGS_FILE)
    except:
        d = {
            "bypass_maintenance": False,
            "maintenance_mode": False,
            "page": 1
        }
        save_json(SETTINGS_FILE, d)
        return d

def save_settings(data):
    save_json(SETTINGS_FILE, data)

# ---- 🔍 VERIFY ----

async def check_channel_member(channel_id, user_id):
    try:
        result = await client(GetParticipantRequest(
            channel=channel_id,
            participant=user_id
        ))
        return True
    except UserNotParticipantError:
        return False
    except:
        return False

async def check_channels(uid):
    try:
        in_channel1 = await check_channel_member(CHANNEL_1_ID, uid)
        in_channel2 = await check_channel_member(CHANNEL_2_ID, uid)
        return in_channel1 and in_channel2
    except:
        return False

async def check_individual_channels(uid):
    try:
        in_channel1 = await check_channel_member(CHANNEL_1_ID, uid)
        in_channel2 = await check_channel_member(CHANNEL_2_ID, uid)
        return in_channel1, in_channel2
    except:
        return False, False

# ---- 🛠️ UTILS ----

async def schedule_delete(msg, delay=AUTO_DELETE_TIME):
    await asyncio.sleep(delay)
    try:
        await msg.delete()
    except:
        pass

async def send_html(chat_id, text, reply_markup=None):
    return await client.send_message(
        chat_id,
        text,
        buttons=reply_markup,
        parse_mode='html'
    )

async def edit_html(msg, text, reply_markup=None):
    return await client.edit_message(
        msg,
        text,
        buttons=reply_markup,
        parse_mode='html'
    )

# ---- 🎨 BUTTON HELPERS ----

def create_primary_button(text, emoji_id):
    style = KeyboardButtonStyle(bg_primary=True, icon=emoji_id)
    return KeyboardButton(text=text, style=style)

def create_success_button(text, emoji_id):
    style = KeyboardButtonStyle(bg_success=True, icon=emoji_id)
    return KeyboardButton(text=text, style=style)

def create_danger_button(text, emoji_id):
    style = KeyboardButtonStyle(bg_danger=True, icon=emoji_id)
    return KeyboardButton(text=text, style=style)

# ---- 🆕 MAIN MENU ----

def create_main_menu(is_admin=False, settings=None):
    if settings is None:
        settings = get_settings()
    page = settings.get("page", 1)
    rows = []
    
    if page == 1:
        # Row 1: Link Bypass (primary)
        row1 = [
            create_primary_button("Lɪɴᴋ Bʏᴘᴀss", ICON_BYPASS)
        ]
        rows.append(KeyboardButtonRow(buttons=row1))
        
        # Row 2: Upgrade To Premium (green) and Invite & Earn (green)
        row2 = [
            create_success_button("Uᴘɢʀᴀᴅᴇ Tᴏ Pʀᴇᴍɪᴜᴍ", ICON_UPGRADE),
            create_success_button("Iɴᴠɪᴛᴇ & Eᴀʀɴ", ICON_INVITE)
        ]
        rows.append(KeyboardButtonRow(buttons=row2))
        
        # Row 3: Next Page (red) and Admin Panel (red if admin)
        row3 = []
        row3.append(create_danger_button("Nᴇxᴛ Pᴀɢᴇ", ICON_NEXT))
        if is_admin:
            row3.append(create_danger_button("Aᴅᴍɪɴ Pᴀɴᴇʟ", ICON_ADMIN))
        rows.append(KeyboardButtonRow(buttons=row3))
    
    else:  # page 2
        rows.append(KeyboardButtonRow(buttons=[
            create_danger_button("◀ Pʀᴇᴠɪᴏᴜs Pᴀɢᴇ", ICON_NEXT)
        ]))
        # Row 2: Stats
        rows.append(KeyboardButtonRow(buttons=[
            create_primary_button("📊 Sᴛᴀᴛs", ICON_TIME)
        ]))
    
    return ReplyKeyboardMarkup(rows=rows, resize=True)

# ---- 🆕 WELCOME PANEL ----

def build_welcome_panel(uid, first_name, credits, premium=False):
    line10 = E_LINE * 10
    role = "PREMIUM" if premium else "USER"
    return f"""<blockquote>{line10}      
{E_STORE_START} 𝚮 𝚬 𝚾   𝚯 S ༏ 𝚴 𝚻 {E_STORE_END}
{line10}
{E_GREET_START} Hᴇʏ {first_name} {E_GREET_END}

{E_DASHBOARD} ʏᴏᴜʀ ᴅᴀꜱʜʙᴏᴀʀᴅ !!
{line10}
{E_VERTICAL_LINE} {E_BALANCE_ICON} ʏᴏᴜʀ ʙᴀʟᴀɴᴄᴇ » {credits} ᴄʀᴇᴅɪᴛꜱ

{E_VERTICAL_LINE} {E_ROLE_ICON} ʀᴏʟᴇ » {role}

{E_VERTICAL_LINE} {E_CHATID_ICON} ʏᴏᴜʀ ɪᴅ » {uid}

{E_VERTICAL_LINE} {E_LINK_ORIGINAL} Lɪɴᴋ Bʏᴘᴀssꜱᴇʀ

{line10}
{E_ARROW} Sᴇɴᴅ ᴀɴʏ ʟɪɴᴋ ᴛᴏ ʙʏᴘᴀss

{E_DIAMOND2} ꜱᴇʟᴇᴄᴛ ᴀ ꜱᴇʀᴠɪᴄᴇ ʙᴇʟᴏᴡ
{line10}
{E_BOLT_WELCOME} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}
{line10}</blockquote>"""

# ---- 🚀 BYPASS FUNCTION ----

async def bypass_link(session, link):
    try:
        url = f"{BYPASS_API}{link}"
        async with session.get(url, timeout=30) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("success"):
                    return {
                        "original": data.get("original", link),
                        "bypassed": data.get("bypassed", link),
                        "time": data.get("time", "0"),
                        "success": True
                    }
                else:
                    return {
                        "error": data.get("error", "Unknown error"),
                        "success": False
                    }
            else:
                return {
                    "error": f"API returned {response.status}",
                    "success": False
                }
    except Exception as e:
        logger.error(f"Bypass error: {e}")
        return {
            "error": str(e),
            "success": False
        }

# ---- 📋 VERIFICATION PAGE ----

async def show_verification_page(event):
    try:
        txt = (
            f"<blockquote>{E_DIAMOND} {BOT_NAME} {E_DIAMOND}\n\n"
            f"@{BOT_USERNAME}\n\n"
            f"{E_LOCK} <b>VERIFICATION REQUIRED</b>\n\n"
            f"JOIN BOTH CHANNELS TO UNLOCK\n\n"
            f"{E_GIFT} +{DAILY_FREE_CREDITS} DAILY {E_STAR}\n\n"
            f"{E_USERS} +{INVITE_CREDITS} PER INVITE\n\n"
            f"{E_CLOCK} {AUTO_DELETE_TIME}s AUTO DELETE\n\n"
            f"{E_CROWN} <b>OWNER: @HeX_CiPhEr</b></blockquote>"
        )
        style1 = KeyboardButtonStyle(bg_primary=True, icon=ICON_JOIN1)
        button1 = KeyboardButtonUrl(text="JOIN CHANNEL 1", url=LINK_1, style=style1)
        style2 = KeyboardButtonStyle(bg_success=True, icon=ICON_JOIN2)
        button2 = KeyboardButtonUrl(text="JOIN CHANNEL 2", url=LINK_2, style=style2)
        style3 = KeyboardButtonStyle(bg_danger=True, icon=ICON_VERIFY)
        button3 = KeyboardButtonCallback(text="VERIFY", data=b"verify", style=style3)
        markup = ReplyInlineMarkup(rows=[
            KeyboardButtonRow(buttons=[button1]),
            KeyboardButtonRow(buttons=[button2]),
            KeyboardButtonRow(buttons=[button3])
        ])
        await send_html(event.chat_id, txt, reply_markup=markup)
    except Exception as e:
        logger.error(f"Verification page error: {e}")

# ---- 🚀 HANDLERS ----

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    async with processing_lock:
        try:
            uid = event.sender_id
            user = get_user(uid)
            user["started"] = True
            save_user(uid, user)
            
            args = event.message.message.split()
            if len(args) > 1 and args[1].startswith("HEX-"):
                users = load_json(USERS_FILE)
                for inviter, data in users.items():
                    if data.get("invite_code") == args[1] and inviter != str(uid):
                        cr = process_invite(inviter, uid)
                        try:
                            await send_html(int(inviter), f"<blockquote>{E_GIFT} +{cr} CREDITS! NEW USER JOINED!\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>")
                        except:
                            pass
                        break
            
            await send_welcome(event)
        except Exception as e:
            logger.error(f"Start: {e}")
            await main_menu(event)

@client.on(events.CallbackQuery(data=b"verify"))
async def verify_cb(event):
    try:
        uid = event.sender_id
        in_channel1, in_channel2 = await check_individual_channels(uid)
        if in_channel1 and in_channel2:
            user = get_user(uid)
            user["verified"] = True
            save_user(uid, user)
            await event.answer("✅ Verified!", alert=True)
            try:
                await event.delete()
            except:
                pass
            try:
                await event.message.delete()
            except:
                pass
            await send_welcome(event)
        elif not in_channel1 and not in_channel2:
            await event.answer("❌ Join both channels first!", alert=True)
        elif not in_channel1:
            await event.answer("❌ Join Channel 1 first!", alert=True)
        elif not in_channel2:
            await event.answer("❌ Join Channel 2 first!", alert=True)
    except Exception as e:
        logger.error(f"Verify callback error: {e}")
        await event.answer("❌ Error, try again", alert=True)

@client.on(events.CallbackQuery)
async def admin_callback_handler(event):
    if event.data and event.data.startswith(b"ad_"):
        await admin_callback(event)

async def send_welcome(event):
    try:
        uid = event.sender_id
        user = get_user(uid)
        credits = user.get('credits', 0)
        premium = user.get('premium', False)
        first_name = event.sender.first_name or "User"
        caption = build_welcome_panel(uid, first_name, credits, premium)
        is_admin = event.sender_id == ADMIN_ID
        if event.is_group:
            msg = await send_html(event.chat_id, caption)
        else:
            markup = create_main_menu(is_admin, get_settings())
            msg = await send_html(event.chat_id, caption, reply_markup=markup)
    except Exception as e:
        logger.error(f"Send welcome error: {e}")
        await main_menu(event)

async def main_menu(event):
    is_admin = event.sender_id == ADMIN_ID
    user = get_user(event.sender_id)
    s = get_settings()
    if not await check_channels(event.sender_id):
        user["verified"] = False
        save_user(event.sender_id, user)
        await show_verification_page(event)
        return
    credits = user.get("credits", 0)
    premium = user.get('premium', False)
    first_name = event.sender.first_name or "User"
    welcome_text = build_welcome_panel(event.sender_id, first_name, credits, premium)
    if event.is_group:
        msg = await send_html(event.chat_id, welcome_text)
    else:
        markup = create_main_menu(is_admin, s)
        msg = await send_html(event.chat_id, welcome_text, reply_markup=markup)

# ---- 🆕 HELPERS ----

async def process_feature(event, mode):
    uid = event.sender_id
    user = get_user(uid)
    if not user.get("verified"):
        if await check_channels(uid):
            user["verified"] = True
            save_user(uid, user)
        else:
            await show_verification_page(event)
            return
    
    if mode == "INVITE":
        user = get_user(uid)
        bot_username = BOT_USERNAME
        link = f"https://t.me/{bot_username}?start={user['invite_code']}"
        invite_msg = (
            f"<blockquote>{E_STAR} Invite & Earn {E_STAR}\n\n"
            f"{E_USERS} +{INVITE_CREDITS} Credits per invite\n\n"
            f"{E_LINK} {link}\n\n"
            f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
        )
        m = await send_html(event.chat_id, invite_msg)
        asyncio.create_task(schedule_delete(m, 120))
        return
    elif mode == "UPGRADE":
        m = await send_html(event.chat_id, 
            f"<blockquote>{E_UPGRADE} Uᴘɢʀᴀᴅᴇ Tᴏ Pʀᴇᴍɪᴜᴍ\n\n"
            f"Contact @HeX_CiPhEr to upgrade your account!\n\n"
            f"🌟 Premium Benefits:\n\n"
            f"• Unlimited Credits\n\n"
            f"• All Services Access\n\n"
            f"• Priority Support\n\n"
            f"• Exclusive Features\n\n"
            f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
        )
        asyncio.create_task(schedule_delete(m, 60))
        return

# ---- 📊 ADMIN PANEL ----

async def admin_panel(event):
    if event.sender_id != ADMIN_ID:
        return
    s = get_settings()
    buttons = [
        [KeyboardButtonCallback(text="🎫 Gen Code", data=b"ad_gen"), KeyboardButtonCallback(text="📋 Codes", data=b"ad_codes")],
        [KeyboardButtonCallback(text="🎁 Add Credits", data=b"ad_credit"), KeyboardButtonCallback(text="📢 Broadcast", data=b"ad_bcast")],
        [KeyboardButtonCallback(text=f"{'🔴' if s.get('maintenance_mode') else '🟢'} Global", data=b"ad_maint")],
        [KeyboardButtonCallback(text="📊 Stats", data=b"ad_stats")],
        [KeyboardButtonCallback(text="❌ Close", data=b"ad_close")]
    ]
    rows = []
    for row in buttons:
        if row:
            rows.append(KeyboardButtonRow(buttons=row))
    markup = ReplyInlineMarkup(rows=rows)
    txt = f"<blockquote>👑 ADMIN PANEL\n\n👥 USERS: {len(load_json(USERS_FILE))} | 🎫 CODES: {len(load_json(REDEEM_FILE))}\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
    if hasattr(event, 'data'):
        await event.edit(txt, buttons=markup)
    else:
        await send_html(event.chat_id, txt, reply_markup=markup)

async def admin_callback(event):
    if event.sender_id != ADMIN_ID:
        await event.answer("❌", alert=True)
        return
    d = event.data.decode()
    s = get_settings()
    if d == "ad_close":
        await event.delete()
    elif d == "ad_codes":
        codes = load_json(REDEEM_FILE)
        txt = f"<blockquote>🎫 CODES: {len(codes)}\n\n"
        for c, v in list(codes.items())[-15:]:
            txt += f"{'✅' if not v.get('used') else '❌'} {c} | {v.get('credits')}cr\n\n"
        txt += f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
        await event.edit(txt, buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="🔙 Back", data=b"ad_back")])]))
    elif d == "ad_gen":
        ADMIN_STATE[event.sender_id] = "gen"
        await event.edit(f"<blockquote>🎫 ENTER CREDITS:\n\n100\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>", buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="🔙 Back", data=b"ad_back")])]))
    elif d == "ad_credit":
        ADMIN_STATE[event.sender_id] = "credit"
        await event.edit(f"<blockquote>🎁 ENTER ID AMOUNT:\n\n123456789 50\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>", buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="🔙 Back", data=b"ad_back")])]))
    elif d == "ad_bcast":
        ADMIN_STATE[event.sender_id] = "bcast"
        await event.edit(f"<blockquote>📢 ENTER MESSAGE:\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>", buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="🔙 Back", data=b"ad_back")])]))
    elif d == "ad_maint":
        s["maintenance_mode"] = not s.get("maintenance_mode", False)
        save_settings(s)
        await event.answer(f"Global: {'ON' if s['maintenance_mode'] else 'OFF'}", alert=True)
        await admin_panel(event)
    elif d == "ad_stats":
        users = load_json(USERS_FILE)
        total_users = len(users)
        total_queries = sum(u.get('total_queries', 0) for u in users.values())
        total_invites = sum(u.get('invites', 0) for u in users.values())
        premium_users = sum(1 for u in users.values() if u.get('premium', False))
        txt = f"""<blockquote>📊 Sᴛᴀᴛɪsᴛɪᴄs

👥 Total Users: {total_users}
📊 Total Queries: {total_queries}
🎫 Total Invites: {total_invites}
👑 Premium Users: {premium_users}
💰 Total Credits: {sum(u.get('credits', 0) for u in users.values())}

{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"""
        await event.edit(txt, buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="🔙 Back", data=b"ad_back")])]))
    elif d == "ad_back":
        await admin_panel(event)
    await event.answer()

# ---- 🚀 MAIN MESSAGE HANDLER ----

@client.on(events.NewMessage)
async def msg_handler(event):
    async with processing_lock:
        try:
            uid = event.sender_id
            txt = event.message.message.strip()
            if not txt:
                return
            
            if txt.startswith('/start'):
                return
            
            # Slash commands
            if txt.startswith('/'):
                raw_cmd = txt.split()[0]
                if '@' in raw_cmd:
                    raw_cmd = raw_cmd.split('@')[0]
                raw_cmd = raw_cmd.lower()
                
                if raw_cmd in ('/help', '/commands'):
                    await show_commands(event)
                    return
                
                if raw_cmd == '/bypass':
                    parts = txt.split(maxsplit=1)
                    arg = parts[1] if len(parts) > 1 else None
                    if arg is None:
                        m = await send_html(event.chat_id, f"<blockquote>{E_WARN} Please provide a link.\nExample: <code>/bypass https://earnlinks.in/WoivZ</code></blockquote>")
                        asyncio.create_task(schedule_delete(m))
                        return
                    user = get_user(uid)
                    if not user.get("verified"):
                        if await check_channels(uid):
                            user["verified"] = True
                            save_user(uid, user)
                        else:
                            await show_verification_page(event)
                            return
                    if user.get("credits", 0) <= 0:
                        m = await send_html(event.chat_id, f"<blockquote>{E_CROSS} No credits! +10 daily | +3 invite</blockquote>")
                        asyncio.create_task(schedule_delete(m))
                        return
                    use_credit(uid)
                    async with aiohttp.ClientSession() as session:
                        result = await bypass_link(session, arg)
                    result_text = format_result(result, arg)
                    sent = await send_html(event.chat_id, result_text)
                    asyncio.create_task(schedule_delete(sent))
                    return
                
                if raw_cmd == '/invite':
                    await process_feature(event, "INVITE")
                    return
                if raw_cmd == '/upgrade':
                    await process_feature(event, "UPGRADE")
                    return
                if raw_cmd == '/stats':
                    await show_stats(event)
                    return
                
                m = await send_html(event.chat_id, f"<blockquote>{E_CROSS} Unknown command. Type /Help for help.</blockquote>")
                asyncio.create_task(schedule_delete(m))
                return
            
            # Duplicate prevention
            msg_id = event.message.id
            if msg_id in processed_messages:
                return
            processed_messages.add(msg_id)
            if len(processed_messages) > 500:
                processed_messages.clear()
            
            # In groups, only slash commands are accepted
            if event.is_group:
                return
            
            # Auto-delete user messages in private
            asyncio.create_task(schedule_delete(event.message, AUTO_DELETE_TIME))
            
            s = get_settings()
            if s.get("maintenance_mode", False) and uid != ADMIN_ID:
                m = await send_html(event.chat_id, f"<blockquote>{E_TOOLS} Under maintenance\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>")
                asyncio.create_task(schedule_delete(m))
                return
            
            # Button labels
            label_map = {
                "Lɪɴᴋ Bʏᴘᴀss": ("BYPASS", None),
                "Uᴘɢʀᴀᴅᴇ Tᴏ Pʀᴇᴍɪᴜᴍ": ("UPGRADE", None),
                "Iɴᴠɪᴛᴇ & Eᴀʀɴ": ("INVITE", None),
                "📊 Sᴛᴀᴛs": ("STATS", None)
            }
            
            if txt in label_map:
                mode, _ = label_map[txt]
                if mode == "BYPASS":
                    user = get_user(uid)
                    if not user.get("verified"):
                        if await check_channels(uid):
                            user["verified"] = True
                            save_user(uid, user)
                        else:
                            await show_verification_page(event)
                            return
                    credits = user.get("credits", 0)
                    m = await send_html(event.chat_id, f"""<blockquote>{E_LINK_ORIGINAL} Lɪɴᴋ Bʏᴘᴀss

Sᴇɴᴅ ᴀɴʏ ʟɪɴᴋ ᴛᴏ ʙʏᴘᴀss

{E_WALLET} Yᴏᴜʀ Cʀᴇᴅɪᴛs: {credits}

Sᴇᴀʀᴄʜ Cᴏsᴛ: 1 Pᴏɪɴᴛ

{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>""")
                    asyncio.create_task(schedule_delete(m))
                    return
                if mode in ("UPGRADE", "INVITE"):
                    await process_feature(event, mode)
                    return
                if mode == "STATS":
                    await show_stats(event)
                    return
            
            # Admin Panel
            if txt == "Aᴅᴍɪɴ Pᴀɴᴇʟ":
                await admin_panel(event)
                return
            
            # Page navigation
            if txt == "Nᴇxᴛ Pᴀɢᴇ":
                s["page"] = 2
                save_settings(s)
                await main_menu(event)
                return
            if txt == "◀ Pʀᴇᴠɪᴏᴜs Pᴀɢᴇ":
                s["page"] = 1
                save_settings(s)
                await main_menu(event)
                return
            
            # ---- BYPASS LINK ----
            if txt.startswith('http://') or txt.startswith('https://'):
                user = get_user(uid)
                if not user.get("verified"):
                    if await check_channels(uid):
                        user["verified"] = True
                        save_user(uid, user)
                    else:
                        await show_verification_page(event)
                        return
                if user.get("credits", 0) <= 0:
                    m = await send_html(event.chat_id, f"<blockquote>{E_CROSS} No credits! +10 daily | +3 invite</blockquote>")
                    asyncio.create_task(schedule_delete(m))
                    return
                
                # Send processing message
                processing = await send_html(
                    event.chat_id,
                    f"""<blockquote>{E_SEARCH} Pʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ʟɪɴᴋ...

{E_LINK_ORIGINAL} {txt}

{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"""
                )
                
                use_credit(uid)
                
                async with aiohttp.ClientSession() as session:
                    result = await bypass_link(session, txt)
                
                await processing.delete()
                
                result_text = format_result(result, txt)
                sent = await send_html(event.chat_id, result_text)
                asyncio.create_task(schedule_delete(sent, 90))
                return
            
        except Exception as e:
            logger.error(f"Msg handler error: {e}")

# ---- 📋 FORMAT RESULT ----

def format_result(result, original_link):
    if not result.get("success"):
        return f"""<blockquote>{E_CROSS} Bʏᴘᴀss Fᴀɪʟᴇᴅ

{E_TOOLS} Error: {result.get('error', 'Unknown')}

{E_LINK_ORIGINAL} Original: {original_link}

{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"""

    return f"""<blockquote>{E_SPARKLE} Lɪɴᴋ Bʏᴘᴀss Sᴜᴄᴄᴇssғᴜʟ {E_SPARKLE}

{E_LINK_ORIGINAL} Oʀɪɢɪɴᴀʟ Lɪɴᴋ:
{result['original']}

{E_LINK_BYPASS} Bʏᴘᴀssᴇᴅ Lɪɴᴋ:
{result['bypassed']}

{E_LINK_TIME} Tɪᴍᴇ Tᴀᴋᴇɴ: {result['time']} seconds

{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"""

# ---- 📊 STATS ----

async def show_stats(event):
    user = get_user(event.sender_id)
    users = load_json(USERS_FILE)
    total_users = len(users)
    uid = str(event.sender_id)
    
    txt = f"""<blockquote>{E_SPARKLE} Yᴏᴜʀ Sᴛᴀᴛs {E_SPARKLE}

{E_WALLET} Credits: {user.get('credits', 0)}
{E_USERS} Total Queries: {user.get('total_queries', 0)}
{E_GIFT} Daily Queries: {user.get('daily_queries', 0)}
{E_USERS} Invites: {user.get('invites', 0)}
{E_CROWN} Premium: {'✅' if user.get('premium', False) else '❌'}

{E_DIAMOND} Gʟᴏʙᴀʟ Sᴛᴀᴛs
{E_USERS} Total Users: {total_users}

{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"""
    m = await send_html(event.chat_id, txt)
    asyncio.create_task(schedule_delete(m, 60))

# ---- 📋 COMMANDS ----

async def show_commands(event):
    txt = f"""<blockquote>{E_DIAMOND} Aᴠᴀɪʟᴀʙʟᴇ Cᴏᴍᴍᴀɴᴅs {E_DIAMOND}

<b>Slash commands (use in any chat):</b>
/bypass <code>https://earnlinks.in/WoivZ</code> – Bypass any link
/invite – Get your invite link
/upgrade – Premium upgrade info
/stats – Your statistics
/help or /commands – Show this list

<b>Menu buttons</b> (private chat only)
Blue buttons for services, Green for Invite/Upgrade, Red for navigation.

{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"""
    return await send_html(event.chat_id, txt)

# ---- 🚀 START ----

async def main():
    print("🚀 LINK SHORTENER BYPASS BOT STARTED")
    print("✅ Premium Emojis Enabled")
    print("✅ Button Colors Active")
    print(f"✅ API: {BYPASS_API}")
    print("✅ Admin Panel Ready")
    print("✅ Invite & Credit System Active")
    await client.start(bot_token=BOT_TOKEN)
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Bot stopped by user")
    except Exception as e:
        print(f"Error: {e}")