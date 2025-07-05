📚 The Enchanted Library An intelligent and secure book management system built with Python, CustomTkinter, and MySQL. Designed for academic and library environments with role-based access, fine management, notifications, and smart recommendations — all wrapped in a magical, fantasy-inspired theme.

🔮 Project Theme

In a mystical realm where knowledge is power, this system manages ancient tomes and general books using modern technology. Scholars, librarians, and guests interact through a dynamic GUI to protect and manage rare resources.

🚀 Features

🔐 Role-Based Access: Admin, Scholar, Librarian, Guest — each with specific permissions.
📚 Book Operations: Reserve, Borrow, Return books with live status updates.
💰 Fine Calculation: Automated based on user role and delay (Strategy Pattern).
🔔 Notification System: Observer pattern alerts for borrow/return/reserve actions.
📊 Admin Panel: Book statistics, overdue monitoring (future scope).
🤖 Smart Recommendations: Based on borrowing history (bonus feature).
🧾 Secure Transactions: All actions logged with timestamps in MySQL.
🧱 Technologies Used

Python (OOP)
CustomTkinter – for the GUI
MySQL + phpMyAdmin – for database
GitHub – version control & collaboration
🧠 Design Patterns Used

🏭 Factory Pattern – Create user objects dynamically
🧩 Facade Pattern – Abstract complex logic into simplified UI calls
👁 Observer Pattern – Real-time user notifications
📐 Strategy Pattern – Role-specific fine calculation
♻ Singleton Pattern – Centralized DB connection
🗂 Database

All tables are created and defined in the database.sql file included in this repo.

Tables:

users
books
borrow_records
reservations
notifications
returns
📦 How to Run

Clone or download the repo
Import database.sql into MySQL via phpMyAdmin
Install Python dependencies (like customtkinter, mysql.connector)
Run main_gui.py to launch the application
🧭 Future Scope

🔑 Secure login/registration with password encryption
📱 Mobile version (using Django or Flask + React)
📊 Real-time analytics dashboard for admins
🤖 ML-powered smart recommendations
📎 License

This project is open-source and available under the MIT License.
