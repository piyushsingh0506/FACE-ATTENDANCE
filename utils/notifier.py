import os
import threading
import logging
from datetime import datetime, date

from config import (
    ENABLE_NOTIFICATIONS,
    NOTIFICATION_CHANNEL,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER,
    TWILIO_WHATSAPP_NUMBER,
    FAST2SMS_API_KEY,
    ADMIN_PHONE_NUMBER
)

from database import add_notification

logger = logging.getLogger("Notifier")


# ==========================================================
# FORMAT PHONE NUMBER
# ==========================================================

def format_phone_number(phone_raw, default_country_code="+91"):
    """
    Standardize phone number with country code (defaults to India +91 if missing).
    """
    if not phone_raw:
        return ""
    
    cleaned = str(phone_raw).strip().replace(" ", "").replace("-", "")
    
    if cleaned.startswith("+"):
        return cleaned
    elif len(cleaned) == 10:
        return f"{default_country_code}{cleaned}"
    elif len(cleaned) == 12 and cleaned.startswith("91"):
        return f"+{cleaned}"
    
    return f"+{cleaned}"


# ==========================================================
# MESSAGE TEMPLATES
# ==========================================================

def get_attendance_message(name, person_id, time_str, date_str):
    return (
        f"✅ Attendance Confirmed!\n"
        f"👤 Name: {name}\n"
        f"🆔 ID: {person_id}\n"
        f"📅 Date: {date_str}\n"
        f"⏰ Time: {time_str}\n"
        f"📍 Status: Present (Face Recognized)"
    )


# ==========================================================
# SEND VIA TWILIO SMS
# ==========================================================

def _send_twilio_sms(to_number, message_text):
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_PHONE_NUMBER:
        return False, "Twilio credentials (ACCOUNT_SID, AUTH_TOKEN, PHONE_NUMBER) not configured."
    
    try:
        from twilio.rest import Client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        message = client.messages.create(
            body=message_text,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        return True, f"Sent via Twilio SMS (SID: {message.sid})"
    except Exception as e:
        return False, f"Twilio SMS error: {str(e)}"


# ==========================================================
# SEND VIA TWILIO WHATSAPP
# ==========================================================

def _send_twilio_whatsapp(to_number, message_text):
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        return False, "Twilio credentials not configured."
    
    try:
        from twilio.rest import Client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        whatsapp_to = to_number if to_number.startswith("whatsapp:") else f"whatsapp:{to_number}"
        whatsapp_from = TWILIO_WHATSAPP_NUMBER if TWILIO_WHATSAPP_NUMBER.startswith("whatsapp:") else f"whatsapp:{TWILIO_WHATSAPP_NUMBER}"
        
        message = client.messages.create(
            body=message_text,
            from_=whatsapp_from,
            to=whatsapp_to
        )
        return True, f"Sent via Twilio WhatsApp (SID: {message.sid})"
    except Exception as e:
        return False, f"Twilio WhatsApp error: {str(e)}"


# ==========================================================
# SEND VIA FAST2SMS (INDIA)
# ==========================================================

def _send_fast2sms(to_number, message_text):
    api_key = os.getenv("FAST2SMS_API_KEY", FAST2SMS_API_KEY)
    if not api_key:
        return False, "FAST2SMS_API_KEY not configured in .env"
    
    try:
        import urllib.request
        import urllib.parse
        import json

        # Extract last 10 digits for Indian number
        cleaned_num = "".join(filter(str.isdigit, to_number))[-10:]
        if len(cleaned_num) != 10:
            return False, f"Invalid 10-digit Indian phone number: {to_number}"
        
        url = "https://www.fast2sms.com/dev/bulkV2"
        data = urllib.parse.urlencode({
            "authorization": api_key,
            "route": "q",
            "message": message_text,
            "language": "english",
            "flash": 0,
            "numbers": cleaned_num
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "authorization": api_key,
                "User-Agent": "Mozilla/5.0",
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )

        with urllib.request.urlopen(req, timeout=12) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            if res_data.get("return") is True:
                return True, "Sent via Fast2SMS"
            else:
                msg_list = res_data.get("message", ["Fast2SMS Error"])
                err_text = ", ".join(msg_list) if isinstance(msg_list, list) else str(msg_list)
                return False, f"Fast2SMS: {err_text}"
    except Exception as e:
        return False, f"Fast2SMS error: {str(e)}"


# ==========================================================
# SEND VIA CALLMEBOT (FREE WHATSAPP)
# ==========================================================

CALLMEBOT_API_KEY = os.getenv("CALLMEBOT_API_KEY", "")

def _send_callmebot_whatsapp(to_number, message_text):
    api_key = CALLMEBOT_API_KEY or os.getenv("CALLMEBOT_API_KEY", "")
    if not api_key:
        return False, "CALLMEBOT_API_KEY not configured in .env"
    
    try:
        import urllib.request
        import urllib.parse

        # Clean number to +91XXXXXXXXXX format
        cleaned_num = "".join(filter(str.isdigit, to_number))
        if len(cleaned_num) == 10:
            cleaned_num = f"91{cleaned_num}"
        
        encoded_text = urllib.parse.quote(message_text)
        url = f"https://api.callmebot.com/whatsapp.php?phone={cleaned_num}&text={encoded_text}&apikey={api_key}"
        
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        
        with urllib.request.urlopen(req, timeout=12) as response:
            res_content = response.read().decode("utf-8")
            if "Message queued" in res_content or "Success" in res_content or "OK" in res_content:
                return True, "Sent via WhatsApp (CallMeBot)"
            else:
                return True, f"Sent via WhatsApp: {res_content[:80]}"
    except Exception as e:
        return False, f"CallMeBot WhatsApp error: {str(e)}"


# ==========================================================
# SEND VIA TELEGRAM BOT (100% FREE MOBILE ALERTS)
# ==========================================================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

def _send_telegram(message_text, chat_id=None):
    token = os.getenv("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN)
    target_chat = chat_id or os.getenv("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID)
    
    if not token or not target_chat:
        return False, "TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not configured in .env"
    
    try:
        import urllib.request
        import urllib.parse
        import json

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = urllib.parse.urlencode({
            "chat_id": target_chat,
            "text": message_text
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            if res_data.get("ok") is True:
                return True, "Sent via Telegram Bot"
            else:
                return False, f"Telegram error: {res_data.get('description', 'Unknown error')}"
    except Exception as e:
        return False, f"Telegram error: {str(e)}"


# ==========================================================
# CORE SENDER FUNCTION
# ==========================================================

def _dispatch_notification(person_id, name, phone_number, channel, message_text):
    """
    Dispatches notification based on channel and logs to database.
    """
    formatted_phone = format_phone_number(phone_number)
    
    if not formatted_phone and channel != "telegram":
        logger.warning(f"No valid phone number for {name} ({person_id})")
        add_notification(
            person_id=person_id,
            recipient_name=name,
            phone_number=phone_number or "N/A",
            channel=channel,
            message=message_text,
            status="Failed",
            error_message="No phone number registered"
        )
        return False, "No phone number provided"

    success = False
    error_msg = None
    detail_status = "Sent"

    # Route based on channel
    if channel == "telegram":
        success, error_msg = _send_telegram(message_text)
    elif channel == "whatsapp":
        if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
            success, error_msg = _send_twilio_whatsapp(formatted_phone, message_text)
        elif CALLMEBOT_API_KEY or os.getenv("CALLMEBOT_API_KEY"):
            success, error_msg = _send_callmebot_whatsapp(formatted_phone, message_text)
        else:
            success = True
            detail_status = "Simulated WhatsApp"
            error_msg = "Simulated (Add Twilio or CALLMEBOT_API_KEY in .env)"
    elif channel == "fast2sms":
        success, error_msg = _send_fast2sms(formatted_phone, message_text)
    elif channel == "sms":
        if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
            success, error_msg = _send_twilio_sms(formatted_phone, message_text)
        elif FAST2SMS_API_KEY or os.getenv("FAST2SMS_API_KEY"):
            success, error_msg = _send_fast2sms(formatted_phone, message_text)
        else:
            # Simulation Mode
            success = True
            detail_status = "Simulated SMS"
            error_msg = "Simulated (Add Twilio or Fast2SMS keys in .env for real SMS)"
    else:
        # Simulation channel
        success = True
        detail_status = "Simulated"
        error_msg = "Simulated mode active"

    # Status to log
    status_str = detail_status if success else "Failed"

    # Log to SQLite DB
    try:
        add_notification(
            person_id=person_id,
            recipient_name=name,
            phone_number=formatted_phone,
            channel=channel,
            message=message_text,
            status=status_str,
            error_message=error_msg if not success or detail_status == "Simulated" else None
        )
    except Exception as db_err:
        logger.error(f"Error logging notification to DB: {db_err}")

    return success, error_msg or detail_status


# ==========================================================
# PUBLIC NOTIFICATION ENTRYPOINT
# ==========================================================

def send_attendance_notification(
    person_id,
    name,
    phone_number,
    time_str=None,
    date_str=None,
    async_send=True
):
    """
    Main entry point to send attendance notifications.
    Can run asynchronously to prevent blocking Streamlit rendering.
    """
    if not ENABLE_NOTIFICATIONS:
        return False, "Notifications are disabled in config."

    if not time_str:
        time_str = datetime.now().strftime("%I:%M:%S %p")
    if not date_str:
        date_str = date.today().strftime("%Y-%m-%d")

    message_text = get_attendance_message(
        name=name,
        person_id=person_id,
        time_str=time_str,
        date_str=date_str
    )

    channel = NOTIFICATION_CHANNEL

    def _worker():
        # 1. Send to the recognized individual
        _dispatch_notification(
            person_id=person_id,
            name=name,
            phone_number=phone_number,
            channel=channel,
            message_text=message_text
        )

        # 2. Optionally send alert copy to Admin
        if ADMIN_PHONE_NUMBER and ADMIN_PHONE_NUMBER != phone_number:
            admin_msg = f"🔔 [Admin Alert] Recognition recorded for {name} ({person_id}) at {time_str}."
            _dispatch_notification(
                person_id=person_id,
                name="Admin",
                phone_number=ADMIN_PHONE_NUMBER,
                channel=channel,
                message_text=admin_msg
            )

    if async_send:
        thread = threading.Thread(target=_worker, daemon=True)
        thread.start()
        formatted_phone = format_phone_number(phone_number)
        return True, f"Notification dispatched to {formatted_phone or 'phone'}"
    else:
        return _worker()


# ==========================================================
# DIRECT TEST ALERT SENDER
# ==========================================================

def send_direct_test_alert(
    phone_number,
    name="Test User",
    channel=None
):
    """
    Synchronously test sending a notification to verify setup.
    """
    selected_channel = channel or NOTIFICATION_CHANNEL
    msg = (
        f"🔔 [Test Alert - Face Attendance System]\n"
        f"Hello {name}, your attendance alert system is working properly!\n"
        f"Time: {datetime.now().strftime('%I:%M:%S %p')}\n"
        f"Channel: {selected_channel.upper()}"
    )

    success, status_or_err = _dispatch_notification(
        person_id="TEST001",
        name=name,
        phone_number=phone_number,
        channel=selected_channel,
        message_text=msg
    )

    return success, status_or_err, msg

