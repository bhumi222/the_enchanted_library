# gui_login.py
import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")  # or "dark"
ctk.set_default_color_theme("blue")  # Try: "dark-blue", "green"

def login():
    username = username_entry.get()
    password = password_entry.get()
    role = role_var.get()

    if username == "scholar" and password == "1234" and role == "Scholar":
        messagebox.showinfo("Success", "Login Successful as Scholar")
    elif username == "guest" and password == "0000" and role == "Guest":
        messagebox.showinfo("Success", "Login Successful as Guest")
    else:
        messagebox.showerror("Error", "Invalid credentials or role mismatch!")

# App window
app = ctk.CTk()
app.geometry("420x400")
app.title("The Enchanted Library – Login")

title = ctk.CTkLabel(app, text="📚 The Enchanted Library", font=ctk.CTkFont(size=22, weight="bold"))
title.pack(pady=20)

username_entry = ctk.CTkEntry(app, placeholder_text="Username")
username_entry.pack(pady=10)

password_entry = ctk.CTkEntry(app, placeholder_text="Password", show="*")
password_entry.pack(pady=10)

role_var = ctk.StringVar()
role_dropdown = ctk.CTkComboBox(app, variable=role_var, values=["Guest", "Scholar", "Librarian"])
role_dropdown.set("Select Role")
role_dropdown.pack(pady=10)

login_button = ctk.CTkButton(app, text="Login", command=login)
login_button.pack(pady=20)

app.mainloop()
