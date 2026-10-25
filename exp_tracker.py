
import tkinter as tk
from tkinter import messagebox
import json
import os
import math

# Application colors
BG = "#F3F0FF"
PURPLE = "#554080"
WHITE = "#FFFFFF"

# Save file location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(BASE_DIR, "expenses.json")

# Application data
expenses = []
total_expense = 0
saved_budget = None


# Save data to a JSON file
def save_data():
    data = {
        "budget": saved_budget,
        "expenses": expenses
    }

    try:
        with open(FILE_NAME, "w") as file:
            json.dump(data, file, indent=4)

    except OSError:
        messagebox.showerror(
            "Save Error",
            "Unable to save expense data."
        )


# Update dashboard
def update_dashboard():
    remaining = (
        saved_budget - total_expense
        if saved_budget is not None else 0
    )

    total_label.config(
        text=f"Rs. {total_expense:.2f}"
    )

    balance_label.config(
        text=f"Rs. {remaining:.2f}",
        fg="#B91C1C" if remaining < 0 else "#287855"
    )

    if saved_budget is None:
        status_label.config(
            text="Enter your first expense.",
            fg=PURPLE
        )
    elif remaining < 0:
        status_label.config(
            text="Warning: Budget exceeded!",
            fg="#B91C1C"
        )
    elif remaining == 0:
        status_label.config(
            text="Your budget is fully used.",
            fg=PURPLE
        )
    else:
        status_label.config(
            text="You are within your budget.",
            fg="#287855"
        )


# Add an expense
def add_expense():
    global total_expense, saved_budget

    try:
        budget = float(budget_entry.get())
        amount = float(amount_entry.get())
        category = category_entry.get().strip().title()

        if not math.isfinite(budget) or not math.isfinite(amount):
            messagebox.showerror(
                "Invalid Amount",
                "Please enter finite numbers."
            )
            return

        if budget < 0 or amount < 0:
            messagebox.showerror(
                "Invalid Amount",
                "Amounts cannot be negative."
            )
            return

        if not category:
            messagebox.showerror(
                "Missing Category",
                "Please enter a category."
            )
            return

        if saved_budget is not None and budget != saved_budget:
            messagebox.showerror(
                "Budget Changed",
                "Reset the tracker to change your budget."
            )
            return

        if saved_budget is None:
            saved_budget = budget
            budget_entry.config(state="disabled")

        expenses.append([category, amount])
        total_expense += amount

        history.insert(
            tk.END,
            f"{category} - Rs. {amount:.2f}"
        )

        update_dashboard()
        save_data()

        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numbers."
        )


# Load previously saved expenses
def load_data():
    global expenses, total_expense, saved_budget

    if not os.path.exists(FILE_NAME):
        return

    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)

        budget = data["budget"]
        loaded_expenses = data["expenses"]

        if (
            not isinstance(budget, (int, float))
            or not math.isfinite(budget)
            or budget < 0
            or not isinstance(loaded_expenses, list)
        ):
            raise ValueError("Invalid saved data")

        checked_expenses = []

        for item in loaded_expenses:
            if (
                not isinstance(item, list)
                or len(item) != 2
                or not isinstance(item[0], str)
                or not item[0].strip()
                or not isinstance(item[1], (int, float))
                or not math.isfinite(item[1])
                or item[1] < 0
            ):
                raise ValueError("Invalid expense record")

            checked_expenses.append(item)

        expenses = checked_expenses
        saved_budget = budget

        total_expense = sum(
            item[1] for item in expenses
        )

        budget_entry.insert(0, str(saved_budget))
        budget_entry.config(state="disabled")

        for category, amount in expenses:
            history.insert(
                tk.END,
                f"{category} - Rs. {amount:.2f}"
            )

        update_dashboard()

    except (OSError, ValueError, KeyError, TypeError):
        messagebox.showwarning(
            "Load Error",
            "Saved data could not be loaded."
        )


# Reset the tracker
def reset_tracker():
    global expenses, total_expense, saved_budget

    if not messagebox.askyesno(
        "Confirm Reset",
        "Delete all saved expenses and start again?"
    ):
        return

    expenses = []
    total_expense = 0
    saved_budget = None

    budget_entry.config(state="normal")
    budget_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

    history.delete(0, tk.END)

    update_dashboard()
    save_data()


# Create main window
window = tk.Tk()
window.title("Smart Student Expense Tracker")
window.geometry("560x700")
window.configure(bg=BG)

# Main heading
tk.Label(
    window,
    text="Smart Student Expense Tracker",
    font=("Arial", 19, "bold"),
    bg=BG,
    fg=PURPLE
).pack(pady=(20, 5))

tk.Label(
    window,
    text="Your personal money dashboard",
    font=("Arial", 11),
    bg=BG,
    fg="#7D7097"
).pack(pady=(0, 15))

# Summary cards
summary = tk.Frame(window, bg=BG)
summary.pack(pady=10)

spent_frame = tk.Frame(
    summary, bg=WHITE, padx=25, pady=15
)
spent_frame.pack(side="left", padx=10)

tk.Label(
    spent_frame,
    text="TOTAL SPENT",
    bg=WHITE, fg=PURPLE
).pack()

total_label = tk.Label(
    spent_frame,
    text="Rs. 0.00",
    font=("Arial", 16, "bold"),
    bg=WHITE, fg=PURPLE
)
total_label.pack()

balance_frame = tk.Frame(
    summary, bg=WHITE, padx=25, pady=15
)
balance_frame.pack(side="left", padx=10)

tk.Label(
    balance_frame,
    text="REMAINING",
    bg=WHITE, fg=PURPLE
).pack()

balance_label = tk.Label(
    balance_frame,
    text="Rs. 0.00",
    font=("Arial", 16, "bold"),
    bg=WHITE, fg="#287855"
)
balance_label.pack()

# Input section
form = tk.Frame(window, bg=BG)
form.pack(pady=10)

tk.Label(
    form, text="Monthly Budget (Rs.)",
    bg=BG, fg=PURPLE
).pack(pady=4)

budget_entry = tk.Entry(
    form, width=35,
    bg=WHITE, fg="black",
    insertbackground="black",
    disabledforeground="#554080"
)
budget_entry.pack(pady=4)

tk.Label(
    form, text="Expense Category",
    bg=BG, fg=PURPLE
).pack(pady=4)

category_entry = tk.Entry(
    form, width=35,
    bg=WHITE, fg="black",
    insertbackground="black"
)
category_entry.pack(pady=4)

tk.Label(
    form, text="Expense Amount (Rs.)",
    bg=BG, fg=PURPLE
).pack(pady=4)

amount_entry = tk.Entry(
    form, width=35,
    bg=WHITE, fg="black",
    insertbackground="black"
)
amount_entry.pack(pady=4)

# Buttons
tk.Button(
    window,
    text="+ Add Expense",
    font=("Arial", 12, "bold"),
    fg="black",
    width=22,
    command=add_expense
).pack(pady=10)

tk.Button(
    window,
    text="Reset Tracker",
    fg="black",
    width=22,
    command=reset_tracker
).pack(pady=5)

# Status
status_label = tk.Label(
    window,
    text="Enter your first expense.",
    bg=BG, fg=PURPLE,
    font=("Arial", 11)
)
status_label.pack(pady=10)

# Expense history
tk.Label(
    window,
    text="Recent Expenses",
    font=("Arial", 13, "bold"),
    bg=BG, fg=PURPLE
).pack(pady=5)

history = tk.Listbox(
    window,
    width=45,
    height=6,
    bg=WHITE,
    fg="black",
    font=("Arial", 11)
)
history.pack(pady=5)

# Restore saved data after widgets exist
load_data()

# Keep application running
window.mainloop()
