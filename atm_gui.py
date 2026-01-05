from decimal import Decimal
import customtkinter as ctk
from tkinter import messagebox
import database

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("red")


class ATMApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ATM Simulator")
        self.geometry("420x480")
        self.user_id = None
        self.balance = 0
        self.login_screen()

    # ---------- LOGIN ----------
    def login_screen(self):
        self.clear()

        ctk.CTkLabel(self, text="ATM Login", font=("Arial", 22)).pack(pady=20)

        self.uid = ctk.CTkEntry(self, placeholder_text="User ID")
        self.uid.pack(pady=10)

        self.pin = ctk.CTkEntry(self, placeholder_text="PIN", show="*")
        self.pin.pack(pady=10)

        ctk.CTkButton(self, text="Login", command=self.login).pack(pady=10)
        ctk.CTkButton(self, text="Register", command=self.register_screen).pack()

    def login(self):
        result = database.login_user(self.uid.get(), self.pin.get())
        if result:
            self.user_id = self.uid.get()
            self.balance = result[0]
            self.dashboard()
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    # ---------- REGISTER ----------
    def register_screen(self):
        self.clear()

        ctk.CTkLabel(self, text="User Registration", font=("Arial", 22)).pack(pady=20)

        self.new_uid = ctk.CTkEntry(self, placeholder_text="New User ID")
        self.new_uid.pack(pady=10)

        self.new_pin = ctk.CTkEntry(self, placeholder_text="New PIN", show="*")
        self.new_pin.pack(pady=10)

        ctk.CTkButton(self, text="Create Account", command=self.register).pack(pady=10)
        ctk.CTkButton(self, text="Back to Login", command=self.login_screen).pack()

    def register(self):
        success = database.register_user(
            self.new_uid.get(),
            self.new_pin.get()
        )
        if success:
            messagebox.showinfo("Success", "Account Created Successfully")
            self.login_screen()
        else:
            messagebox.showerror("Error", "User ID Already Exists")

    # ---------- DASHBOARD ----------
    def dashboard(self):
        self.clear()

        ctk.CTkLabel(self, text=f"Welcome {self.user_id}", font=("Arial", 18)).pack(pady=15)

        ctk.CTkButton(self, text="Check Balance", command=self.check_balance).pack(pady=5)
        ctk.CTkButton(self, text="Deposit", command=self.deposit).pack(pady=5)
        ctk.CTkButton(self, text="Withdraw", command=self.withdraw).pack(pady=5)
        ctk.CTkButton(self, text="Transaction History", command=self.history).pack(pady=5)
        ctk.CTkButton(self, text="Logout", command=self.login_screen).pack(pady=15)

    # ---------- FUNCTIONS ----------
    def check_balance(self):
        messagebox.showinfo("Balance", f"₹{self.balance}")

    def deposit(self):
        amount = ctk.CTkInputDialog(
        text="Enter amount:",
        title="Deposit"
        ).get_input()

        if amount:
            amount = Decimal(amount)
            if amount > 0:
                self.balance += amount
                database.update_balance(self.user_id, self.balance)
                database.add_transaction(self.user_id, "Deposit", amount)
                messagebox.showinfo("Success", "Amount Deposited")


    def withdraw(self):
        amount = ctk.CTkInputDialog(
            text="Enter amount:",
            title="Withdraw"
        ).get_input()

        if amount:
            amount = Decimal(amount)
            if amount <= self.balance:
                self.balance -= amount
                database.update_balance(self.user_id, self.balance)
                database.add_transaction(self.user_id, "Withdraw", amount)
                messagebox.showinfo("Success", "Amount Withdrawn")
            else:
                messagebox.showerror("Error", "Insufficient Balance")
    def history(self):
        data = database.get_transactions(self.user_id)
        if not data:
            messagebox.showinfo("History", "No transactions")
        else:
            text = "\n".join([f"{a} ₹{b} | {t}" for a, b, t in data])
            messagebox.showinfo("Transactions", text)

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()


ATMApp().mainloop()
