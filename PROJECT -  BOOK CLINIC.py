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


class ClinicBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clinic Booking System")
        self.root.geometry("1200x800")
        self.root.configure(bg=MAIN_BG)
        self.current_user = None
        self.cart = {}
        self.product_images = {}

        # Load existing users from file
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

        self.create_login_page()
# try lang lods
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def set_background_image(self):
        """Set dental.jpeg as background for the entire page."""
        try:
            bg_img = Image.open("dental.jpeg")
            bg_img = bg_img.resize((1200, 800), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_img)
            bg_label = tk.Label(self.root, image=self.bg_photo)
            bg_label.image = self.bg_photo  # Keep a reference
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            pass

    def create_login_page(self):
        self.clear_window()
        self.root.configure(bg=MAIN_BG)
        self.set_background_image()

        login_frame = tk.Frame(self.root, width=700, height=400, bg="white", bd=2, relief="ridge")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        left_panel = tk.Frame(login_frame, bg=ACCENT, width=350, height=400)
        left_panel.pack(side="left", fill="both")

        tk.Label(left_panel, text="🏥 Welcome Back", font=self.header_font, bg=ACCENT, fg="white").place(
            relx=0.5, rely=0.35, anchor="center"
        )
        tk.Label(left_panel, text="Login to your Clinic Account", font=self.font_regular, bg=ACCENT, fg="white").place(
            relx=0.5, rely=0.5, anchor="center"
        )

        right_panel = tk.Frame(login_frame, bg="white", width=350, height=400)
        right_panel.pack(side="right", fill="both")

        tk.Label(right_panel, text="Login", font=self.header_font, bg="white").place(x=120, y=30) 
        tk.Label(right_panel, text="Email / Username", bg="white", font=self.font_regular).place(x=50, y=100)
        self.login_username = ttk.Entry(right_panel, width=30)
        self.login_username.place(x=50, y=125)

        tk.Label(right_panel, text="Password", bg="white", font=self.font_regular).place(x=50, y=165)
        self.login_password = ttk.Entry(right_panel, show="*", width=30)
        self.login_password.place(x=50, y=190)

        ttk.Button(right_panel, text="Submit", command=self.login).place(x=135, y=240)

        tk.Label(right_panel, text="Don't have an account?", bg="white", font=self.font_regular).place(x=60, y=290)
        register_link = tk.Label(
            right_panel,
            text="Register",
            fg="blue",
            cursor="hand2",
            bg="white",
            font=(self.font_regular[0], 10, "underline"),
        )
        register_link.place(x=210, y=290)
        register_link.bind("<Button-1>", lambda e: self.create_register_page())

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
            "Physical Therapy": "pt.jpg",
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
            tk.Spinbox(qty_frame, from_=0, to=1, width=5, textvariable=qty_var).pack(side=tk.LEFT, padx=5)
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

        # Header
        header_frame = tk.Frame(bookings_window, bg=ACCENT, height=60)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="📋 My Bookings", font=("Arial", 16, "bold"), 
                 bg=ACCENT, fg="white").pack(pady=15)

        # Main content frame with scrollbar
        content_frame = tk.Frame(bookings_window, bg="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        if not bookings:
            tk.Label(content_frame, text="No bookings found.", font=("Arial", 12), 
                     bg="white", fg="#999").pack(pady=50)
        else:
            # Create a canvas with scrollbar for multiple bookings
            canvas = tk.Canvas(content_frame, bg="white", highlightthickness=0)
            scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="white")

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Display each booking
            for booking in bookings:
                booking_card = tk.Frame(scrollable_frame, bg=CARD_BG, bd=1, relief="solid", padx=15, pady=15)
                booking_card.pack(fill="x", pady=10)

                # Booking ID and Status
                header_row = tk.Frame(booking_card, bg=CARD_BG)
                header_row.pack(fill="x", pady=(0, 10))
                tk.Label(header_row, text=f"Booking ID: {booking['booking_id']}", font=("Arial", 10, "bold"), 
                         bg=CARD_BG, fg=TEXT_COLOR).pack(side="left")
                tk.Label(header_row, text=f"Status: {booking['status'].upper()}", font=("Arial", 9, "bold"), 
                         bg=CARD_BG, fg="#4CAF50").pack(side="right")

                # Appointment Date
                tk.Label(booking_card, text=f"Appointment Date: {booking['appointment_date']}", 
                         font=("Arial", 10), bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="w", pady=3)

                # Services
                tk.Label(booking_card, text="Services:", font=("Arial", 9, "bold"), 
                         bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="w", pady=(5, 3))
                
                for service in booking['services']:
                    service_name, qty, price = service
                    tk.Label(booking_card, text=f"  • {service_name} x{qty} = ₱{price}", 
                             font=("Arial", 9), bg=CARD_BG, fg=TEXT_COLOR).pack(anchor="w")

                # Total and Created Date
                total_frame = tk.Frame(booking_card, bg=CARD_BG)
                total_frame.pack(fill="x", pady=(10, 0))
                tk.Label(total_frame, text=f"Total: ₱{booking['total_amount']}", font=("Arial", 10, "bold"), 
                         bg=CARD_BG, fg=ACCENT).pack(side="left")
                tk.Label(total_frame, text=f"Booked on: {booking['created_at']}", font=("Arial", 8), 
                         bg=CARD_BG, fg="#999").pack(side="right")

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

        # Close button
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
