from customtkinter import (CTk, CTkLabel, CTkEntry, CTkButton,
                           CTkScrollableFrame, CTkImage, CTkFrame,
                           CTkSlider, CTkCheckBox, StringVar,
                           set_appearance_mode, set_default_color_theme,
                           filedialog, END)
from PIL import Image, ImageTk
from notifypy import Notify
import pyperclip

import sys, os
from tkinter import Toplevel, messagebox, Menu, Button
import webbrowser
from random import choices
import string

import login_system.helpers as h
import login_system.constants as c
import login_system.settings as s

set_appearance_mode("light")
set_default_color_theme(c.DEFAULT_THEME)

get_pillow_image = lambda relative_path: Image.open(h.get_resource_path(relative_path))

signin_image = CTkImage(light_image=get_pillow_image(c.SIGNIN_IMAGE_PATH),
                dark_image=get_pillow_image(c.SIGNIN_IMAGE_PATH))
signup_image = CTkImage(light_image=get_pillow_image(c.SIGNUP_IMAGE_PATH),
                dark_image=get_pillow_image(c.SIGNUP_IMAGE_PATH))
find_image = CTkImage(light_image=get_pillow_image(c.FIND_IMAGE_PATH),
                dark_image=get_pillow_image(c.FIND_IMAGE_PATH))
copy_image = CTkImage(light_image=get_pillow_image(c.COPY_IMAGE_PATH),
                dark_image=get_pillow_image(c.COPY_IMAGE_PATH), size=(17,17))
retry_image = CTkImage(light_image=get_pillow_image(c.RETRY_IMAGE_PATH),
                dark_image=get_pillow_image(c.RETRY_IMAGE_PATH))

class DisablePasswordMask(Button):
    def __init__(self, master, entry, **kwargs):
        tk_image = Image.open(c.PWORD_UNMASK_IMAGE_PATH)
        tk_image = tk_image.resize((24, 24))
        self.unmask = ImageTk.PhotoImage(tk_image)
        super().__init__(master, image=self.unmask, **kwargs)
        self.entry = entry
        self.bind("<Button-1>", lambda _: self.held_down())
        self.bind("<ButtonRelease-1>", lambda _: self.button_up())
        self.activate = False

    def held_down(self):
        self.configure(relief="sunken")
        self.entry.configure(show="")
        self.activate = True

    def button_up(self):
        self.configure(relief="raised")
        self.entry.configure(show="●")
        self.activate = False

class App(CTk):
    def __init__(self):
        super().__init__()

        self.title(c.MAIN_TITLE)
        self.geometry(c.MAIN_GEOMETRY)
        
        if sys.platform.startswith("win"):
            self.iconbitmap(h.get_resource_path(c.WINDOW_ICON))

        self.bg_pil = Image.open(h.get_resource_path(c.BACKGROUND))

        self.bg_photo = CTkLabel(self, text="")
        self.bg_photo.place(x=0, y=0)

        self.columnconfigure(0, weight=100)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=10)
        self.columnconfigure(3, weight=100)

        self.rowconfigure(0, weight=50)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=50)

        self.username_entry= CTkEntry(self, placeholder_text="Enter username",
                                      width=250)
        self.username_entry.grid(row=1, column=1, sticky="ew")

        self.password_entry = CTkEntry(self, placeholder_text="Enter password",
                                       width=250, show="●")
        self.password_entry.grid(row=2, column=1, sticky="ew")

        self.password_unmask = DisablePasswordMask(self, self.password_entry, bd=0, background="#F9F9FA")
        self.password_unmask.grid(row=2, column=1, sticky="e")
        
        self.submit_button = CTkButton(self, text="Sign In", image=signin_image,
                                       width=200, command=self.submit)
        self.submit_button.grid(column=1, row=3, pady=(10,0))

        self.signup_button = CTkButton(self, text="Sign Up", image=signup_image,
                                       width=200, command=self.signup_function)
        self.signup_button.grid(column=1, row=4)

        self.username_entry.bind("<Return>", lambda _: self.submit())
        self.password_entry.bind("<Return>", lambda _: self.submit())

        self.resize_image()

    def signup_function(self):
        signup = Signup()
        signup.mainloop()

    def submit(self):
        username_entered = self.username_entry.get()
        password_entered = self.password_entry.get()

        if username_entered:
            if password_entered:
                if h.check_details(username_entered, password_entered):
                    self.destroy()
                    account = Account(username_entered)
                    account.mainloop()
                else:
                    messagebox.showerror(title="Error", message="Username or password incorrect.")
            else:
                messagebox.showerror(title="Invalid Input",
                                 message="Please enter a valid password.")
                return
        else:
            messagebox.showerror(title="Invalid Input",
                                 message="Please enter a valid username.")
            return

        h.check_details(username_entered, password_entered)

    def resize_image(self):
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        img_width, img_height = self.bg_pil.size
        aspect_ratio = img_width / img_height

        if window_width / window_height > aspect_ratio:
            new_width = window_width
            new_height = int(window_width / aspect_ratio)
        else:
            new_width = int(window_height * aspect_ratio)
            new_height = window_height

        resized_img = self.bg_pil.resize((new_width, new_height))
        resized_img = ImageTk.PhotoImage(resized_img)

        self.bg_photo.configure(image=resized_img)

        self.after_loop = self.after(75, self.resize_image)

class Signup(Toplevel):
    def __init__(self):
        super().__init__()
        self.title(c.SIGNUP_TITLE)
        self.geometry(c.SIGNUP_GEOMETRY)

        if sys.platform.startswith("win"):
            self.iconbitmap(h.get_resource_path(c.WINDOW_ICON))
        
        self.frame = CTkFrame(self, fg_color="#000e20", corner_radius=0)
        self.frame.pack(fill="both", expand=True)
        self.frame.columnconfigure(0, weight=1)

        self.username_entry= CTkEntry(self.frame, placeholder_text="Enter username",
                                      width=250)
        self.username_entry.grid(column=0, row=100, pady=(0,70))
        self.username_entry.focus()

        self.password_entry = CTkEntry(self.frame, placeholder_text="Enter password",
                                       width=250, show="●")
        self.password_entry.grid(column=0, row=100, pady=(0,0))

        self.submit_button = CTkButton(self.frame, text="Create Account", image=signup_image,
                                       width=200, command=self.create_login)
        self.submit_button.grid(column=0, row=100, pady=(80,0))

        self.username_entry.bind("<Return>", lambda _: self.create_login())
        self.password_entry.bind("<Return>", lambda _: self.create_login())
    
    def create_login(self):
        username_entered = self.username_entry.get()
        password_entered = self.password_entry.get()

        if username_entered:
            if password_entered:
                if h.check_username_exist(username_entered):
                    messagebox.showerror(title="Invalid Input", 
                                         message="Username already exists.")
                    self.lift()
                    self.username_entry.focus()
                    return
                
                dir = self.choose_dir()
                if dir is None:
                    return
                
                try:
                    h.encrypt_signup_details(username_entered, password_entered, dir)
                    h.create_necessary_files(username_entered, dir)
                except PermissionError or FileExistsError or FileNotFoundError:
                    return

                messagebox.showinfo(title="Success", message="Account successfully created.")
                self.destroy()
            else:
                messagebox.showerror(title="Invalid Input",
                                 message="Please enter a valid password.")
                self.lift()
                self.password_entry.focus()
                return
        else:
            messagebox.showerror(title="Invalid Input",
                                 message="Please enter a valid username.")
            self.lift()
            self.username_entry.focus()
            return
    
    def choose_dir(self) -> str:
        file = filedialog.askdirectory(title="Choose a folder to store account files")
        if file:
            return file
        else:
            return

class Account(CTk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.user_directory = h.get_user_dir(self.username)
        self.settings_file_dir = h.get_user_settings_file(self.user_directory, self.username)

        self.title(self.username)
        self.geometry(c.ACCOUNT_GEOMETRY)
        
        if sys.platform.startswith("win"):
            self.iconbitmap(h.get_resource_path(c.WINDOW_ICON))
        
        self.menu = Menu(self)
        self.config(menu=self.menu)
        self.filemenu = Menu(self.menu, tearoff="off")

        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="⚙ Preferences    ", command=self.preferences, accelerator="Ctrl+Shift+P    ", hidemargin=True)

        self.frame = CTkScrollableFrame(self)
        self.frame.pack(fill="both", expand=True, pady=20, padx=20)
        self.frame.columnconfigure(1, weight=480)

        welcome = Notify()
        welcome.title = "Welcome!"
        welcome.message = f"Welcome {username}. Good to see you."
        if os.path.exists(f"{self.user_directory}/{self.username}_pfp.png"):
            welcome.icon = f"{self.user_directory}/{self.username}_pfp.png"
        else:
            welcome.icon = h.get_resource_path(c.NOTIFICATION_ICON)
        welcome.audio = h.get_resource_path(c.NOTIFICATION_SOUND_PATH)

        welcome.send()

        self.welcome_label = CTkLabel(self.frame, font=("Segoe UI", 20, "bold"),
                                      text=f"Welcome to your account, {username}.")
        self.welcome_label.grid(row=0, column=0, padx=10, pady=(10,0), sticky="w")

        self.profile_pic = CTkLabel(self.frame, text="")
        self.profile_pic.grid(row=0, column=1, padx=10, pady=(10,0), sticky="e")

        self.web_search_entry = CTkEntry(self.frame, placeholder_text="Search web",
                                       width=400)
        self.web_search_entry.grid(row=1, column=0, padx=10, pady=(10,0), sticky="w")
        self.web_search_entry.bind("<Return>", lambda _: self.web_search())

        self.web_search_button = CTkButton(self.frame, text="", image=find_image,
                                           command=self.web_search, width=60)
        self.web_search_button.grid(row=1, column=0, padx=(400,0), pady=(10,0), sticky="w")

        self.password_generator_label = CTkLabel(self.frame, text="Password Generator",
                                                 font=("Segoe UI", 15, "bold"))
        self.password_generator_label.grid(row=2, column=0, padx=10, pady=(10,0), sticky="w")

        self.password_generator_entry = CTkEntry(self.frame, placeholder_text="Password will appear here",
                                                 width=250)
        self.password_generator_entry.grid(row=3, column=0, padx=10, pady=(10,0), sticky="w")
        self.password_generator_entry.configure(state="disabled")

        self.retry_password = CTkButton(self.frame, text="", width=28, height=26, 
                                        image=retry_image, command=self.change_password)
        self.retry_password.grid(row=3, column=0, pady=(10,0), padx=232, sticky="w")

        self.password_copy_button = CTkButton(self.frame, text="Copy", command=self.copy_password,
                                              image=copy_image, width=80)
        self.password_copy_button.grid(row=3, column=0, padx=(258, 0), pady=(10,0), sticky="w")

        self.password_length_slider = CTkSlider(self.frame, from_=1, to=25, number_of_steps=24,
                                                command=self.change_pword_length, width=250)
        self.password_length_slider.grid(row=4, column=0, padx=10, pady=(10,0), sticky="w")

        self.password_length_entry = CTkEntry(self.frame, width=40, justify="center")
        self.password_length_entry.grid(row=4, column=0, padx=(270,0), pady=(10,0), sticky="w")
        self.password_length_entry.bind("<KeyRelease>", lambda _: self.check_int_entry())

        self.password_length_slider.set(1)
        self.password_length_entry.insert(END, "1")

        self.previous_length = 1
        self.capital_letters_onoff = StringVar(value="off")
        self.lowercase_letters_onoff = StringVar(value="off")
        self.numbers_onoff = StringVar(value="off")
        self.symbols_onoff = StringVar(value="off")
        self.capital_letters_check = CTkCheckBox(self.frame, checkbox_height=20,
                                    variable=self.capital_letters_onoff,
                                    checkbox_width=20, height=20, text="Capital Letters", 
                                    offvalue="off", onvalue="on",
                                    command=self.change_password)
        self.capital_letters_check.grid(row=5, column=0, padx=(10,0), pady=(20,0), sticky="w")

        self.lowercase_letters_check = CTkCheckBox(self.frame, checkbox_height=20,
                                    variable=self.lowercase_letters_onoff,
                                    checkbox_width=20, height=20, text="Lowercase Letters",
                                    offvalue="off", onvalue="on",
                                    command=self.change_password)
        self.lowercase_letters_check.grid(row=5, column=0, padx=(130,0), pady=(20,0), sticky="w")

        self.numbers_check = CTkCheckBox(self.frame, checkbox_height=20,
                                    variable=self.numbers_onoff,
                                    checkbox_width=20, height=20, text="Numbers",
                                    offvalue="off", onvalue="on", 
                                    command=self.change_password)
        self.numbers_check.grid(row=5, column=0, padx=(280,0), pady=(20,0), sticky="w")

        self.symbols_check = CTkCheckBox(self.frame, checkbox_height=20,
                                    variable=self.symbols_onoff,
                                    checkbox_width=20, height=20, text="Symbols",
                                    offvalue="off", onvalue="on",
                                    command=self.change_password)
        self.symbols_check.grid(row=5, column=0, padx=(380,0), pady=(20,0), sticky="w")

        self.bind_all("<Control-Shift-KeyPress-P>", lambda _: self.preferences())
        self.load_pfp()

    def load_pfp(self):
        pfp = h.load_pfp(self.username)
        if pfp:
            resized = pfp.resize((75,75))
            pfp_tk = ImageTk.PhotoImage(resized)
            self.profile_pic.configure(image=pfp_tk)

    def check_int_entry(self):
        if self.password_length_entry.get():
            try:
                int_val = int(self.password_length_entry.get())
                self.password_length_entry.configure(border_color="#979DA2")
                self.password_length_slider.set(int_val)
                self.change_password()
            except ValueError:
                self.password_length_entry.configure(border_color="red")
        else:
            self.password_length_entry.configure(border_color="red")

    def copy_password(self):
        password = self.password_generator_entry.get()
        if password:
            pyperclip.copy(password)

    def change_pword_length(self, length):
        self.password_length_entry.delete(0, END)
        self.password_length_entry.insert(END, int(length))
        self.make_password()

    def make_password(self):
        length = self.password_length_slider.get()
        if length != self.previous_length:
            self.change_password()           
            
    def change_password(self):
        length = self.password_length_entry.get()
        int_length = int(length)
        password_choices = []
        if self.capital_letters_check.get() == "on":
            password_choices.append("caps")
        if self.lowercase_letters_check.get() == "on":
            password_choices.append("lower")
        if self.numbers_check.get() == "on":
            password_choices.append("numbers")
        if self.symbols_check.get() == "on":
            password_choices.append("symbols")

        password_dict = {
            "caps": string.ascii_uppercase,
            "lower": string.ascii_lowercase,
            "numbers": string.digits,
            "symbols": string.punctuation
        }

        val = ""
        for item in password_choices:
            val += password_dict[item]

        if val != "":
            password = "".join(choices(val, k=int_length))
            self.password_generator_entry.configure(state="normal")
            self.password_generator_entry.delete(0, END)
            self.password_generator_entry.insert(END, password)
            self.password_generator_entry.configure(state="disabled")
            self.previous_length = int_length
    
    def web_search(self):
        arg = self.web_search_entry.get()
        if arg:
            links = ["https://", "http://", ".com", ".org", ".uk", "www."]
            if any(link in arg for link in links):
                webbrowser.open(arg)
            else:
                webbrowser.open(f"https://www.google.com/search?q={arg}")
        else:
            messagebox.showerror(title="Invalid Input", message="Please enter a valid query.")
    
    def preferences(self):
        preferences_window = Preferences(self.username)
        preferences_window.mainloop()

class Preferences(Toplevel):
    def __init__(self, username: str):
        super().__init__()
        self.username = username
        self.focus()
        self.title(f"Preferences - {username}")
        self.geometry(c.PREFERENCES_GEOMETRY)
        if sys.platform.startswith("win"):
            self.iconbitmap(h.get_resource_path(c.WINDOW_ICON))
        
        self.frame = CTkScrollableFrame(self)
        self.frame.pack(fill="both", expand=True, pady=10, padx=10)

        self.general_header = CTkLabel(self.frame, text="General", 
                                       font=("Segoe UI", 15, "bold"))
        self.general_header.grid(column=0, row=0, padx=10, pady=(10,0), sticky="w")

        self.account_directory_label = CTkLabel(self.frame, text="Account Directory")
        self.account_directory_label.grid(column=0, row=1, padx=10, pady=(10,0), sticky="w")
        self.account_directory_entry = CTkEntry(self.frame, width=500,
                                      placeholder_text="Account directory path (C:/...)")
        self.account_directory_entry.grid(column=1, row=1, pady=(10,0))
        self.account_dir_change = CTkButton(self.frame, text="Change  ",
                                        width=70, command=self.change_account_dir)
        self.account_dir_change.grid(column=2, row=1, pady=(10,0))

        self.profile_pic_label = CTkLabel(self.frame, text="Profile Picture")
        self.profile_pic_label.grid(column=0, row=2, padx=10, pady=(10,0), sticky="w")
        self.profile_pic_entry = CTkEntry(self.frame, width=500,
                                      placeholder_text="Account directory path (C:/...)")
        self.profile_pic_entry.grid(column=1, row=2, pady=(10,0))
        self.profile_pic_change = CTkButton(self.frame, text="Change  ",
                                        width=70, command=self.change_pfp)
        self.profile_pic_change.grid(column=2, row=2, pady=(10,0))

        self.load_settings()

    def change_pfp(self):
        self.focus()
        file = filedialog.askopenfile(title="Choose a profile picture",
                                      filetypes=[
                                          ("Image Files", "*.png, *.jpg"),
                                          ("BMP File (*.bmp)", "*.bmp"),
                                          ("TIFF File (*.tiff)", "*.tiff"),
                                          ("All Files (*.*)", "*.*")
                                      ])
        if file:
            h.make_profile_picture(file.name, self.username)
            s.edit_setting(*c.PROFILE_PICTURE_SETTING_LOCATOR, file.name, 
                        h.get_user_settings_file(h.get_user_dir(self.username), self.username))
            self.profile_pic_entry.delete(0, END)
            self.profile_pic_entry.insert(END, file.name)
        self.focus()

    def change_account_dir(self):
        self.focus()
        current_dir = h.get_user_dir(self.username)
        file = filedialog.askdirectory(title="Choose a new folder to store account files")
        self.account_directory_entry.delete(0, END)
        self.account_directory_entry.insert(END, file)
        h.move_files(self.username, current_dir, file)
        self.focus()

    def load_settings(self):
        self.focus()
        self.account_directory_entry.delete(0, END)
        self.account_directory_entry.insert(END, h.get_user_dir(self.username))
        self.profile_pic_entry.delete(0, END)
        self.profile_pic_entry.insert(END, s.get_setting(h.get_user_settings_file(h.get_user_dir(self.username), self.username),
                                                         *c.PROFILE_PICTURE_SETTING_LOCATOR))
        self.focus()

def main():
    app = App()
    app.mainloop()