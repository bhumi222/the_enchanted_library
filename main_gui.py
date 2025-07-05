from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import mysql.connector
from datetime import datetime, timedelta
from fine_calculator import FineCalculator
from fine_summary import FineSummary
from tkinter import ttk
from factories import EnchantedLibraryFactory
from observers import LibraryNotifier, LibrarianObserver, GuestObserver
from strategies import AcademicLendingStrategy, PublicLendingStrategy, RestrictedLendingStrategy
from states import AvailableState, BorrowedState, ReservedState, RestorationState
import os
import sys

# Appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Dummy login users
#users = {
 #   "admin": "admin123",  "scholar": "scholar123",    "librarian": "lib123",    "guest": "guest123"
#}

# Dummy role mapping
#roles = {    "admin": "Admin",    "scholar": "Scholar",    "librarian": "Librarian",    "guest": "Guest"}

import customtkinter as ctk
from PIL import Image, ImageTk

class LoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Enchanted Library - Login")
        
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Store the PIL Image object as instance variable
        self.pil_image = None
        self.bg_image = None
        
        # Create and store the image reference
        try:
            self.pil_image = Image.open("background.png")
            self.bg_image = ctk.CTkImage(
                light_image=self.pil_image,
                dark_image=self.pil_image,
                size=(screen_width, screen_height)
            )
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.bg_image = None

        # Configure full screen and remove window decorations
        self.state('zoomed')
        self.attributes('-topmost', False)

        # Set window size to match screen
        self.geometry(f"{screen_width}x{screen_height}+0+0")

        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2)  # More weight for background
        self.grid_columnconfigure(1, weight=1)  # Less weight for login box
        
        # Create background frame
        self.bg_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.bg_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        # Create background label and set it to cover the full window
        if self.bg_image:
            self.bg_label = ctk.CTkLabel(self.bg_frame, image=self.bg_image, text="")
            self.bg_label.place(relwidth=1, relheight=1)  # Makes the background fill the window
        
        # Add this line to setup the login frame
        self.setup_login_frame()

    def setup_login_frame(self):
        # Create login frame with glass effect
        self.login_frame = ctk.CTkFrame(
            self,
            width=400,
            height=450,
            corner_radius=15,
            fg_color=("#FFFFFF", "#2B2B2B")  # Light mode: white, Dark mode: dark grey
        )
        self.login_frame.grid(row=0, column=1, padx=50, pady=50, sticky="e")
        self.login_frame.grid_propagate(False)
        
        # Center the content in login frame
        self.login_frame.grid_rowconfigure(0, weight=1)
        self.login_frame.grid_rowconfigure(6, weight=1)
        self.login_frame.grid_columnconfigure(0, weight=1)
        
        # Add decorative elements with enhanced visibility
        ctk.CTkLabel(
            self.login_frame,
            text="🏰",
            font=ctk.CTkFont(size=48),
            text_color=("#1A1A1A", "#FFFFFF")  # Dark text for light mode, white for dark mode
        ).grid(row=1, pady=(20, 0))
        
        ctk.CTkLabel(
                self.login_frame,
                text="Welcome to\nEnchanted Library",
                font=ctk.CTkFont(size=24, weight="bold"),
                justify="center",
                text_color=("black", "white")  # Ensure text visibility
        ).grid(row=2, pady=(10, 30))
            
        # Login inputs with enhanced styling and visibility
        self.username_entry = ctk.CTkEntry(
            self.login_frame,
            width=300,
            height=40,
            placeholder_text="Username",
            font=ctk.CTkFont(size=14),
            fg_color=("white", "#2B2B2B"),  # Solid colors for input fields
            border_color=("#2B2B2B", "white"),
            text_color=("black", "white")
        )
        self.username_entry.grid(row=3, padx=20, pady=10)
        
        self.password_entry = ctk.CTkEntry(
            self.login_frame,
            width=300,
            height=40,
            placeholder_text="Password",
            show="●",
            font=ctk.CTkFont(size=14),
            fg_color=("white", "#2B2B2B"),  # Solid colors for input fields
            border_color=("#2B2B2B", "white"),
            text_color=("black", "white")
        )
        self.password_entry.grid(row=4, padx=20, pady=10)
        
        # Login button with enhanced visibility
        login_button = ctk.CTkButton(
            self.login_frame,
            text="Enter Library",
            width=200,
            height=30,
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.login,
            fg_color="#2c3e50",
            hover_color="#34495e",
            text_color="white"
        )
        login_button.grid(row=5, pady=30)

        # Add Register button below login button
        register_button = ctk.CTkButton(
            self.login_frame,
            text="New User? Register",
            width=200,
            height=30,
            corner_radius=8,
            font=ctk.CTkFont(size=14),
            command=self.show_registration,
            fg_color="#34495e",
            hover_color="#2c3e50",
            text_color="white"
        )
        register_button.grid(row=6, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password!")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="enchanted_library"
            )
            cursor = connection.cursor()
            
            # Check if user exists and verify credentials
            cursor.execute("SELECT role, password, verified FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            
            if not result:
                messagebox.showerror("Login Failed", "User does not exist!")
                return
                
            stored_role, stored_password, verified = result
            
            if stored_password != password:
                messagebox.showerror("Login Failed", "Invalid password!")
                return
                
            if not verified and stored_role.lower() == "scholar":
                messagebox.showwarning("Account Not Verified", "Please wait for account verification.")
                return
            
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            
            # Create new window before destroying current one
            app = LibraryDashboard(username, stored_role)
            
            # Withdraw the current window instead of destroying it immediately
            self.withdraw()
            
            # Start the new window's main loop
            app.mainloop()
            
            # Only destroy after the new window is closed
            self.destroy()
            #messagebox.showinfo("Login Success", f"Welcome, {username}!\nRole: {stored_role}")
   
            cursor.close()
            connection.close()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def show_registration(self):
        # Clear login frame
        for widget in self.winfo_children():
            widget.destroy()

        # Create registration frame
        registration_frame = ctk.CTkFrame(
            self,
            width=400,
            height=550,
            corner_radius=15,
            fg_color=("#FFFFFF", "#2B2B2B")
        )
        registration_frame.grid(row=0, column=1, padx=50, pady=50, sticky="e")
        registration_frame.grid_propagate(False)

        # Title
        ctk.CTkLabel(
            registration_frame,
            text="Create Account",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("black", "white")
        ).grid(row=0, pady=20)

        # Registration fields
        fields = [
            ("Username", "username"),
            ("Email", "email"),
            ("Password", "password", True),
            ("Confirm Password", "confirm_password", True)
        ]

        self.reg_entries = {}
        for i, (label, key, *hide) in enumerate(fields, 1):
            ctk.CTkLabel(
                registration_frame,
                text=label,
                font=ctk.CTkFont(size=14)
            ).grid(row=i*2-1, pady=(10, 0))

            self.reg_entries[key] = ctk.CTkEntry(
                registration_frame,
                width=300,
                height=40,
                font=ctk.CTkFont(size=14),
                show="●" if hide else "",
                fg_color=("white", "#2B2B2B"),
                border_color=("#2B2B2B", "white")
            )
            self.reg_entries[key].grid(row=i*2, pady=(0, 10))

        # Role selection
        ctk.CTkLabel(
            registration_frame,
            text="Role",
            font=ctk.CTkFont(size=14)
        ).grid(row=9, pady=(10, 0))

        self.role_var = tk.StringVar(value="guest")
        roles_frame = ctk.CTkFrame(registration_frame, fg_color="transparent")
        roles_frame.grid(row=10, pady=10)

        # Only show Guest and Scholar options
        for i, role in enumerate(["Guest", "Scholar"]):
            ctk.CTkRadioButton(
                roles_frame,
                text=role,
                variable=self.role_var,
                value=role.lower(),
                font=ctk.CTkFont(size=14)
            ).grid(row=0, column=i, padx=20)

        # Register button
        ctk.CTkButton(
            registration_frame,
            text="Register",
            width=200,
            height=30,
            command=self.register_user,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2c3e50",
            hover_color="#34495e"
        ).grid(row=11, pady=20)

        # Back to login button
        ctk.CTkButton(
            registration_frame,
            text="Back to Login",
            width=200,
            height=40,
            command=self.__init__,
            font=ctk.CTkFont(size=14),
            fg_color="#90A4AE",
            hover_color="#78909C"
        ).grid(row=12, pady=10)

    def register_user(self):
        # Get registration data
        username = self.reg_entries["username"].get().strip()  # Add strip() to remove whitespace
        email = self.reg_entries["email"].get().strip()
        password = self.reg_entries["password"].get()
        confirm_password = self.reg_entries["confirm_password"].get()
        role = self.role_var.get()

        # Enhanced validation
        if not username:
            messagebox.showwarning("Input Error", "Username cannot be empty!")
            return

        if not email:
            messagebox.showwarning("Input Error", "Email cannot be empty!")
            return

        if not password or not confirm_password:
            messagebox.showwarning("Input Error", "Password fields cannot be empty!")
            return

        if password != confirm_password:
            messagebox.showwarning("Input Error", "Passwords do not match!")
            return

        # Ensure only Guest and Scholar roles can register
        if role.lower() not in ["guest", "scholar"]:
            messagebox.showwarning("Registration Error", "Invalid role selection!")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="enchanted_library"
            )
            cursor = connection.cursor()

            # Check if username exists
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showwarning("Registration Error", "Username already exists!")
                return

            # Set verified=True for Guest users, False for Scholar
            verified = role.lower() == "guest"
            
            # Add user to database with correct column names
            cursor.execute("""
                INSERT INTO users (username, email, password, role, verified)
                VALUES (%s, %s, %s, %s, %s)
            """, (username, email, password, role, verified))

            connection.commit()
            cursor.close()
            connection.close()

            if verified:
                messagebox.showinfo("Success", "Registration successful! You can now login.")
            else:
                messagebox.showinfo("Success", "Registration successful! Please wait for account verification.")
            self.__init__()  # Return to login page

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

class LibraryDashboard(ctk.CTk): 
    def __init__(self, user, role):
        super().__init__()
        self.user = user
        self.role = role.lower()
        
        # Initialize Factory
        self.library_factory = EnchantedLibraryFactory()
        
        # Initialize Notifier and Observers
        self.notifier = LibraryNotifier()
        
        # Create and attach appropriate observer based on role
        if self.role == "librarian":
            self.observer = LibrarianObserver(user)
        elif self.role == "guest":
            self.observer = GuestObserver(user)
        elif self.role == "admin":
            self.observer = LibrarianObserver(user)  # Admin gets librarian notifications
        elif self.role == "scholar":
            self.observer = GuestObserver(user)  # Scholar gets guest notifications
            
        self.notifier.attach(self.observer)
        
        # Initialize Lending Strategy based on role
        if self.role in ["admin", "librarian", "scholar"]:
            self.lending_strategy = AcademicLendingStrategy()
        elif self.role == "guest":
            self.lending_strategy = PublicLendingStrategy()
        else:
            self.lending_strategy = RestrictedLendingStrategy()
        
        # Configure window
        self.title(f"Enchanted Library - Welcome {user}")
        self.attributes('-topmost', False)
        self.state('zoomed')
        
        # Set window size to match screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")

        # Configure color scheme with better contrast
        self.configure(fg_color=("#FFFFFF", "#1E1E1E"))

        # Create main container frame
        self.main_container = ctk.CTkFrame(self, fg_color=("#F0F0F0", "#2D2D2D"))
        self.main_container.pack(fill="both", expand=True)
        
        # Create horizontal layout
        self.horizontal_layout = ctk.CTkFrame(self.main_container, fg_color=("#F0F0F0", "#2D2D2D"))
        self.horizontal_layout.pack(fill="both", expand=True)
        
        # Create sidebar frame with enhanced styling
        self.sidebar = ctk.CTkFrame(
            self.horizontal_layout,
            width=280,
            fg_color=("#E0E0E0", "#363636")
        )
        self.sidebar.pack(side="left", fill="y", padx=5)
        
        # Content area
        self.content_frame = ctk.CTkFrame(self.horizontal_layout,
            fg_color=("#FFFFFF", "#2D2D2D"))
        self.content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
       # Button styling with more contrast
        button_params = {
            "corner_radius": 10,
            "height": 25,
            "fg_color": ("#1a365d", "#2d4a77"),  # Lighter color for dark mode
            "hover_color": ("#2c5282", "#4a69a1"),  # Even lighter hover for dark mode
            "text_color": "white",
            "font": ctk.CTkFont(size=14, weight="bold")
        }
        
        # Logo and title with better contrast
        logo_label = ctk.CTkLabel(
            self.sidebar,
            text="🏰 Enchanted\nLibrary",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#2c3e50", "#FFFFFF")
        )
        logo_label.pack(pady=40)
        
        # User info section with better visibility
        user_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        user_frame.pack(fill="x", padx=25, pady=20)
        ctk.CTkLabel(
            user_frame,
            text=f"👤 {user}",
            font=("Helvetica", 16, "bold"),
            text_color=("#2c3e50", "#FFFFFF")
        ).pack()
        ctk.CTkLabel(
            user_frame,
            text=f"🎭 {role}",
            font=("Helvetica", 14),
            text_color=("#34495e", "#E0E0E0")
        ).pack() 
        
        # Add separator
        ctk.CTkFrame(self.sidebar, height=2, fg_color="#34495e").pack(fill="x", padx=20, pady=10)
        
        # Common buttons for all users
        common_buttons = [
            ("📚 View Books", self.show_books),
            ("🔍 Search Books", self.show_advanced_search),
            ("📖 Borrow Book", self.borrow_action),
            ("🔖 Reserve Book", self.reserve_action),
            ("↩️ Return Book", self.return_book_action),
            ("📋 Book Recommendations", self.show_recommendations)
        ]
        
        # Add common buttons
        for text, command in common_buttons:
            ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                **button_params
            ).pack(pady=5, padx=25, fill="x")
        
        # Add role-specific buttons
        if self.role in ["admin", "librarian"]:
            # Add separator for management section
            ctk.CTkFrame(self.sidebar, height=2, fg_color="#34495e").pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(
                self.sidebar,
                text="Management",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=("#2c3e50", "#ECF0F1")
            ).pack(pady=10)
            
            management_buttons = [
                ("➕ Add Books", self.show_add_book),
                ("❌ Remove Books", self.show_remove_book)
            ]
            
            for text, command in management_buttons:
                ctk.CTkButton(
                    self.sidebar,
                    text=text,
                    command=command,
                    **button_params
                ).pack(pady=5, padx=25, fill="x")
        
        # Admin-specific buttons
        if self.role == "admin":
            admin_buttons = [
                ("👥 Add Librarian", self.show_add_librarian),
                ("🗑️ Remove Librarian", self.show_remove_librarian)
            ]
            
            for text, command in admin_buttons:
                ctk.CTkButton(
                    self.sidebar,
                    text=text,
                    command=command,
                    **button_params
                ).pack(pady=5, padx=25, fill="x")
        
        # Add notifications button for all except guests
        if self.role != "guest":
            ctk.CTkButton(
                self.sidebar,
                text="🔔 Notifications",
                command=self.show_notifications,
                **button_params
            ).pack(pady=5, padx=25, fill="x")
        
        # Logout button for all users
        ctk.CTkButton(
            self.sidebar,
            text="🚪 Logout",
            command=self.logout,
            **button_params
        ).pack(pady=20, padx=25, fill="x")
        
        # Add welcome message to content area
        welcome_frame = ctk.CTkFrame(self.content_frame, fg_color=("#FFFFFF", "#2D2D2D"))
        welcome_frame.pack(pady=50, padx=30, fill="both", expand=True)
        
        ctk.CTkLabel(
            welcome_frame,
            text=f"Welcome to Enchanted Library, {user}!",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=("#2c3e50", "#FFFFFF")
        ).pack(pady=20)
        
        ctk.CTkLabel(
            welcome_frame,
            text="Select an option from the sidebar to get started",
            font=ctk.CTkFont(size=16),
            text_color=("#34495e", "#E0E0E0")
        ).pack()     
    
    def show_add_librarian(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Create form frame
        form_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        form_frame.pack(pady=50, padx=30)
        
        # Title
        ctk.CTkLabel(
            form_frame,
            text="Add New Librarian",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#2c3e50", "#FFFFFF")
        ).pack(pady=20)
        
        # Entry fields
        self.librarian_username = ctk.CTkEntry(
            form_frame,
            width=300,
            placeholder_text="Username",
            font=ctk.CTkFont(size=14)
        )
        self.librarian_username.pack(pady=10)
        
        self.librarian_password = ctk.CTkEntry(
            form_frame,
            width=300,
            placeholder_text="Password",
            show="●",
            font=ctk.CTkFont(size=14)
        )
        self.librarian_password.pack(pady=10)
        
        self.librarian_email = ctk.CTkEntry(
            form_frame,
            width=300,
            placeholder_text="Email",
            font=ctk.CTkFont(size=14)
        )
        self.librarian_email.pack(pady=10)
        
        # Add button
        ctk.CTkButton(
            form_frame,
            text="Add Librarian",
            command=self.add_librarian_action,
            width=200,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2c3e50",
            hover_color="#34495e"
        ).pack(pady=20)

    def add_librarian_action(self):
        username = self.librarian_username.get().strip()
        password = self.librarian_password.get()
        email = self.librarian_email.get().strip()
        
        if not all([username, password, email]):
            messagebox.showwarning("Input Error", "All fields are required!")
            return
            
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="enchanted_library"
            )
            cursor = connection.cursor()
            
            # Check if username exists
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showwarning("Error", "Username already exists!")
                return
            
            # Add librarian to database
            cursor.execute("""
                INSERT INTO users (username, email, password, role, verified)
                VALUES (%s, %s, %s, 'librarian', TRUE)
            """, (username, email, password))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            messagebox.showinfo("Success", "Librarian added successfully!")
            self.show_add_librarian()  # Reset form
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def show_remove_librarian(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Create form frame
        form_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        form_frame.pack(pady=50, padx=30)
        
        # Title
        ctk.CTkLabel(
            form_frame,
            text="Remove Librarian",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#2c3e50", "#FFFFFF")
        ).pack(pady=20)
        
        # Username entry
        self.remove_librarian_username = ctk.CTkEntry(
            form_frame,
            width=300,
            placeholder_text="Librarian Username",
            font=ctk.CTkFont(size=14)
        )
        self.remove_librarian_username.pack(pady=10)
        
        # Remove button
        ctk.CTkButton(
            form_frame,
            text="Remove Librarian",
            command=self.remove_librarian_action,
            width=200,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(pady=20)

    def remove_librarian_action(self):
        username = self.remove_librarian_username.get().strip()
        
        if not username:
            messagebox.showwarning("Input Error", "Please enter a username!")
            return
            
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="enchanted_library"
            )
            cursor = connection.cursor()
            
            # Check if librarian exists
            cursor.execute("SELECT role FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            
            if not result:
                messagebox.showwarning("Error", "User does not exist!")
                return
                
            if result[0].lower() != 'librarian':
                messagebox.showwarning("Error", "User is not a librarian!")
                return
            
            # Remove librarian
            cursor.execute("DELETE FROM users WHERE username = %s", (username,))
            connection.commit()
            
            cursor.close()
            connection.close()
            
            messagebox.showinfo("Success", "Librarian removed successfully!")
            self.show_remove_librarian()  # Reset form
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")



    def _on_frame_configure(self, event=None):
        self.sidebar_canvas.configure(scrollregion=self.sidebar_canvas.bbox("all"))


        
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_recommendations(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="📋 Book Recommendations", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # Create recommendations frame
        recommendations_frame = ctk.CTkFrame(self.content_frame)
        recommendations_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="enchanted_library"
            )
            cursor = connection.cursor()
            
            # Get user's borrowed books to base recommendations on
            cursor.execute("""
                SELECT DISTINCT b.book_type
                FROM books b
                JOIN borrow_records br ON b.book_id = br.book_id
                WHERE br.user_id = (SELECT user_id FROM users WHERE username = %s LIMIT 1)
                AND br.status = 'returned'
            """, (self.user,))
            
            user_preferences = cursor.fetchall()
            
            if user_preferences:
                # Get recommendations based on user's reading history
                book_types = tuple(pref[0] for pref in user_preferences)
                placeholders = ', '.join(['%s'] * len(book_types))
                
                cursor.execute(f"""
                    SELECT book_title, author, book_type, status
                    FROM books
                    WHERE book_type IN ({placeholders})
                    AND status = 'available'
                    LIMIT 10
                """, book_types)
            else:
                # If no history, show popular books
                cursor.execute("""
                    SELECT book_title, author, book_type, status
                    FROM books
                    WHERE status = 'available'
                    ORDER BY RAND()
                    LIMIT 10
                """)
            
            recommendations = cursor.fetchall()
            
            if recommendations:
                for i, book in enumerate(recommendations, 1):
                    book_frame = ctk.CTkFrame(recommendations_frame)
                    book_frame.pack(fill="x", padx=10, pady=5)
                    
                    ctk.CTkLabel(
                        book_frame,
                        text=f"📚 {book[0]}",
                        font=ctk.CTkFont(size=14, weight="bold")
                    ).pack(anchor="w", padx=10, pady=2)
                    
                    ctk.CTkLabel(
                        book_frame,
                        text=f"👤 {book[1]} | 📖 {book[2]} | 📍 {book[3]}"
                    ).pack(anchor="w", padx=10, pady=2)
            else:
                ctk.CTkLabel(
                    recommendations_frame,
                    text="No recommendations available at this time.",
                    font=ctk.CTkFont(size=14)
                ).pack(pady=20)
            
            cursor.close()
            connection.close()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    
    def show_books(self):
        self.clear_content()
        self.books_frame = ctk.CTkFrame(self.content_frame)
        self.books_frame.pack(pady=20)
        self.books_table = ttk.Treeview(self.books_frame, columns=("Book ID", "Title", "Author", "Status"), show="headings")
        self.books_table.heading("Book ID", text="Book ID")
        self.books_table.heading("Title", text="Title")
        self.books_table.heading("Author", text="Author")
        self.books_table.heading("Status", text="Status")
        self.books_table.pack()
        self.load_books()
    def load_books(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="library"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        for book in books:
            self.books_table.insert("", "end", values=book)
        conn.close()
    
    def show_dashboard(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="📊 Dashboard", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)

        # Add dashboard widgets
        stats_frame = ctk.CTkFrame(self.content_frame)
        stats_frame.pack(pady=20, padx=20, fill="x")

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="enchanted_library"
            )
            cursor = connection.cursor()

            # Get total books
            cursor.execute("SELECT COUNT(*) FROM books")
            total_books = cursor.fetchone()[0]

            # Get borrowed books
            cursor.execute("SELECT COUNT(*) FROM books WHERE status = 'Borrowed'")
            borrowed_books = cursor.fetchone()[0]

            # Get user's active borrows
            cursor.execute("""
                SELECT COUNT(*) FROM borrow_records 
                WHERE user_id = %s AND status = 'Borrowed'
            """, (self.user,))
            user_borrows = cursor.fetchone()[0]

            # Display stats
            ctk.CTkLabel(stats_frame, text=f"📚 Total Books: {total_books}").pack(pady=5)
            ctk.CTkLabel(stats_frame, text=f"📖 Currently Borrowed: {borrowed_books}").pack(pady=5)
            ctk.CTkLabel(stats_frame, text=f"🔖 Your Active Borrows: {user_borrows}").pack(pady=5)

            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def show_books(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="📚 Book List", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        list_frame = ctk.CTkFrame(self.content_frame)
        list_frame.pack(expand=True, fill="both", padx=10, pady=10)

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="enchanted_library"
            )
            cursor = connection.cursor()

            cursor.execute("""
                SELECT book_id, book_title, author, book_type, status, is_restricted 
                FROM books
            """)
            books = cursor.fetchall()

            # Treeview table
            columns = ("ID", "Title", "Author", "Type", "Status", "Restricted")
            tree = ttk.Treeview(list_frame, columns=columns, show="headings")
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=130)

            tree.pack(side="left", fill="both", expand=True)

            scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
            scrollbar.pack(side="right", fill="y")
            tree.config(yscrollcommand=scrollbar.set)

            for book in books:
                book_id, title, author, btype, status, restricted = book
                restricted_text = "Yes" if restricted else "No"
                tree.insert("", "end", values=(book_id, title, author, btype, status, restricted_text))

            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def show_advanced_search(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="🔍 Advanced Book Search", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        search_frame = ctk.CTkFrame(self.content_frame)
        search_frame.pack(pady=10)

        keyword_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter search keyword")
        keyword_entry.grid(row=0, column=0, padx=10)

        filter_var = tk.StringVar(value="book_title")
        filter_dropdown = ctk.CTkOptionMenu(search_frame, variable=filter_var, 
                                          values=["book_title", "author", "book_type", "status"])
        filter_dropdown.grid(row=0, column=1, padx=10)

        result_frame = ctk.CTkFrame(self.content_frame)
        result_frame.pack(pady=10, fill="both", expand=True)

        # Create Treeview for results
        columns = ("Title", "Author", "Type", "Status", "Restricted")
        tree = ttk.Treeview(result_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130)

        tree.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(result_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.config(yscrollcommand=scrollbar.set)

        def perform_search():
            keyword = keyword_entry.get().strip()
            filter_field = filter_var.get()

            if not keyword:
                messagebox.showwarning("Input Error", "Please enter a keyword.")
                return

            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="enchanted_library"
                )
                cursor = connection.cursor()

                query = f"""
                    SELECT book_title, author, book_type, status, is_restricted 
                    FROM books 
                    WHERE {filter_field} LIKE %s
                """
                cursor.execute(query, (f"%{keyword}%",))
                results = cursor.fetchall()

                # Clear previous results
                for item in tree.get_children():
                    tree.delete(item)

                if results:
                    for book in results:
                        title, author, btype, status, restricted = book
                        restricted_text = "Yes" if restricted else "No"
                        tree.insert("", "end", values=(title, author, btype, status, restricted_text))
                else:
                    messagebox.showinfo("No Results", "No books found matching your search.")

                cursor.close()
                connection.close()

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        ctk.CTkButton(search_frame, text="Search", command=perform_search).grid(row=0, column=2, padx=10)

    def return_book_action(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create return frame
        return_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        return_frame.pack(pady=50, padx=30)

        # Title
        ctk.CTkLabel(
            return_frame,
            text="Return a Book",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#2c3e50", "#FFFFFF")
        ).pack(pady=20)

        # Book title entry
        self.return_title_entry = ctk.CTkEntry(
            return_frame,
            width=300,
            placeholder_text="Enter Book Title",
            font=ctk.CTkFont(size=14)
        )
        self.return_title_entry.pack(pady=10)

        # Return button
        ctk.CTkButton(
            return_frame,
            text="Return",
            command=self.process_return,
            width=200,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2c3e50",
            hover_color="#34495e"
        ).pack(pady=20)

    def process_return(self):
        book_title = self.return_title_entry.get().strip()

        if not book_title:
            messagebox.showwarning("Input Error", "Please enter a book title!")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="enchanted_library"
            )
            cursor = connection.cursor()

            # Get user_id
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (self.user,))
            user_row = cursor.fetchone()
            if not user_row:
                messagebox.showerror("User Error", "User not found in database!")
                return
            user_id = user_row[0]

            # Check if this user has borrowed the book
            cursor.execute("""
                SELECT b.book_id, b.status
                FROM books b
                JOIN borrow_records br ON b.book_id = br.book_id
                WHERE b.book_title = %s AND br.user_id = %s AND br.status = 'borrowed'
            """, (book_title, user_id))

            book_row = cursor.fetchone()
            if not book_row:
                messagebox.showwarning("Not Borrowed", "Book not found or not borrowed by you!")
                return

            book_id, book_status = book_row

            # Mark borrow record as returned
            cursor.execute("""
                UPDATE borrow_records 
                SET status = 'returned', return_date = CURRENT_TIMESTAMP
                WHERE book_id = %s AND user_id = %s AND status = 'borrowed'
            """, (book_id, user_id))

            # Update book status
            cursor.execute("UPDATE books SET status = 'available' WHERE book_id = %s", (book_id,))

            connection.commit()
            messagebox.showinfo("Success", f"Successfully returned '{book_title}'")
            self.return_book_action()  # Refresh form

        except mysql.connector.Error as err:
            if connection:
                connection.rollback()
            messagebox.showerror("Database Error", f"MySQL Error: {err}")
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()

    def borrow_action(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="📚 Borrow a Book", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        borrow_frame = ctk.CTkFrame(self.content_frame)
        borrow_frame.pack(pady=20)

        title_entry = ctk.CTkEntry(borrow_frame, placeholder_text="Enter Book Title")
        title_entry.pack(pady=10)

        def process_borrow():
            title = title_entry.get().strip()
            if not title:
                messagebox.showwarning("Input Error", "Please enter a book title.")
                return

            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="enchanted_library"
                )
                cursor = connection.cursor()

                # Create user using Factory Pattern
                user_obj = self.library_factory.create_user(self.user, self.role)
                
                cursor.execute("""
                    SELECT book_id, book_type, status, is_restricted 
                    FROM books 
                    WHERE book_title = %s
                """, (title,))
                result = cursor.fetchone()

                if result:
                    book_id, book_type, status, is_restricted = result
                    
                    # Create book using Factory Pattern
                    book_obj = self.library_factory.create_book(title, "", book_type)
                    book_obj.status = status 
                    book_obj.is_restricted = is_restricted

                    # Check if user can borrow using Strategy Pattern
                    if self.lending_strategy.can_borrow(user_obj, book_obj):
                        if status == "Available":
                            # Update book status
                            cursor.execute("""
                                UPDATE books 
                                SET status = 'Borrowed' 
                                WHERE book_id = %s
                            """, (book_id,))

                            # Create borrow record
                            borrow_date = datetime.now()
                            due_date = borrow_date + timedelta(days=14)  # 2 weeks lending period
                            
                            cursor.execute("""
               INSERT INTO borrow_records 
                                (user_id, book_id, borrow_date, due_date, status) 
                                VALUES (%s, %s, %s, %s, 'Borrowed')
                            """, (self.user, book_id, borrow_date, due_date))

                            cursor.execute("""
                UPDATE books 
                SET status = 'borrowed'
                WHERE book_id = %s
            """, (book_id,))

                            connection.commit()
                            messagebox.showinfo("Success", f"Book '{title}' has been borrowed successfully!\nDue date: {due_date.strftime('%Y-%m-%d')}")

                            # Notify librarian
                            self.notifier.notify(f"Book '{title}' has been borrowed by {self.user}")
                        else:
                            messagebox.showwarning("Not Available", f"Book '{title}' is currently {status.lower()}.")
                    else:
                        messagebox.showwarning("Not Allowed", "You are not allowed to borrow this book.")
                else:
                    messagebox.showwarning("Not Found", f"Book '{title}' not found.")

                cursor.close()
                connection.close()

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        ctk.CTkButton(borrow_frame, text="Borrow", command=process_borrow).pack(pady=10)


      
    def show_notifications(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="🔔 Notifications", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        list_frame = ctk.CTkFrame(self.content_frame)
        list_frame.pack(expand=True, fill="both", padx=10, pady=10)

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="enchanted_library"
            )
            cursor = connection.cursor()

            # Modified query to only check username
            cursor.execute("""
                SELECT message, created_at 
                FROM notifications 
                WHERE username = %s 
                ORDER BY created_at DESC
            """, (self.user,))
            
            notifications = cursor.fetchall()

            text_box = tk.Text(list_frame, height=15, width=80, wrap="word")
            text_box.pack(side="left", fill="both", expand=True)

            scrollbar_y = tk.Scrollbar(list_frame, orient="vertical", command=text_box.yview)
            scrollbar_y.pack(side="right", fill="y")
            text_box.config(yscrollcommand=scrollbar_y.set)

            if notifications:
                for msg, time in notifications:
                    time_str = time.strftime('%Y-%m-%d %H:%M:%S') if time else "N/A"
                    text_box.insert("end", f"📢 {msg}\n🕒 {time_str}\n\n")
            else:
                text_box.insert("end", "📭 No notifications yet.")

            text_box.config(state="disabled")  # Make text box read-only
            
            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"❌ Failed to load notifications.\n{err}")

    
    def show_add_book(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="➕ Add New Book", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        # Create entry fields
        title_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Book Title")
        author_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Author")
        
        # Book Type Dropdown
        book_types = ["GeneralBook", "RareBook", "AncientScript", "ReferenceBook", "TextBook"]
        type_var = ctk.StringVar(value=book_types[0])
        type_dropdown = ctk.CTkOptionMenu(self.content_frame, 
                                        variable=type_var,
                                        values=book_types)
        
        # Book Condition Dropdown
        conditions = ["New", "Good", "Fair", "Poor", "Needs Restoration"]
        condition_var = ctk.StringVar(value=conditions[0])
        condition_dropdown = ctk.CTkOptionMenu(self.content_frame, 
                                            variable=condition_var,
                                            values=conditions)
        
        restricted_var = ctk.BooleanVar()
        restricted_switch = ctk.CTkSwitch(self.content_frame, text="Restricted", variable=restricted_var)

        # Pack all fields
        title_entry.pack(pady=5)
        author_entry.pack(pady=5)
        type_dropdown.pack(pady=5)
        condition_dropdown.pack(pady=5)
        restricted_switch.pack(pady=5)

        def add_to_db():
            book_title = title_entry.get().strip()
            author = author_entry.get().strip()
            book_type = type_var.get()
            condition = condition_var.get()
            is_restricted = restricted_var.get()

            if not all([book_title, author]):
                messagebox.showwarning("Missing Info", "Please fill all fields.")
                return

            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="enchanted_library"
                )
                cursor = connection.cursor()

                cursor.execute("""
                    INSERT INTO books (book_title, author, book_type, status, `condition`, is_restricted)
                    VALUES (%s, %s, %s, 'available', %s, %s)
                """, (book_title, author, book_type, condition, is_restricted))
                connection.commit()

                # Use Observer Pattern for notification
                self.notifier.send_notification(f"New book '{book_title}' added by {self.user}")

                messagebox.showinfo("Success", f"📚 Book '{book_title}' added!")
                
                # Clear the entries after successful addition
                title_entry.delete(0, 'end')
                author_entry.delete(0, 'end')
                type_var.set(book_types[0])
                condition_var.set(conditions[0])
                restricted_var.set(False)
                
                connection.close()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"DB Error: {err}")

        # Add the "Add Book" button
        ctk.CTkButton(self.content_frame, text="Add Book", command=add_to_db).pack(pady=20)

    def reserve_action(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="📖 Reserve a Book", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        reserve_frame = ctk.CTkFrame(self.content_frame)
        reserve_frame.pack(pady=20)

        title_entry = ctk.CTkEntry(reserve_frame, placeholder_text="Enter Book Title")
        title_entry.pack(pady=10)

        def process_reserve():
            title = title_entry.get().strip()
            if not title:
                messagebox.showwarning("Input Error", "Please enter a book title.")
                return

            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="enchanted_library"
                )
                cursor = connection.cursor()

                # Create user using Factory Pattern
                user_obj = self.library_factory.create_user(self.user, self.role)
                
                cursor.execute("""
                    SELECT book_id, book_type, status, is_restricted 
                    FROM books 
                    WHERE book_title = %s
                """, (title,))
                result = cursor.fetchone()

                if result:
                    book_id, book_type, status, is_restricted = result
                    
                    # Create book using Factory Pattern
                    book_obj = self.library_factory.create_book(title, "", book_type)
                    book_obj.status = status
                    book_obj.is_restricted = is_restricted

                    # Check if user can reserve using Strategy Pattern
                    if not self.lending_strategy.can_borrow(user_obj, book_obj):
                        messagebox.showwarning("Access Denied", "⚠️ You don't have permission to reserve this book.")
                        return

                    # Use State Pattern to handle reservation
                    if status.lower() == "available":
                        book_obj.state = AvailableState()
                        if book_obj.state.reserve(book_obj):
                            reserved_at = datetime.now()
                            
                            cursor.execute("UPDATE books SET status = 'Reserved' WHERE book_id = %s", (book_id,))
                            cursor.execute("""
                                INSERT INTO reservations 
                                (user_id, book_id, reserved_at, status) 
                                VALUES (%s, %s, %s, 'Reserved')
                            """, (user_obj.id, book_id, reserved_at))

                            # Use Observer Pattern for notification
                            self.notifier.send_notification(f"Book '{title}' has been reserved by {self.user}")

                            connection.commit()
                            messagebox.showinfo("Success", f"📖 Book '{title}' has been reserved!")
                    else:
                        messagebox.showinfo("Unavailable", f"⚠️ Book '{title}' is currently {status.lower()}.")
                else:
                    messagebox.showerror("Not Found", "❌ Book not found in the library.")

                cursor.close()
                connection.close()

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        ctk.CTkButton(reserve_frame, text="Reserve", command=process_reserve).pack(pady=10)
    def show_remove_book(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="❌ Remove Book", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        remove_frame = ctk.CTkFrame(self.content_frame)
        remove_frame.pack(pady=20)

        # Create entry field
        title_entry = ctk.CTkEntry(remove_frame, placeholder_text="Enter Book Title")
        title_entry.pack(pady=10)

        def remove_book():
            title = title_entry.get().strip()
            if not title:
                messagebox.showwarning("Input Error", "Please enter a book title.")
                return

            if messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove '{title}'?"):
                try:
                    connection = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="enchanted_library"
                    )
                    cursor = connection.cursor()

                    cursor.execute("SELECT book_id FROM books WHERE book_title = %s", (title,))
                    result = cursor.fetchone()

                    if result:
                        book_id = result[0]
                        cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
                        
                        # Use Observer Pattern for notification
                        self.notifier.send_notification(f"Book '{title}' has been removed by {self.user}")
                        
                        connection.commit()
                        messagebox.showinfo("Success", f"📚 Book '{title}' has been removed!")
                        title_entry.delete(0, 'end')  # Clear the entry field
                    else:
                        messagebox.showerror("Error", "Book not found!")

                    cursor.close()
                    connection.close()

                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")

        # Add the Remove Book button
        ctk.CTkButton(remove_frame, text="Remove Book", command=remove_book).pack(pady=10)

    def logout(self):
        # Clean up any resources
        if hasattr(self, 'notifier'):
           self.notifier = None
        if hasattr(self, 'observer'):
           self.observer = None
        if hasattr(self, 'lending_strategy'):
           self.lending_strategy = None
        self.destroy()   
        # Create new login window
        new_login = LoginPage()
        
        # Position the new window
        new_login.state('zoomed')
        #new_login.update()  # Ensure window is updated before showing
        
        # Destroy current window
       
        #os.execl(sys.executable, sys.executable, *sys.argv)  # Full app restart
        # Show new login window
        #new_login.deiconify()
        new_login.mainloop()

if __name__ == "__main__":
    app = LoginPage()
    app.mainloop()
