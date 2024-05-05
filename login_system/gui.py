from customtkinter import (CTk, CTkToplevel, CTkLabel, CTkEntry, CTkButton,
                           CTkOptionMenu, CTkImage, END, CTkFrame, set_appearance_mode,
                           set_default_color_theme)
from PIL import Image, ImageTk
from notifypy import Notify

from tkinter import Toplevel, messagebox

import login_system.helpers as h
import login_system.constants as c

set_appearance_mode("light")
set_default_color_theme(c.DEFAULT_THEME)

class App(CTk):
    def __init__(self):
        super().__init__()
        get_pillow_image = lambda relative_path: Image.open(h.get_resource_path(relative_path))
        
        self.signin_image = CTkImage(light_image=get_pillow_image(c.SIGNIN_IMAGE_PATH),
                      dark_image=get_pillow_image(c.SIGNIN_IMAGE_PATH))
        self.signup_image = CTkImage(light_image=get_pillow_image(c.SIGNUP_IMAGE_PATH),
                      dark_image=get_pillow_image(c.SIGNUP_IMAGE_PATH))

        self.title(c.MAIN_TITLE)
        self.geometry(c.MAIN_GEOMETRY)
        self.iconbitmap(h.get_resource_path(c.WINDOW_ICON))

        self.frame = CTkFrame(self)
        self.frame.grid(column=0, row=0, sticky="nsew")
        self.frame.columnconfigure(0, weight=1)

        self.bg_pil = Image.open(c.BACKGROUND)

        self.bg_photo = CTkLabel(self.frame, text="")
        self.bg_photo.grid(column=0, row=0, sticky="nsew", rowspan=200)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.username_entry= CTkEntry(self.frame, placeholder_text="Enter username",
                                      width=250, corner_radius=0)
        self.username_entry.grid(column=0, row=100, pady=(0,120))

        self.password_entry = CTkEntry(self.frame, placeholder_text="Enter password",
                                       width=250, corner_radius=0, show="●")
        self.password_entry.grid(column=0, row=100, pady=(0,50))

        self.submit_button = CTkButton(self.frame, text="Sign In", image=self.signin_image,
                                       width=200, command=self.submit, corner_radius=0)
        self.submit_button.grid(column=0, row=100, pady=(40,0))

        self.signup_button = CTkButton(self.frame, text="Sign Up", image=self.signup_image,
                                       width=200, command=self.signup_function, corner_radius=0)
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
                    self.withdraw()
                    self.quit()
                    account = Account(username_entered)
                    account.mainloop()
                    self.destroy()
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

        self.after(75, self.resize_image)

class Signup(Toplevel):
    def __init__(self):
        super().__init__()
        get_pillow_image = lambda relative_path: Image.open(h.get_resource_path(relative_path))
        self.signup_image = CTkImage(light_image=get_pillow_image(c.SIGNUP_IMAGE_PATH),
                      dark_image=get_pillow_image(c.SIGNUP_IMAGE_PATH))
        
        self.title(c.SIGNUP_TITLE)
        self.geometry(c.SIGNUP_GEOMETRY)
        self.iconbitmap(h.get_resource_path(c.WINDOW_ICON))

        self.frame = CTkFrame(self, fg_color="#000e20", corner_radius=0)
        self.frame.pack(fill="both", expand=True)
        self.frame.columnconfigure(0, weight=1)

        self.username_entry= CTkEntry(self.frame, placeholder_text="Enter username",
                                      width=250, corner_radius=0)
        self.username_entry.grid(column=0, row=100, pady=(0,70))

        self.password_entry = CTkEntry(self.frame, placeholder_text="Enter password",
                                       width=250, corner_radius=0, show="●")
        self.password_entry.grid(column=0, row=100, pady=(0,0))

        self.submit_button = CTkButton(self.frame, text="Create Account", image=self.signup_image,
                                       width=200, command=self.create_login, corner_radius=0)
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
        self.iconbitmap(h.get_resource_path(c.WINDOW_ICON))

        self.frame = CTkFrame(self)
        self.frame.pack(fill="both", expand=True, pady=20, padx=20)
        self.frame.columnconfigure(0, weight=1)

        welcome = Notify()
        welcome.title = "Welcome!"
        welcome.message = f"Welcome {username}. Good to see you."
        welcome.icon = h.get_resource_path(c.NOTIFICATION_ICON)
        welcome.audio = h.get_resource_path(c.NOTIFICATION_SOUND_PATH)

        welcome.send()

        self.welcome_label = CTkLabel(self.frame, 
                                      text=f"Welcome to your account, {username}.", )
        self.welcome_label.grid(row=0, column=0, padx=10, pady=(10,0), sticky="w")
        
def main():
    app = App()
    app.mainloop()