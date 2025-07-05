
import customtkinter as ctk

# Dynamically pass role to show respective dashboard
def open_dashboard(role):
    app = ctk.CTk()
    app.geometry("600x400")
    app.title(f"{role} Dashboard – The Enchanted Library")

    title = ctk.CTkLabel(app, text=f"Welcome {role}", font=ctk.CTkFont(size=24, weight="bold"))
    title.pack(pady=20)

    # Common for all
    ctk.CTkButton(app, text="🔍 Search Books", width=200).pack(pady=10)
    ctk.CTkButton(app, text="📘 View All Books", width=200).pack(pady=10)

    if role == "Scholar":
        ctk.CTkButton(app, text="📚 Borrow Book", width=200).pack(pady=10)
        ctk.CTkButton(app, text="↩️ Return Book", width=200).pack(pady=10)
        ctk.CTkButton(app, text="✨ Book Recommendations", width=200).pack(pady=10)

    elif role == "Librarian":
        ctk.CTkButton(app, text="➕ Add Book", width=200).pack(pady=10)
        ctk.CTkButton(app, text="🧾 Manage Users", width=200).pack(pady=10)
        ctk.CTkButton(app, text="🛠️ Restore Book", width=200).pack(pady=10)
        ctk.CTkButton(app, text="⚙️ System Logs", width=200).pack(pady=10)

    ctk.CTkButton(app, text="🚪 Logout", command=app.destroy, fg_color="red", width=100).pack(pady=20)

    app.mainloop()

# 🧪 For testing individually
if __name__ == "__main__":
    open_dashboard("Scholar")
