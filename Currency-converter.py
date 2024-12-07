import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("500x600")

        # Currency Symbols for West African countries
        self.currency_symbols = {
            "USD": "$", "EUR": "€", "GBP": "£", "INR": "₹", "NGN": "₦",  # Added NGN for Nigeria
            "XOF": "CFA",  # West African CFA Franc
            "XAF": "CFA"  # Central African CFA Franc
        }

        # UI Setup
        self.create_widgets()

        # Initialize history list
        self.history_list = []

    def create_widgets(self):
        # Title Label
        self.title_label = tk.Label(self.root, text="Currency Converter", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=10)

        # Amount Entry
        self.amount_label = tk.Label(self.root, text="Amount:")
        self.amount_label.pack(pady=5)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack(pady=5)

        # From Currency Dropdown
        self.from_currency_label = tk.Label(self.root, text="From Currency:")
        self.from_currency_label.pack(pady=5)
        self.from_currency = tk.StringVar(self.root)
        self.from_currency.set("USD")
        self.from_currency_menu = tk.OptionMenu(self.root, self.from_currency, "USD", "EUR", "GBP", "INR", "NGN", "XOF", "XAF")
        self.from_currency_menu.pack(pady=5)

        # To Currency Dropdown
        self.to_currency_label = tk.Label(self.root, text="To Currency:")
        self.to_currency_label.pack(pady=5)
        self.to_currency = tk.StringVar(self.root)
        self.to_currency.set("EUR")
        self.to_currency_menu = tk.OptionMenu(self.root, self.to_currency, "USD", "EUR", "GBP", "INR", "NGN", "XOF", "XAF")
        self.to_currency_menu.pack(pady=5)

        # Convert Button
        self.convert_button = tk.Button(self.root, text="Convert", command=self.convert_currency)
        self.convert_button.pack(pady=10)

        # Result Label
        self.result_label = tk.Label(self.root, text="Converted Amount:", font=("Arial", 14, "bold"))
        self.result_label.pack(pady=5)
        self.result = tk.Label(self.root, text="", font=("Arial", 14))
        self.result.pack(pady=5)

        # Conversion History
        self.history_label = tk.Label(self.root, text="Conversion History", font=("Arial", 14, "bold"))
        self.history_label.pack(pady=10)
        self.history_box = tk.Listbox(self.root, width=50, height=5)
        self.history_box.pack(pady=10)

        # Graph Button
        self.graph_button = tk.Button(self.root, text="Show Exchange Rate Trend", command=self.show_graph)
        self.graph_button.pack(pady=10)

        # Dark Mode Button
        self.dark_mode_button = tk.Button(self.root, text="Toggle Dark Mode", command=self.toggle_dark_mode)
        self.dark_mode_button.pack(pady=5)

    def convert_currency(self):
        # Validate amount input
        amount = self.amount_entry.get()
        if not amount.replace('.', '', 1).isdigit():
            messagebox.showerror("Invalid Input", "Please enter a valid number for amount.")
            return

        amount = float(amount)
        from_currency = self.from_currency.get()
        to_currency = self.to_currency.get()

        # Fetch exchange rates using an API
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        try:
            response = requests.get(url)
            data = response.json()

            rate = data["rates"].get(to_currency)
            if rate:
                converted_amount = amount * rate
                symbol = self.currency_symbols.get(to_currency, "")
                self.result.config(text=f"{symbol}{converted_amount:.2f}")
                self.add_to_history(amount, from_currency, to_currency, converted_amount)
            else:
                messagebox.showerror("Error", "Unable to fetch conversion rate.")
        except requests.exceptions.RequestException:
            messagebox.showerror("Network Error", "Unable to fetch exchange rates. Please check your connection.")

    def add_to_history(self, amount, from_currency, to_currency, result):
        # Add conversion to history
        history_entry = f"{amount} {from_currency} = {result} {to_currency}"
        self.history_list.append(history_entry)
        self.history_box.insert(tk.END, history_entry)

    def show_graph(self):
        # Placeholder data for graph (use real-time historical data for advanced app)
        dates = ["2023-01-01", "2023-01-02", "2023-01-03"]
        rates = [1.15, 1.18, 1.17]  # Example rates

        plt.plot(dates, rates)
        plt.title("Currency Trend (USD to EUR)")
        plt.xlabel("Date")
        plt.ylabel("Exchange Rate")
        plt.show()

    def toggle_dark_mode(self):
        if self.root.config("bg")[-1] == "#f5f5f5":
            self.root.config(bg="#2c3e50")
            self.title_label.config(fg="#ecf0f1", bg="#2c3e50")
            self.amount_label.config(fg="#ecf0f1", bg="#2c3e50")
            self.amount_entry.config(bg="#34495e", fg="white")
            self.result.config(fg="#ecf0f1", bg="#2c3e50")
            self.history_label.config(fg="#ecf0f1", bg="#2c3e50")
            self.history_box.config(bg="#34495e", fg="white")
            self.convert_button.config(bg="#34495e", fg="white")
            self.graph_button.config(bg="#34495e", fg="white")
            self.dark_mode_button.config(bg="#34495e", fg="white")
        else:
            self.root.config(bg="#f5f5f5")
            self.title_label.config(fg="#2c3e50", bg="#f5f5f5")
            self.amount_label.config(fg="#34495e", bg="#f5f5f5")
            self.amount_entry.config(bg="white", fg="black")
            self.result.config(fg="#34495e", bg="#f5f5f5")
            self.history_label.config(fg="#34495e", bg="#f5f5f5")
            self.history_box.config(bg="white", fg="black")
            self.convert_button.config(bg="#f5f5f5", fg="#2c3e50")
            self.graph_button.config(bg="#f5f5f5", fg="#2c3e50")
            self.dark_mode_button.config(bg="#f5f5f5", fg="#2c3e50")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
