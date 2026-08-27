import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# ==========================================================
# BASE DIRECTORY
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ==========================================================
# DATA DIRECTORY
# ==========================================================

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

DATABASE_PATH = os.path.join(
    DATA_DIR,
    "attendance.db"
)


# ==========================================================
# APPLICATION SETTINGS
# ==========================================================

APP_TITLE = "Face Recognition Attendance"
APP_ICON = "👁️"


# ==========================================================
# FACE REGISTRATION
# ==========================================================

MIN_REGISTRATION_IMAGES = 5
MAX_REGISTRATION_IMAGES = 10


# ==========================================================
# FACE RECOGNITION
# ==========================================================

# Lower distance = more similar.
# This value should be calibrated using your own test data.
RECOGNITION_THRESHOLD = 0.65


# ==========================================================
# ATTENDANCE
# ==========================================================

# Prevent repeated attendance during continuous recognition.
ATTENDANCE_COOLDOWN = 60


# ==========================================================
# CAMERA
# ==========================================================

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480


# ==========================================================
# NOTIFICATIONS SETTINGS
# ==========================================================

# Toggle notifications (True = Enabled, False = Disabled)
ENABLE_NOTIFICATIONS = os.getenv("ENABLE_NOTIFICATIONS", "True").lower() in ("true", "1", "yes")

# Notification channel: "sms", "whatsapp", "fast2sms", "simulation"
NOTIFICATION_CHANNEL = os.getenv("NOTIFICATION_CHANNEL", "sms").lower()

# Twilio SMS / WhatsApp Settings
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

# Fast2SMS (Indian SMS Gateway) Settings
FAST2SMS_API_KEY = os.getenv("FAST2SMS_API_KEY", "")

# Optional Admin Phone Number to also receive recognition alerts
ADMIN_PHONE_NUMBER = os.getenv("ADMIN_PHONE_NUMBER", "")


# ==========================================================
# CREATE DATA DIRECTORY
# ==========================================================

os.makedirs(
    DATA_DIR,
    exist_ok=True
)