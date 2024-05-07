from cryptography.fernet import Fernet
import login_system.constants as c
import login_system.settings as s
import os, sys, shutil
from dotenv import set_key

def get_resource_path(relative_path: str="") -> str:
    """Gets absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def create_encryption_key() -> None:
    """Creates a unique encryption key on first time"""
    if os.path.exists(get_resource_path(c.ENCRYPTION_KEY_PATH)):
        pass
    else:
        key = Fernet.generate_key()
        open(get_resource_path(c.ENCRYPTION_KEY_PATH), "w")
        set_key(get_resource_path(c.ENCRYPTION_KEY_PATH), "ENCRYPTION_KEY", key.decode())
        c.ENCRYPTION_KEY = key

def create_txt_file() -> None:
    """Creates a txt file for login details (encrypted)"""
    if os.path.exists(get_resource_path(c.LOGIN_DATA_PATH)):
        pass
    else:
        open(get_resource_path(c.LOGIN_DATA_PATH), "w")

def check_username_exist(username: str) -> bool:
    """Checks to see if username already exists.\n
    Returns True if it does, False if it doesn't"""
    fernet = Fernet(c.ENCRYPTION_KEY)
    with open(get_resource_path(c.LOGIN_DATA_PATH), "rb") as f:
        lines = [line.decode().split(",") for line in f.readlines()]

        for _, line in enumerate(lines, start=1):
            docusername = fernet.decrypt(line[0].encode()).decode().strip()

            if username in docusername:
                return True
    return False

def encrypt_signup_details(username: str, password: str, directory: str) -> None:
    """Encrypts new users' details"""
    fernet = Fernet(c.ENCRYPTION_KEY)
    encrypted_username = fernet.encrypt(username.encode())
    encrypted_password = fernet.encrypt(password.encode())
    encrypted_directory = fernet.encrypt(directory.encode())
    data = b",".join([
                encrypted_username, encrypted_password, encrypted_directory
                ]) + b'\n'
    with open(get_resource_path(c.LOGIN_DATA_PATH), "ab") as f:
        f.write(data)

def check_details(username: str, password: str) -> bool:
    """Checks to see if credentials entered are correct"""
    fernet = Fernet(c.ENCRYPTION_KEY)
    with open(get_resource_path(c.LOGIN_DATA_PATH), "rb") as f:
        lines = [line.decode().split(",") for line in f.readlines()]

    for _, line in enumerate(lines, start=1):
        docusername = fernet.decrypt(line[0].encode()).decode().strip()
        docpassword = fernet.decrypt(line[1].strip().encode()).decode()

        if username == docusername and password == docpassword:
            return True

    return False

def get_user_dir(username: str) -> str:
    """Finds user's directory"""
    fernet = Fernet(c.ENCRYPTION_KEY)
    with open(get_resource_path(c.LOGIN_DATA_PATH), "rb") as f:
        lines = [line.decode().split(",") for line in f.readlines()]

    for _, line in enumerate(lines, start=1):
        docusername = fernet.decrypt(line[0].encode()).decode().strip()
        docdir = fernet.decrypt(line[2].encode()).decode().strip()
        
        if docusername == username:
            return docdir
        
def create_necessary_files(username: str, directory: str) -> None:
    """Creates necessary files in the user's dir"""
    s.make_default_settings_file(c.DEFAULT_SETTINGS, f"{directory}/{username}.ini")
    s.edit_setting(*c.ACCOUNT_DIRECTORY_SETTING_LOCATOR, directory, f"{directory}/{username}.ini")
    open(f"{directory}/{username}.txt", "w")

def move_files(username: str, src: str, dst: str) -> None:
    fernet = Fernet(c.ENCRYPTION_KEY)
    shutil.move(f"{src}/{username}.ini", f"{dst}/{username}.ini")
    shutil.move(f"{src}/{username}.txt", f"{dst}/{username}.txt")

    encrypted_dir = fernet.encrypt(dst.encode())
    with open(get_resource_path(c.LOGIN_DATA_PATH), "rb") as f:
        lines = [line.decode().split(",") for line in f.readlines()]

    for i, line in enumerate(lines, start=1):
        docusername = fernet.decrypt(line[0].encode()).decode().strip()

        if username == docusername:
            line[2] = encrypted_dir.decode()
            lines[i-1] = ",".join(line) + "\n"
            break

    with open(get_resource_path(c.LOGIN_DATA_PATH), "wb") as f:
        f.writelines(bytes(line, "utf-8") for line in lines)