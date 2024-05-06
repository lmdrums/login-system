import os
from dotenv import load_dotenv

# Directories
IMAGES_FOLDER_PATH = os.path.join("login_system", "images")
FILES_FOLDER_PATH = os.path.join("login_system", "files")
ASSETS_FOLDER_PATH = os.path.join("login_system", "assets")

# Main window
MAIN_TITLE = "Login"
MAIN_GEOMETRY = "960x540+480+270"
WINDOW_ICON = os.path.join(IMAGES_FOLDER_PATH, "logo.ico")
BACKGROUND = os.path.join(IMAGES_FOLDER_PATH, "background.png")

# Signup window
SIGNUP_TITLE = "Signup"
SIGNUP_GEOMETRY = "300x200+580+370"

# Encryption key
ENCRYPTION_KEY_PATH = os.path.join(FILES_FOLDER_PATH, ".env")
LOGIN_DATA_PATH = os.path.join(FILES_FOLDER_PATH, ".txt")
load_dotenv(ENCRYPTION_KEY_PATH)
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

# Account window
ACCOUNT_GEOMETRY = "960x540+480+270"
NOTIFICATION_ICON = os.path.join(IMAGES_FOLDER_PATH, "iconpng.png")
NOTIFICATION_SOUND_PATH = os.path.join(FILES_FOLDER_PATH, "notification.wav")

# Images
SIGNIN_IMAGE_PATH = os.path.join(IMAGES_FOLDER_PATH, "signin.png")
SIGNUP_IMAGE_PATH = os.path.join(IMAGES_FOLDER_PATH, "signup.png")
FIND_IMAGE_PATH = os.path.join(IMAGES_FOLDER_PATH, "find.png")

# Misc
DEFAULT_THEME = os.path.join(ASSETS_FOLDER_PATH, "theme.json")