from login_system.gui import main as gui
from login_system.helpers import create_encryption_key, create_txt_file

def main():
    create_encryption_key()
    create_txt_file()
    gui()

if __name__ == "__main__":
    main()