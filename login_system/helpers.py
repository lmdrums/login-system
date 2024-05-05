from cryptography.fernet import Fernet
import login_system.constants as c
import os, sys
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
        
        with open(get_resource_path(c.ENCRYPTION_KEY_PATH), "w"):
            pass
        
        set_key(get_resource_path(c.ENCRYPTION_KEY_PATH), "ENCRYPTION_KEY", key.decode())
        c.ENCRYPTION_KEY = key

def create_txt_file() -> None:
    if os.path.exists(get_resource_path(c.LOGIN_DATA_PATH)):
        pass
    else:
        with open(get_resource_path(c.LOGIN_DATA_PATH), "w"):
            pass

def check_username_exist(username: str) -> bool:
    fernet = Fernet(c.ENCRYPTION_KEY)
    with open(get_resource_path(c.LOGIN_DATA_PATH), "rb") as f:
        lines = [line.decode().split(",") for line in f.readlines()]

        for _, line in enumerate(lines, start=1):
            docusername = fernet.decrypt(line[0].encode()).decode().strip()

            if username in docusername:
                return True
    return False

def encrypt_signup_details(username: str, password: str) -> None:
    """Encrypts new users' details"""
    fernet = Fernet(c.ENCRYPTION_KEY)
    encrypted_username = fernet.encrypt(username.encode())
    encrypted_password = fernet.encrypt(password.encode())
    data = b",".join([
                encrypted_username, encrypted_password
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