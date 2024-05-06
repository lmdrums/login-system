from customtkinter import (CTk, CTkToplevel, CTkLabel, CTkEntry, CTkButton,
                           CTkScrollableFrame, CTkImage, END, CTkFrame, 
                           set_appearance_mode, set_default_color_theme)
from PIL import Image, ImageTk
from notifypy import Notify
from time import strftime

import sys
from tkinter import Toplevel, messagebox, Menu, PhotoImage
import webbrowser

import login_system.helpers as h
import login_system.constants as c

set_appearance_mode("light")
set_default_color_theme(c.DEFAULT_THEME)

get_pillow_image = lambda relative_path: Image.open(h.get_resource_path(relative_path))

signin_image = CTkImage(light_image=get_pillow_image(c.SIGNIN_IMAGE_PATH),
                dark_image=get_pillow_image(c.SIGNIN_IMAGE_PATH))
signup_image = CTkImage(light_image=get_pillow_image(c.SIGNUP_IMAGE_PATH),
                dark_image=get_pillow_image(c.SIGNUP_IMAGE_PATH))
find_image = CTkImage(light_image=get_pillow_image(c.FIND_IMAGE_PATH),
                dark_image=get_pillow_image(c.FIND_IMAGE_PATH))

class App(CTk):
    def __init__(self):
        super().__init__()

        self.title(c.MAIN_TITLE)
        self.geometry(c.MAIN_GEOMETRY)
        
        if sys.platform.startswith("win"):
            self.iconbitmap(h.get_resource_path(c.WINDOW_ICON))
        else:
            pass
        
        self.frame = CTkFrame(self)
        self.frame.grid(column=0, row=0, sticky="nsew")
        self.frame.columnconfigure(0, weight=1)

        self.bg_pil = Image.open(c.BACKGROUND)

        self.bg_photo = CTkLabel(self.frame, text="")
        self.bg_photo.grid(column=0, row=0, sticky="nsew", rowspan=200)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.username_entry= CTkEntry(self.frame, placeholder_text="Enter username",
                                      width=250)
        self.username_entry.grid(column=0, row=100, pady=(0,120))

        self.password_entry = CTkEntry(self.frame, placeholder_text="Enter password",
                                       width=250, show="●")
        self.password_entry.grid(column=0, row=100, pady=(0,50))

        self.submit_button = CTkButton(self.frame, text="Sign In", image=signin_image,
                                       width=200, command=self.submit)
        self.submit_button.grid(column=0, row=100, pady=(40,0))

        self.signup_button = CTkButton(self.frame, text="Sign Up", image=signup_image,
                                       width=200, command=self.signup_function)
        self.signup_button.grid(column=0, row=100, pady=(120,0))

        self.username_entry.bind("<Return>", lambda e: self.submit())
        self.password_entry.bind("<Return>", lambda e: self.submit())

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
        else:
            pass
        
        self.frame = CTkFrame(self, fg_color="#000e20", corner_radius=0)
        self.frame.pack(fill="both", expand=True)
        self.frame.columnconfigure(0, weight=1)

        self.username_entry= CTkEntry(self.frame, placeholder_text="Enter username",
                                      width=250)
        self.username_entry.grid(column=0, row=100, pady=(0,70))

        self.password_entry = CTkEntry(self.frame, placeholder_text="Enter password",
                                       width=250, show="●")
        self.password_entry.grid(column=0, row=100, pady=(0,0))

        self.submit_button = CTkButton(self.frame, text="Create Account", image=signup_image,
                                       width=200, command=self.create_login)
        self.submit_button.grid(column=0, row=100, pady=(80,0))

        self.username_entry.bind("<Return>", lambda e: self.create_login())
        self.password_entry.bind("<Return>", lambda e: self.create_login())
    
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
                h.encrypt_signup_details(username_entered, password_entered)
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

class Account(CTk):
    def __init__(self, username):
        super().__init__()
        self.username = username

        self.title(self.username)
        self.geometry(c.ACCOUNT_GEOMETRY)
        
        if sys.platform.startswith("win"):
            self.iconbitmap(h.get_resource_path(c.WINDOW_ICON))
        else:
            pass
        
        self.menu = Menu(self)
        self.config(menu=self.menu)
        self.filemenu = Menu(self.menu, tearoff="off")

        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="⚙ Preferences", command=self.preferences, accelerator="Ctrl+Shift+P    ", hidemargin=True)

        self.frame = CTkScrollableFrame(self)
        self.frame.pack(fill="both", expand=True, pady=20, padx=20)
        self.frame.columnconfigure(0, weight=1)

        welcome = Notify()
        welcome.title = "Welcome!"
        welcome.message = f"Welcome {username}. Good to see you."
        welcome.icon = h.get_resource_path(c.NOTIFICATION_ICON)
        welcome.audio = h.get_resource_path(c.NOTIFICATION_SOUND_PATH)

        welcome.send()

        self.welcome_label = CTkLabel(self.frame, font=("", 20, "bold"),
                                      text=f"Welcome to your account, {username}.")
        self.welcome_label.grid(row=0, column=0, padx=10, pady=(10,0), sticky="w")

        self.web_search_entry = CTkEntry(self.frame, placeholder_text="Search web",
                                       width=400)
        self.web_search_entry.grid(row=1, column=0, padx=10, pady=(10,0), sticky="w")
        self.web_search_entry.bind("<Return>", lambda e: self.web_search())

        self.web_search_button = CTkButton(self.frame, text="", image=find_image,
                                           command=self.web_search, width=60)
        self.web_search_button.grid(row=1, column=0, padx=400, pady=(10,0), sticky="w")

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
        pass

def main():
    app = App()
    app.mainloop()