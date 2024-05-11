import os
from dotenv import load_dotenv

# Settings
GENERAL_SETTINGS_SECTION = "GENERAL"
ACCOUNT_DIRECTORY_SETTING_LOCATOR = (GENERAL_SETTINGS_SECTION, "account_directory")

DEFAULT_SETTINGS = {
    GENERAL_SETTINGS_SECTION: {
        ACCOUNT_DIRECTORY_SETTING_LOCATOR[1]: ""
    }
}

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
SIGNUP_GEOMETRY = "300x150+490+310"

# Preferences window
PREFERENCES_GEOMETRY = "960x540+580+370"

# Account window
ACCOUNT_GEOMETRY = "960x540+480+270"
NOTIFICATION_ICON = os.path.join(IMAGES_FOLDER_PATH, "iconpng.png")
NOTIFICATION_SOUND_PATH = os.path.join(FILES_FOLDER_PATH, "notification.wav")

# Encryption key
ENCRYPTION_KEY_PATH = f"{FILES_FOLDER_PATH}/.env"
LOGIN_DATA_PATH = f"{FILES_FOLDER_PATH}/.txt"
load_dotenv(ENCRYPTION_KEY_PATH)
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

# Images
SIGNIN_IMAGE_PATH = os.path.join(IMAGES_FOLDER_PATH, "signin.png")
SIGNUP_IMAGE_PATH = os.path.join(IMAGES_FOLDER_PATH, "signup.png")
FIND_IMAGE_PATH = os.path.join(IMAGES_FOLDER_PATH, "find.png")
PWORD_UNMASK_IMAGE_PATH = os.path.join(IMAGES_FOLDER_PATH, "pword_unmask.png")
COPY_IMAGE_PATH = os.path.join(IMAGES_FOLDER_PATH, "copy.png")
RETRY_IMAGE_PATH = os.path.join(IMAGES_FOLDER_PATH, "retry.png")

# Misc
DEFAULT_THEME = os.path.join(ASSETS_FOLDER_PATH, "theme.json")