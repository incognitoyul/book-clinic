import tkinter as tk
from tkinter import messagebox, ttk, font
from tkcalendar import DateEntry
from PIL import Image, ImageTk

users = {}

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


class ClinicBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clinic Booking System")
        self.root.geometry("1200x800")
        self.root.configure(bg=MAIN_BG)
        self.current_user = None
        self.cart = {}
        self.product_images = {}

        
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

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
#Test idol
    def create_login_page(self):
        self.clear_window()
        self.root.configure(bg=MAIN_BG)

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
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.create_login_page()

    def create_main_interface(self):
        self.clear_window()
        self.root.configure(bg=MAIN_BG)

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
            "Dental Cleaning": "dental.jpg",
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
            messagebox.showinfo("Booked", f"Your appointment on {chosen_date} has been booked.\nTotal: ₱{total}")
            for v in self.cart.values():
                v.set(0)
            summary_window.destroy()

        ttk.Button(summary_window, text="Confirm Booking", command=confirm_and_close).pack(pady=8)
        ttk.Button(summary_window, text="Close", command=summary_window.destroy).pack()

    def logout(self):
        self.current_user = None
        self.create_login_page()


if __name__ == "__main__":
    root = tk.Tk()
    app = ClinicBookingApp(root)
    root.mainloop()
