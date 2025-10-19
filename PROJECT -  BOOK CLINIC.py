import tkinter as tk
from tkinter import messagebox, ttk, font
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import json
import os
from datetime import datetime

users = {}
USERS_FILE = "booking_data/users.txt"
BOOKINGS_FILE = "booking_data/bookings.txt"
FORGOT_PASSWORD_FILE = "booking_data/forgot_password.txt"
CANCELLATIONS_FILE = "booking_data/cancellations.txt"

services = {    
    "Dental Cleaning": 1000,
    "Physical Therapy": 1500,
    "Eye Check-up": 1000
}

MAIN_BG = "#00B7FF"
CARD_BG = "#FFFFFF"
ACCENT = "#FF0000"
BUTTON_COLOR = "#FF8BA7"
TEXT_COLOR = "#4A4A4A"


def load_users():
    """Load users from users.txt file."""
    global users
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        user_data = json.loads(line)
                        users[user_data['username']] = user_data['password']
        except Exception as e:
            print(f"Error loading users: {e}")


def save_user(username, password):
    """Save a new user to users.txt file."""
    os.makedirs("booking_data", exist_ok=True)
    try:
        user_data = {
            "username": username,
            "password": password,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(USERS_FILE, 'a') as f:
            f.write(json.dumps(user_data) + '\n')
    except Exception as e:
        print(f"Error saving user: {e}")


def save_booking(patient_name, appointment_date, services_list, total_amount):
    """Save booking record to bookings.txt file."""
    os.makedirs("booking_data", exist_ok=True)
    try:
        booking_data = {
            "booking_id": f"BK-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "patient_name": patient_name,
            "appointment_date": appointment_date,
            "services": services_list,
            "total_amount": total_amount,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "confirmed"
        }
        with open(BOOKINGS_FILE, 'a') as f:
            f.write(json.dumps(booking_data) + '\n')
    except Exception as e:
        print(f"Error saving booking: {e}")


def load_bookings_for_user(username):
    """Load all bookings for a specific user from bookings.txt file."""
    bookings = []
    if os.path.exists(BOOKINGS_FILE):
        try:
            with open(BOOKINGS_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        booking_data = json.loads(line)
                        if booking_data['patient_name'] == username:
                            bookings.append(booking_data)
        except Exception as e:
            print(f"Error loading bookings: {e}")
    return bookings


def save_forgot_password_record(username, new_password):
    """Save forgot password reset record to forgot_password.txt file."""
    os.makedirs("booking_data", exist_ok=True)
    try:
        reset_record = {
            "reset_id": f"RST-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "username": username,
            "reset_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "completed"
        }
        with open(FORGOT_PASSWORD_FILE, 'a') as f:
            f.write(json.dumps(reset_record) + '\n')
    except Exception as e:
        print(f"Error saving forgot password record: {e}")


def load_forgot_password_history(username):
    """Load password reset history for a specific user."""
    history = []
    if os.path.exists(FORGOT_PASSWORD_FILE):
        try:
            with open(FORGOT_PASSWORD_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        record = json.loads(line)
                        if record['username'] == username:
                            history.append(record)
        except Exception as e:
            print(f"Error loading forgot password history: {e}")
    return history


def save_cancellation_record(patient_name, booking_id, appointment_date, services_list, total_amount, reason=""):
    """Save booking cancellation record to cancellations.txt file."""
    os.makedirs("booking_data", exist_ok=True)
    try:
        cancellation_data = {
            "cancellation_id": f"CAN-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "booking_id": booking_id,
            "patient_name": patient_name,
            "appointment_date": appointment_date,
            "services": services_list,
            "total_amount": total_amount,
            "cancellation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reason": reason,
            "status": "cancelled"
        }
        with open(CANCELLATIONS_FILE, 'a') as f:
            f.write(json.dumps(cancellation_data) + '\n')
    except Exception as e:
        print(f"Error saving cancellation record: {e}")


def load_cancellations_for_user(username):
    """Load all cancellation records for a specific user."""
    cancellations = []
    if os.path.exists(CANCELLATIONS_FILE):
        try:
            with open(CANCELLATIONS_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        cancellation = json.loads(line)
                        if cancellation['patient_name'] == username:
                            cancellations.append(cancellation)
        except Exception as e:
            print(f"Error loading cancellations: {e}")
    return cancellations


class ClinicBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clinic Booking System")
        
        self.root.state('zoomed')
        self.root.configure(bg=MAIN_BG)
        self.current_user = None
        self.cart = {}
        self.product_images = {}

        load_users()
        
        available = font.families()
        if "Poppins" in available:
            self.font_regular = ("Poppins", 11)
            self.font_bold = ("Poppins", 12, "bold")
            self.header_font = ("Poppins", 24, "bold")
        else:
            fallback = "Arial"
            self.font_regular = (fallback, 11)
            self.font_bold = (fallback, 12, "bold")
            self.header_font = (fallback, 24, "bold")

            
        self.selected_date = tk.StringVar()

        self.create_welcome_page()
# try lang lods
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def set_background_image(self, image_file="dental.jpeg"):
        """Set background image for the page."""
        try:
            bg_img = Image.open(image_file)
            
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            
            
            if window_width <= 1:
                window_width = 1600
            if window_height <= 1:
                window_height = 900
            
          
            bg_img = bg_img.resize((window_width, window_height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_img)
            bg_label = tk.Label(self.root, image=self.bg_photo)
            bg_label.image = self.bg_photo  
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            pass

    def create_welcome_page(self):
        """Display welcome/landing page with Get Started button."""
        self.clear_window()
        self.root.configure(bg="#0B8FA3")
        self.set_background_image("background of the GUI log in page.jpeg")

        
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        if window_width <= 1:
            window_width = 1600
        if window_height <= 1:
            window_height = 900

        
        main_container = tk.Frame(self.root, bg="white", relief="flat", bd=0, highlightbackground="#0B8FA3", highlightthickness=2)
        main_container.place(relx=0.5, rely=0.5, anchor="center", width=int(window_width * 0.8), height=int(window_height * 0.7))

        
        left_panel = tk.Frame(main_container, bg="white")
        left_panel.pack(side="left", fill="both", expand=True, padx=30, pady=40)

        
        content_frame = left_panel

        
        tk.Label(content_frame, text="🏥 OUR CLINIC", font=("Arial", 24, "bold"), 
                bg="white", fg="#0B8FA3").pack(pady=(0, 10))
        
        
        tk.Label(content_frame, text="TREATS ALL", font=("Arial", 32, "bold"), 
                bg="white", fg="#0B8FA3").pack(pady=(0, 20))

        
        tk.Label(content_frame, text="Your Health, One Click Away", font=("Arial", 14), 
                bg="white", fg="#666").pack(pad y=(0, 30))

        
        features = ["✓ Easy Appointment Booking", "✓ Multiple Services", "✓ Secure & Reliable", "✓ 24/7 Support"]
        for feature in features:
            tk.Label(content_frame, text=feature, font=("Arial", 11), 
                    bg="white", fg="#333").pack(anchor="w", pady=5)

        
        tk.Label(content_frame, text="", bg="white").pack(pady=20)

        
        get_started_btn = tk.Button(content_frame, text="Get Started", command=self.create_login_page,
                                   bg="#0B8FA3", fg="white", font=("Arial", 14, "bold"),
                                   border=0, relief="flat", cursor="hand2", padx=40, pady=15,
                                   activebackground="#087A8F", activeforeground="white")
        get_started_btn.pack(fill="x", ipady=5)
        
        
        def on_enter(e):
            get_started_btn.config(bg="#087A8F")
        def on_leave(e):
            get_started_btn.config(bg="#0B8FA3")
        get_started_btn.bind("<Enter>", on_enter)
        get_started_btn.bind("<Leave>", on_leave)

        
        right_panel = tk.Frame(main_container, bg="white")
        right_panel.pack(side="right", fill="both", expand=False, padx=20, pady=20)

        
        images_container = tk.Frame(right_panel, bg="white")
        images_container.pack()

        
        try:
            doctor_img = Image.open("MAIN DOCTOR.png")
            
            self.doctor_photo = ImageTk.PhotoImage(doctor_img)
            doctor_label = tk.Label(images_container, image=self.doctor_photo, bg="white")
            doctor_label.pack(side="left", padx=10, pady=10)
        except Exception:
            tk.Label(images_container, text="👨‍⚕️\nMAIN DOCTOR", font=("Arial", 16, "bold"), 
                    bg="white", fg="#0B8FA3", justify="center").pack(side="left", padx=10, pady=10)

        
        try:
            book_img = Image.open("booking book.jpg")
            
            self.book_photo = ImageTk.PhotoImage(book_img)
            book_label = tk.Label(images_container, image=self.book_photo, bg="white")
            book_label.pack(side="left", padx=10, pady=10)
        except Exception:
            tk.Label(images_container, text="📖\nBOOKING BOOK", font=("Arial", 16, "bold"), 
                    bg="white", fg="#0B8FA3", justify="center").pack(side="left", padx=10, pady=10)

        
        footer_frame = tk.Frame(self.root, bg="#0B8FA3", height=40)
        footer_frame.pack(side="bottom", fill="x")
        
        footer_content = tk.Frame(footer_frame, bg="#0B8FA3")
        footer_content.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(footer_content, text="© 2025 Clinic Booking System. All rights reserved.", 
                font=("Arial", 9), bg="#0B8FA3", fg="white").pack(side="left")
        tk.Label(footer_content, text="Developed by: Yul, Dwayne, James, Zaiver", 
                font=("Arial", 9), bg="#0B8FA3", fg="white").pack(side="right")

    def create_login_page(self):
        self.clear_window() 
        self.root.configure(bg="#E8E8E8")

        
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        
        if window_width <= 1:
            window_width = 1600
        if window_height <= 1:
            window_height = 900
        
        
        container_width = int(window_width * 0.95)
        container_height = int(window_height * 0.95)

        
        container = tk.Frame(self.root, bg="white", relief="flat", bd=0)
        container.place(relx=0.5, rely=0.5, anchor="center", width=container_width, height=container_height)

        
        left_panel = tk.Frame(container, bg="white")
        left_panel.pack(side="left", fill="both", expand=True)

        
        header_bar = tk.Frame(left_panel, bg="#0B8FA3", height=50)
        header_bar.pack(fill="x")

        
        tk.Label(left_panel, text="Your Health, One Click Away", font=("Arial", 20, "bold"), 
                bg="white", fg="#0B8FA3").pack(pady=(25, 5))
        tk.Label(left_panel, text="Clinic Booking System", font=("Arial", 11), 
                bg="white", fg="#999").pack(pady=(0, 25))

        
        tk.Label(left_panel, text="Username", bg="white", font=("Arial", 11), 
                fg="#333").pack(anchor="w", padx=40, pady=(10, 3))
        username_frame = tk.Frame(left_panel, bg="white", highlightbackground="#E0E0E0", 
                               highlightthickness=1, relief="flat")
        username_frame.pack(padx=40, pady=(0, 15), fill="x")
        self.login_username = tk.Entry(username_frame, width=35, font=("Arial", 12), 
                                       border=0, bg="white")
        self.login_username.pack(padx=12, pady=10)

        
        tk.Label(left_panel, text="Password", bg="white", font=("Arial", 11), 
                fg="#333").pack(anchor="w", padx=40, pady=(10, 3))
        password_frame = tk.Frame(left_panel, bg="white", highlightbackground="#E0E0E0", 
                                 highlightthickness=1, relief="flat")
        password_frame.pack(padx=40, pady=(0, 15), fill="x")
        self.login_password = tk.Entry(password_frame, show="•", width=35, font=("Arial", 12), 
                                       border=0, bg="white")
        self.login_password.pack(padx=12, pady=10)

        
        options_frame = tk.Frame(left_panel, bg="white")
        options_frame.pack(padx=40, pady=(0, 20), fill="x")
        tk.Label(options_frame, text="Remember me", bg="white", font=("Arial", 10), 
                fg="#333").pack(side="left")
        forgot_link = tk.Label(options_frame, text="Forgot Password?", bg="white", font=("Arial", 10), 
                fg="#0099CC", cursor="hand2")
        forgot_link.pack(side="right")
        forgot_link.bind("<Button-1>", lambda e: self.forgot_password())

        
        login_btn = tk.Button(left_panel, text="Login", command=self.login, 
                             bg="#0B8FA3", fg="white", font=("Arial", 13, "bold"), 
                             border=0, relief="flat", cursor="hand2", padx=20, pady=12)
        login_btn.pack(pady=15, padx=40, fill="x")
        
        
        def on_enter(e):
            login_btn.config(bg="#087A8F")
        def on_leave(e):
            login_btn.config(bg="#0B8FA3")
        login_btn.bind("<Enter>", on_enter)
        login_btn.bind("<Leave>", on_leave)

        
        create_link = tk.Label(left_panel, text="Create Account", bg="white", font=("Arial", 11), 
                              fg="#333", cursor="hand2")
        create_link.pack(pady=20)
        create_link.bind("<Button-1>", lambda e: self.create_register_page())

        
        divider = tk.Frame(container, bg="#E0E0E0", width=2)
        divider.pack(side="left", fill="y")

        
        right_panel = tk.Frame(container, bg="#B8E6F0")
        right_panel.pack(side="right", fill="both", expand=True)

        
        try:
            anime_img = Image.open("log in anime doctor.png")
            
            anime_img = anime_img.resize((int(container_width * 0.4), int(container_height * 0.8)), Image.LANCZOS)
            self.anime_photo = ImageTk.PhotoImage(anime_img)
            anime_label = tk.Label(right_panel, image=self.anime_photo, bg="#B8E6F0")
            anime_label.pack(expand=True, padx=20, pady=20)
        except Exception:
            tk.Label(right_panel, text="🏥\nAnime Doctor\nImage", font=("Arial", 16, "bold"), 
                    bg="#B8E6F0", fg="#0B8FA3", justify="center").pack(expand=True)

        
        footer_frame = tk.Frame(self.root, bg="#0B8FA3", height=40)
        footer_frame.pack(side="bottom", fill="x")
        
        footer_content = tk.Frame(footer_frame, bg="#0B8FA3")
        footer_content.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(footer_content, text="© 2025 Clinic Booking System. All rights reserved.", 
                font=("Arial", 9), bg="#0B8FA3", fg="white").pack(side="left")
        tk.Label(footer_content, text="Developed by: Yul, Dwayne, James, Zaiver", 
                font=("Arial", 9), bg="#0B8FA3", fg="white").pack(side="right")

    def create_register_page(self):
        self.clear_window()
        self.root.configure(bg=MAIN_BG)
        self.set_background_image()

        center_frame = tk.Frame(self.root, bg="white", padx=20, pady=20, relief="raised", bd=2)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="Create Account", font=self.header_font, bg="white", fg=TEXT_COLOR).pack(pady=10)
        tk.Label(center_frame, text="Username", bg="white", font=self.font_regular).pack(anchor="w", pady=2)
        self.reg_username = ttk.Entry(center_frame, width=30)
        self.reg_username.pack(pady=2)

        tk.Label(center_frame, text="Password", bg="white", font=self.font_regular).pack(anchor="w", pady=2)
        self.reg_password = ttk.Entry(center_frame, show="*", width=30)
        self.reg_password.pack(pady=2)

        ttk.Button(center_frame, text="Register", command=self.register).pack(pady=10)
        ttk.Button(center_frame, text="Back to Login", command=self.create_login_page).pack()

    def login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()
        self.login_username.delete(0, tk.END)
        self.login_password.delete(0, tk.END)

        if username in users and users[username] == password:
            self.current_user = username
            self.create_main_interface()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def forgot_password(self):
        """Handle forgot password functionality."""
        forgot_window = tk.Toplevel(self.root)
        forgot_window.title("Forgot Password")
        forgot_window.geometry("400x250")
        forgot_window.configure(bg="white")
        forgot_window.resizable(False, False)

        
        header_frame = tk.Frame(forgot_window, bg="#0B8FA3", height=50)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="Reset Password", font=("Arial", 16, "bold"), 
                bg="#0B8FA3", fg="white").pack(pady=12)

        
        content_frame = tk.Frame(forgot_window, bg="white")
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)

        
        tk.Label(content_frame, text="Enter your username to reset your password", 
                font=("Arial", 10), bg="white", fg="#666").pack(pady=(0, 20))

        
        tk.Label(content_frame, text="Username", font=("Arial", 10), bg="white", fg="#333").pack(anchor="w", pady=(5, 2))
        username_entry = tk.Entry(content_frame, font=("Arial", 11), width=30, border=1, relief="solid")
        username_entry.pack(pady=(0, 20), fill="x")

        
        button_frame = tk.Frame(content_frame, bg="white")
        button_frame.pack(fill="x", pady=10)

        def reset_password():
            username = username_entry.get().strip()
            if not username:
                messagebox.showerror("Error", "Please enter your username")
                return
            
            if username not in users:
                messagebox.showerror("Error", "Username not found")
                return
            
            
            new_pass_window = tk.Toplevel(forgot_window)
            new_pass_window.title("Set New Password")
            new_pass_window.geometry("400x200")
            new_pass_window.configure(bg="white")
            new_pass_window.resizable(False, False)

            tk.Label(new_pass_window, text="Enter New Password", font=("Arial", 12, "bold"), 
                    bg="white", fg="#0B8FA3").pack(pady=15)

            tk.Label(new_pass_window, text="New Password:", font=("Arial", 10), bg="white").pack(anchor="w", padx=30, pady=(5, 2))
            new_pass_entry = tk.Entry(new_pass_window, show="•", font=("Arial", 11), width=30, border=1, relief="solid")
            new_pass_entry.pack(padx=30, pady=(0, 15), fill="x")

            def confirm_reset():
                new_password = new_pass_entry.get().strip()
                if not new_password:
                    messagebox.showerror("Error", "Please enter a new password")
                    return
                
                
                users[username] = new_password
                
                
                try:
                    
                    all_users = []
                    if os.path.exists(USERS_FILE):
                        with open(USERS_FILE, 'r') as f:
                            for line in f:
                                line = line.strip()
                                if line:
                                    user_data = json.loads(line)
                                    if user_data['username'] == username:
                                        user_data['password'] = new_password
                                    all_users.append(user_data)
                    
                    
                    with open(USERS_FILE, 'w') as f:
                        for user in all_users:
                            f.write(json.dumps(user) + '\n')
                    
                    
                    save_forgot_password_record(username, new_password)
                    
                    messagebox.showinfo("Success", "Password reset successfully! Please login with your new password.")
                    new_pass_window.destroy()
                    forgot_window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to reset password: {str(e)}")

            tk.Button(new_pass_window, text="Confirm", command=confirm_reset, 
                     bg="#0B8FA3", fg="white", font=("Arial", 11, "bold"), 
                     border=0, relief="flat", cursor="hand2", padx=20, pady=8).pack(pady=10)

        tk.Button(button_frame, text="Reset Password", command=reset_password, 
                 bg="#0B8FA3", fg="white", font=("Arial", 11, "bold"), 
                 border=0, relief="flat", cursor="hand2", padx=20, pady=8).pack(side="left", padx=5)
        tk.Button(button_frame, text="Cancel", command=forgot_window.destroy, 
                 bg="#999", fg="white", font=("Arial", 11, "bold"), 
                 border=0, relief="flat", cursor="hand2", padx=20, pady=8).pack(side="left", padx=5)

    def register(self):
        username = self.reg_username.get().strip()
        password = self.reg_password.get().strip()
        self.reg_username.delete(0, tk.END)
        self.reg_password.delete(0, tk.END)

        if username in users:
            messagebox.showerror("Error", "Username already exists")
        elif not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
        else:
            users[username] = password
            save_user(username, password)
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.create_login_page()

    def create_main_interface(self):
        self.clear_window()
        self.root.configure(bg=MAIN_BG)
        self.set_background_image()

        header = tk.Frame(self.root, bg=ACCENT, height=90)
        header.pack(fill="x")
        tk.Label(header, text=f"🏥 Clinic Booking — Welcome, {self.current_user}",
                 font=self.header_font, bg=ACCENT, fg="white").pack(side="left", padx=20, pady=15)

        date_frame = tk.Frame(header, bg=ACCENT)
        date_frame.pack(side="right", padx=20)
        tk.Label(date_frame, text="Pick appointment date:", bg=ACCENT, fg="white", font=self.font_regular).pack(side="left", padx=(0, 5))
        date_entry = DateEntry(date_frame, textvariable=self.selected_date, width=12, background="darkblue",
                               foreground="white", borderwidth=2)
        date_entry.pack(side="left")

        self.cart = {}
        products_frame = tk.Frame(self.root, bg=MAIN_BG)
        products_frame.pack(pady=30)

        image_files = {
            "Dental Cleaning": "dental.jpeg",
            "Physical Therapy": "physical therapy.jpeg",
            "Eye Check-up": "eye.jpg"
        }

        columns = 3
        row = 0
        col = 0
        for product, price in services.items():
            card = tk.Frame(products_frame, bg=CARD_BG, bd=1, relief="solid", padx=20, pady=10)
            card.grid(row=row, column=col, padx=20, pady=20, ipadx=10, ipady=10)
            try:
                img = Image.open(image_files[product])
                img = img.resize((150, 150), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.product_images[product] = photo
                tk.Label(card, image=photo, bg=CARD_BG).pack(pady=5)
            except Exception:
                tk.Label(card, text="[Image Missing]", bg=CARD_BG, relief="sunken", width=20, height=8).pack(pady=5)

            tk.Label(card, text=f"{product}", font=self.font_bold, bg=CARD_BG, fg=TEXT_COLOR).pack()
            tk.Label(card, text=f"₱{price}", font=self.font_regular, bg=CARD_BG, fg="#6B6B6B").pack(pady=(0, 5))

            qty_var = tk.IntVar(value=0)
            qty_frame = tk.Frame(card, bg=CARD_BG)
            qty_frame.pack(pady=5)
            tk.Label(qty_frame, text="Select:", bg=CARD_BG, fg=TEXT_COLOR).pack(side=tk.LEFT)
            tk.Spinbox(qty_frame, from_=0, to=10, width=5, textvariable=qty_var).pack(side=tk.LEFT, padx=5)
            self.cart[product] = qty_var

            col += 1
            if col >= columns:
                col = 0
                row += 1
    
        buttons_frame = tk.Frame(self.root, bg=MAIN_BG)
        buttons_frame.pack(pady=20)
        ttk.Button(buttons_frame, text="Appointment Summary", command=self.checkout).pack(side=tk.LEFT, padx=10)
        ttk.Button(buttons_frame, text="View My Bookings", command=self.view_bookings).pack(side=tk.LEFT, padx=10)
        ttk.Button(buttons_frame, text="Logout", command=self.logout).pack(side=tk.LEFT)

    def checkout(self):
        total = 0
        selected_services = []
        for product, qty_var in self.cart.items():
            qty = qty_var.get()
            if qty > 0:
                price = services[product]
                subtotal = price * qty
                total += subtotal
                selected_services.append((product, qty, subtotal))

        if total == 0:
            messagebox.showinfo("No Selection", "Please select at least one service to book.")
            return

        chosen_date = self.selected_date.get()
        if not chosen_date:
            messagebox.showerror("Date Required", "Please pick an appointment date before confirming.")
            return

        summary_window = tk.Toplevel(self.root)
        summary_window.title("Appointment Summary")
        summary_window.geometry("360x420")
        summary_window.configure(bg="white")

        tk.Label(summary_window, text="🧾 Appointment Summary", font=self.header_font, bg="white").pack(pady=10)
        tk.Label(summary_window, text=f"Patient: {self.current_user}", bg="white", font=self.font_regular).pack(pady=(0, 5))
        tk.Label(summary_window, text=f"Date: {chosen_date}", bg="white", font=self.font_regular).pack(pady=(0, 10))

        for prod, qty, subtotal in selected_services:
            tk.Label(summary_window, text=f"{prod} x{qty} = ₱{subtotal}", bg="white", font=self.font_regular).pack(anchor="w", padx=20)

        tk.Label(summary_window, text=f"\nTotal: ₱{total}", font=self.font_bold, bg="white").pack(pady=10)

        def confirm_and_close():
            self.show_receipt(self.current_user, chosen_date, selected_services, total)
            for v in self.cart.values():
                v.set(0)
            summary_window.destroy()

        ttk.Button(summary_window, text="Confirm Booking", command=confirm_and_close).pack(pady=8)
        ttk.Button(summary_window, text="Close", command=summary_window.destroy).pack()

    def show_receipt(self, patient_name, appointment_date, services_list, total_amount):
        """Display a professional receipt page for the confirmed booking."""
        # Save booking to file
        save_booking(patient_name, appointment_date, services_list, total_amount)
        
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("Booking Receipt")
        receipt_window.geometry("500x650")
        receipt_window.configure(bg="white")
        receipt_window.resizable(False, False)

        # Header
        header_frame = tk.Frame(receipt_window, bg=ACCENT, height=80)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="🏥 CLINIC BOOKING RECEIPT", font=("Arial", 16, "bold"), 
                 bg=ACCENT, fg="white").pack(pady=15)

        # Main content frame
        content_frame = tk.Frame(receipt_window, bg="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Receipt number and date
        receipt_num = f"RCP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        tk.Label(content_frame, text=f"Receipt #: {receipt_num}", font=("Arial", 9), 
                 bg="white", fg="#666").pack(anchor="w", pady=(0, 10))
        tk.Label(content_frame, text=f"Issued: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                 font=("Arial", 9), bg="white", fg="#666").pack(anchor="w", pady=(0, 15))

        # Separator
        tk.Label(content_frame, text="─" * 50, bg="white", fg="#DDD").pack(anchor="w", pady=(0, 10))

        # Patient details
        tk.Label(content_frame, text="PATIENT INFORMATION", font=("Arial", 10, "bold"), 
                 bg="white", fg=TEXT_COLOR).pack(anchor="w", pady=(0, 5))
        tk.Label(content_frame, text=f"Name: {patient_name}", font=("Arial", 10), 
                 bg="white", fg=TEXT_COLOR).pack(anchor="w")
        tk.Label(content_frame, text=f"Appointment Date: {appointment_date}", font=("Arial", 10), 
                 bg="white", fg=TEXT_COLOR).pack(anchor="w", pady=(0, 15))

        # Separator
        tk.Label(content_frame, text="─" * 50, bg="white", fg="#DDD").pack(anchor="w", pady=(0, 10))

        # Services
        tk.Label(content_frame, text="SERVICES BOOKED", font=("Arial", 10, "bold"), 
                 bg="white", fg=TEXT_COLOR).pack(anchor="w", pady=(0, 8))

        for service_name, qty, subtotal in services_list:
            service_frame = tk.Frame(content_frame, bg="white")
            service_frame.pack(fill="x", pady=3)
            tk.Label(service_frame, text=f"  {service_name}", font=("Arial", 9), 
                     bg="white", fg=TEXT_COLOR).pack(side="left", anchor="w")
            tk.Label(service_frame, text=f"x{qty}", font=("Arial", 9), 
                     bg="white", fg=TEXT_COLOR).pack(side="right")

            price_frame = tk.Frame(content_frame, bg="white")
            price_frame.pack(fill="x", pady=(0, 8))
            tk.Label(price_frame, text=f"    ₱{subtotal}", font=("Arial", 9, "bold"), 
                     bg="white", fg=BUTTON_COLOR).pack(side="right")

        # Separator
        tk.Label(content_frame, text="─" * 50, bg="white", fg="#DDD").pack(anchor="w", pady=(10, 10))

        # Total
        total_frame = tk.Frame(content_frame, bg="white")
        total_frame.pack(fill="x", pady=10)
        tk.Label(total_frame, text="TOTAL AMOUNT:", font=("Arial", 11, "bold"), 
                 bg="white", fg=TEXT_COLOR).pack(side="left")
        tk.Label(total_frame, text=f"₱{total_amount}", font=("Arial", 14, "bold"), 
                 bg="white", fg=ACCENT).pack(side="right")

        # Separator
        tk.Label(content_frame, text="─" * 50, bg="white", fg="#DDD").pack(anchor="w", pady=(10, 15))

        # Footer message
        tk.Label(content_frame, text="✓ Booking Confirmed Successfully!", font=("Arial", 10, "bold"), 
                 bg="white", fg="#4CAF50").pack(pady=10)
        tk.Label(content_frame, text="A confirmation email has been sent to your registered email.", 
                 font=("Arial", 8), bg="white", fg="#999", wraplength=400).pack(pady=(0, 15))

        # Buttons
        button_frame = tk.Frame(receipt_window, bg="white")
        button_frame.pack(fill="x", padx=20, pady=15)
        ttk.Button(button_frame, text="Print Receipt", command=lambda: self.print_receipt(receipt_num, patient_name, appointment_date, services_list, total_amount)).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Close", command=receipt_window.destroy).pack(side="left", padx=5)

    def print_receipt(self, receipt_num, patient_name, appointment_date, services_list, total_amount):
        """Handle print receipt functionality."""
        messagebox.showinfo("Print", f"Receipt #{receipt_num} sent to printer.\n\nPatient: {patient_name}\nDate: {appointment_date}\nTotal: ₱{total_amount}")
    
    def view_bookings(self):
        """Display all bookings for the logged-in user."""
        bookings = load_bookings_for_user(self.current_user)
        
        bookings_window = tk.Toplevel(self.root)
        bookings_window.title("My Bookings")
        bookings_window.geometry("700x600")
        bookings_window.configure(bg="white")

        
        header_frame = tk.Frame(bookings_window, bg=ACCENT, height=60)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="📋 My Bookings", font=("Arial", 16, "bold"), 
                 bg=ACCENT, fg="white").pack(pady=15)

        
        content_frame = tk.Frame(bookings_window, bg="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        if not bookings:
            tk.Label(content_frame, text="No bookings found.", font=("Arial", 12), 
                     bg="white", fg="#999").pack(pady=50)
        else:
            
            canvas = tk.Canvas(content_frame, bg="white", highlightthickness=0)
            scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="white")

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            
            for booking in bookings:
                booking_card = tk.Frame(scrollable_frame, bg=CARD_BG, bd=1, relief="solid", padx=15, pady=15)
                booking_card.pack(fill="x", pady=10)

                
                header_row = tk.Frame(booking_card, bg=CARD_BG)
                header_row.pack(fill="x", pady=(0, 10))
                tk.Label(header_row, text=f"Booking ID: {booking['booking_id']}", font=("Arial", 10, "bold"), 
                         bg=CARD_BG, fg=TEXT_COLOR).pack(side="left")
                tk.Label(header_row, text=f"Status: {booking['status'].upper()}", font=("Arial", 9, "bold"), 
                         bg=CARD_BG, fg="#4CAF50").pack(side="right")

                
                tk.Label(booking_card, text=f"Appointment Date: {booking['appointment_date']}", 
                         font=("Arial", 10), bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="w", pady=3)

                
                tk.Label(booking_card, text="Services:", font=("Arial", 9, "bold"), 
                         bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="w", pady=(5, 3))
                
                for service in booking['services']:
                    service_name, qty, price = service
                    tk.Label(booking_card, text=f"  • {service_name} x{qty} = ₱{price}", 
                             font=("Arial", 9), bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="w")

                
                total_frame = tk.Frame(booking_card, bg=CARD_BG)
                total_frame.pack(fill="x", pady=(10, 0))
                tk.Label(total_frame, text=f"Total: ₱{booking['total_amount']}", font=("Arial", 10, "bold"), 
                         bg=CARD_BG, fg=ACCENT).pack(side="left")
                tk.Label(total_frame, text=f"Booked on: {booking['created_at']}", font=("Arial", 8), 
                         bg=CARD_BG, fg="#999").pack(side="right")

                
                def cancel_booking(booking_data=booking):
                    def confirm_cancel():
                        reason = reason_entry.get().strip()
                        save_cancellation_record(
                            self.current_user,
                            booking_data['booking_id'],
                            booking_data['appointment_date'],
                            booking_data['services'],
                            booking_data['total_amount'],
                            reason
                        )
                        messagebox.showinfo("Success", "Booking cancelled successfully!")
                        cancel_window.destroy()
                        bookings_window.destroy()
                        self.view_bookings()

                    cancel_window = tk.Toplevel(bookings_window)
                    cancel_window.title("Cancel Booking")
                    cancel_window.geometry("400x200")
                    cancel_window.configure(bg="white")
                    cancel_window.resizable(False, False)

                    tk.Label(cancel_window, text="Cancel Booking", font=("Arial", 14, "bold"), 
                            bg="white", fg=ACCENT).pack(pady=15)
                    tk.Label(cancel_window, text="Reason for cancellation (optional):", font=("Arial", 10), 
                            bg="white").pack(anchor="w", padx=20, pady=(5, 2))
                    
                    reason_entry = tk.Entry(cancel_window, font=("Arial", 10), width=40, border=1, relief="solid")
                    reason_entry.pack(padx=20, pady=(0, 15), fill="x")

                    button_frame = tk.Frame(cancel_window, bg="white")
                    button_frame.pack(fill="x", padx=20, pady=10)
                    tk.Button(button_frame, text="Confirm Cancel", command=confirm_cancel, 
                             bg="#FF6B6B", fg="white", font=("Arial", 10, "bold"), 
                             border=0, relief="flat", cursor="hand2").pack(side="left", padx=5)
                    tk.Button(button_frame, text="Keep Booking", command=cancel_window.destroy, 
                             bg="#999", fg="white", font=("Arial", 10, "bold"), 
                             border=0, relief="flat", cursor="hand2").pack(side="left", padx=5)

                cancel_btn = tk.Button(booking_card, text="❌ Cancel Booking", command=cancel_booking, 
                                      bg="#FF6B6B", fg="white", font=("Arial", 9, "bold"), 
                                      border=0, relief="flat", cursor="hand2", padx=10, pady=5)
                cancel_btn.pack(pady=(10, 0), fill="x")

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

        
        button_frame = tk.Frame(bookings_window, bg="white")
        button_frame.pack(fill="x", padx=20, pady=15)
        ttk.Button(button_frame, text="Close", command=bookings_window.destroy).pack()

    def logout(self):
        self.current_user = None
        self.create_login_page()


if __name__ == "__main__":
    root = tk.Tk()
    app = ClinicBookingApp(root)
    root.mainloop()
