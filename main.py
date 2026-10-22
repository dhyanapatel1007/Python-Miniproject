
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from backend import ExpenseTracker


class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.tracker = ExpenseTracker()

        # Color palette
        self.bg = "#F5F6FC"
        self.white = "#FFFFFF"
        self.navy = "#20213D"
        self.purple = "#7161EF"
        self.purple_dark = "#5949D8"
        self.purple_light = "#EEEAFE"
        self.green = "#159B72"
        self.green_light = "#E4F7EF"
        self.red = "#E35D6A"
        self.red_light = "#FDEBED"
        self.text = "#292A43"
        self.muted = "#898AA3"
        self.border = "#E9EAF3"

        self.root.title("PocketWise | Personal Finance")
        self.root.geometry("1180x760")
        self.root.minsize(900, 650)
        self.root.configure(bg=self.bg)

        self.setup_styles()
        self.create_interface()
        self.refresh_dashboard()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Modern.Treeview",
            background=self.white,
            foreground=self.text,
            fieldbackground=self.white,
            rowheight=42,
            borderwidth=0,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Modern.Treeview.Heading",
            background="#F7F7FC",
            foreground=self.muted,
            font=("Segoe UI", 9, "bold"),
            padding=(10, 13),
            relief="flat"
        )

        style.map(
            "Modern.Treeview",
            background=[("selected", self.purple_light)],
            foreground=[("selected", self.text)]
        )

        style.configure(
            "Modern.Vertical.TScrollbar",
            background="#D9D8EA",
            troughcolor=self.white,
            bordercolor=self.white,
            arrowcolor=self.muted
        )

        style.configure(
            "Modern.TCombobox",
            padding=8,
            fieldbackground=self.white,
            background=self.white,
            foreground=self.text,
            arrowsize=14
        )

    # ---------------- MAIN LAYOUT ----------------

    def create_interface(self):
        self.create_header()

        body = tk.Frame(self.root, bg=self.bg)
        body.pack(fill="both", expand=True, padx=28, pady=22)

        self.create_welcome_section(body)
        self.create_summary_cards(body)

        workspace = tk.Frame(body, bg=self.bg)
        workspace.pack(fill="both", expand=True, pady=(22, 0))

        workspace.columnconfigure(0, weight=1, minsize=285)
        workspace.columnconfigure(1, weight=2, minsize=430)
        workspace.rowconfigure(0, weight=1)

        self.create_form(workspace)
        self.create_transaction_panel(workspace)

        footer = tk.Frame(body, bg=self.bg)
        footer.pack(fill="x", pady=(12, 0))

        tk.Label(
            footer,
            text="POCKETWISE  •  Small steps, smarter savings.",
            bg=self.bg,
            fg=self.muted,
            font=("Segoe UI", 9)
        ).pack(side="left")

        self.status_label = tk.Label(
            footer,
            text="Your finances, organized.",
            bg=self.bg,
            fg=self.muted,
            font=("Segoe UI", 9)
        )
        self.status_label.pack(side="right")

    def create_header(self):
        header = tk.Frame(self.root, bg=self.navy, height=92)
        header.pack(fill="x")
        header.pack_propagate(False)

        left = tk.Frame(header, bg=self.navy)
        left.pack(side="left", padx=28, pady=15)

        logo = tk.Label(
            left,
            text="P",
            bg=self.purple,
            fg=self.white,
            font=("Segoe UI", 21, "bold"),
            width=2,
            height=1
        )
        logo.pack(side="left", padx=(0, 13))

        brand = tk.Frame(left, bg=self.navy)
        brand.pack(side="left")

        tk.Label(
            brand,
            text="PocketWise",
            bg=self.navy,
            fg=self.white,
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        tk.Label(
            brand,
            text="PERSONAL FINANCE DASHBOARD",
            bg=self.navy,
            fg="#B9B7DD",
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", pady=(1, 0))

        right = tk.Frame(header, bg=self.navy)
        right.pack(side="right", padx=28)

        tk.Label(
            right,
            text="YOUR MONEY. YOUR CONTROL.",
            bg=self.navy,
            fg="#D2CFFC",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="e")

        tk.Label(
            right,
            text=date.today().strftime("%d %B %Y"),
            bg=self.navy,
            fg="#FFFFFF",
            font=("Segoe UI", 10)
        ).pack(anchor="e", pady=(5, 0))

    def create_welcome_section(self, parent):
        row = tk.Frame(parent, bg=self.bg)
        row.pack(fill="x", pady=(0, 18))

        left = tk.Frame(row, bg=self.bg)
        left.pack(side="left")

        tk.Label(
            left,
            text="Good money habits start here.",
            bg=self.bg,
            fg=self.text,
            font=("Segoe UI", 19, "bold")
        ).pack(anchor="w")

        tk.Label(
            left,
            text="Track your spending, monitor your income, and stay on budget.",
            bg=self.bg,
            fg=self.muted,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(5, 0))

        tk.Label(
            row,
            text="  LIVE OVERVIEW  ",
            bg=self.purple_light,
            fg=self.purple_dark,
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=8
        ).pack(side="right", pady=5)

    # ---------------- SUMMARY CARDS ----------------

    def create_summary_cards(self, parent):
        cards = tk.Frame(parent, bg=self.bg)
        cards.pack(fill="x")

        cards.columnconfigure((0, 1, 2), weight=1, uniform="summary")

        self.balance_value = self.make_summary_card(
            cards, 0, "TOTAL BALANCE", "₹ 0.00",
            "Income minus expenses", self.purple,
            self.purple_light, "B"
        )

        self.income_value = self.make_summary_card(
            cards, 1, "TOTAL INCOME", "₹ 0.00",
            "Money received", self.green,
            self.green_light, "+"
        )

        self.expense_value = self.make_summary_card(
            cards, 2, "TOTAL EXPENSES", "₹ 0.00",
            "Money spent", self.red,
            self.red_light, "-"
        )

    def make_summary_card(
        self, parent, column, heading, amount, subtitle,
        accent, light, symbol
    ):
        card = tk.Frame(
            parent,
            bg=self.white,
            highlightbackground=self.border,
            highlightthickness=1
        )
        card.grid(
            row=0, column=column, sticky="nsew",
            padx=(0 if column == 0 else 8, 8 if column < 2 else 0)
        )

        top = tk.Frame(card, bg=self.white)
        top.pack(fill="x", padx=18, pady=(16, 8))

        tk.Label(
            top,
            text=heading,
            bg=self.white,
            fg=self.muted,
            font=("Segoe UI", 9, "bold")
        ).pack(side="left")

        tk.Label(
            top,
            text=symbol,
            bg=light,
            fg=accent,
            font=("Segoe UI", 12, "bold"),
            width=3,
            pady=3
        ).pack(side="right")

        value_label = tk.Label(
            card,
            text=amount,
            bg=self.white,
            fg=accent,
            font=("Segoe UI", 23, "bold")
        )
        value_label.pack(anchor="w", padx=18, pady=(0, 2))

        tk.Label(
            card,
            text=subtitle,
            bg=self.white,
            fg=self.muted,
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=18, pady=(0, 17))

        tk.Frame(card, bg=accent, height=3).pack(
            side="bottom", fill="x"
        )

        return value_label

    # ---------------- TRANSACTION FORM ----------------

    def create_form(self, parent):
        panel = tk.Frame(
            parent,
            bg=self.white,
            highlightbackground=self.border,
            highlightthickness=1
        )
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        tk.Label(
            panel,
            text="New transaction",
            bg=self.white,
            fg=self.text,
            font=("Segoe UI", 15, "bold")
        ).pack(anchor="w", padx=19, pady=(19, 4))

        tk.Label(
            panel,
            text="Record your income or spending.",
            bg=self.white,
            fg=self.muted,
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=19, pady=(0, 14))

        tk.Frame(panel, bg=self.border, height=1).pack(
            fill="x", padx=19, pady=(0, 9)
        )

        self.title_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.category_var = tk.StringVar(value="Food")
        self.type_var = tk.StringVar(value="Expense")
        self.date_var = tk.StringVar(value=date.today().isoformat())

        self.create_input(
            panel, "DESCRIPTION", self.title_var,
            "e.g. Lunch with friends"
        )

        self.create_input(
            panel, "AMOUNT (₹)", self.amount_var,
            "e.g. 250"
        )

        self.create_combo(
            panel, "CATEGORY", self.category_var,
            [
                "Food", "Travel", "Shopping", "Bills",
                "Education", "Health", "Salary", "Other"
            ]
        )

        self.create_combo(
            panel, "TRANSACTION TYPE", self.type_var,
            ["Expense", "Income"]
        )

        self.create_input(
            panel, "DATE (YYYY-MM-DD)", self.date_var,
            "YYYY-MM-DD"
        )

        tk.Button(
            panel,
            text="＋   Save Transaction",
            command=self.add_transaction,
            bg=self.purple,
            fg=self.white,
            activebackground=self.purple_dark,
            activeforeground=self.white,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 11, "bold"),
            pady=12
        ).pack(fill="x", padx=19, pady=(19, 8))

        tk.Button(
            panel,
            text="Clear all fields",
            command=self.reset_form,
            bg="#F1F0FB",
            fg=self.purple_dark,
            activebackground="#E4E1FA",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            pady=9
        ).pack(fill="x", padx=19, pady=(0, 18))

    def create_input(self, parent, label, variable, placeholder):
        group = tk.Frame(parent, bg=self.white)
        group.pack(fill="x", padx=19, pady=(8, 2))

        tk.Label(
            group,
            text=label,
            bg=self.white,
            fg=self.text,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", pady=(0, 5))

        entry = tk.Entry(
            group,
            textvariable=variable,
            bg="#FCFCFF",
            fg=self.text,
            insertbackground=self.purple,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.border,
            highlightcolor=self.purple,
            font=("Segoe UI", 10)
        )
        entry.pack(fill="x", ipady=8)

        # Placeholder is a hint only; actual values are not overwritten.
        if not variable.get() and placeholder:
            entry.insert(0, placeholder)
            entry.config(fg="#A5A5B6")

            def clear_hint(event):
                if entry.get() == placeholder:
                    entry.delete(0, "end")
                    entry.config(fg=self.text)

            def restore_hint(event):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(fg="#A5A5B6")

            entry.bind("<FocusIn>", clear_hint)
            entry.bind("<FocusOut>", restore_hint)

    def create_combo(self, parent, label, variable, values):
        group = tk.Frame(parent, bg=self.white)
        group.pack(fill="x", padx=19, pady=(8, 2))

        tk.Label(
            group,
            text=label,
            bg=self.white,
            fg=self.text,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", pady=(0, 5))

        ttk.Combobox(
            group,
            textvariable=variable,
            values=values,
            state="readonly",
            style="Modern.TCombobox",
            font=("Segoe UI", 10)
        ).pack(fill="x")

    # ---------------- TRANSACTION TABLE ----------------

    def create_transaction_panel(self, parent):
        panel = tk.Frame(
            parent,
            bg=self.white,
            highlightbackground=self.border,
            highlightthickness=1
        )
        panel.grid(row=0, column=1, sticky="nsew")

        heading = tk.Frame(panel, bg=self.white)
        heading.pack(fill="x", padx=18, pady=(18, 5))

        tk.Label(
            heading,
            text="Transaction history",
            bg=self.white,
            fg=self.text,
            font=("Segoe UI", 15, "bold")
        ).pack(side="left")

        self.count_label = tk.Label(
            heading,
            text="0 records",
            bg=self.purple_light,
            fg=self.purple_dark,
            font=("Segoe UI", 9, "bold"),
            padx=8,
            pady=4
        )
        self.count_label.pack(side="right")

        tk.Label(
            panel,
            text="Review and manage your recent activity.",
            bg=self.white,
            fg=self.muted,
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=18, pady=(0, 12))

        search_row = tk.Frame(panel, bg=self.white)
        search_row.pack(fill="x", padx=18, pady=(0, 13))

        self.search_var = tk.StringVar()

        search_box = tk.Frame(
            search_row,
            bg="#FAFAFE",
            highlightbackground=self.border,
            highlightthickness=1
        )
        search_box.pack(side="left", fill="x", expand=True)

        tk.Label(
            search_box,
            text="⌕",
            bg="#FAFAFE",
            fg=self.purple,
            font=("Segoe UI", 17)
        ).pack(side="left", padx=(9, 3))

        tk.Entry(
            search_box,
            textvariable=self.search_var,
            bg="#FAFAFE",
            fg=self.text,
            insertbackground=self.purple,
            relief="flat",
            font=("Segoe UI", 10)
        ).pack(side="left", fill="x", expand=True, ipady=9, padx=5)

        tk.Button(
            search_row,
            text="Reset",
            command=lambda: self.search_var.set(""),
            bg=self.purple_light,
            fg=self.purple_dark,
            activebackground="#DFDAFC",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=8
        ).pack(side="left", padx=(7, 0))

        table_frame = tk.Frame(panel, bg=self.white)
        table_frame.pack(
            fill="both", expand=True, padx=12, pady=(0, 10)
        )

        columns = ("date", "title", "category", "type", "amount")

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            style="Modern.Treeview"
        )

        headings = {
            "date": "DATE",
            "title": "DESCRIPTION",
            "category": "CATEGORY",
            "type": "TYPE",
            "amount": "AMOUNT (₹)"
        }

        widths = {
            "date": 90,
            "title": 135,
            "category": 95,
            "type": 78,
            "amount": 100
        }

        for col in columns:
            self.table.heading(col, text=headings[col])
            self.table.column(
                col,
                width=widths[col],
                minwidth=60,
                anchor="w"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview,
            style="Modern.Vertical.TScrollbar"
        )
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.table.tag_configure(
            "Income", foreground=self.green
        )
        self.table.tag_configure(
            "Expense", foreground=self.red
        )

        bottom = tk.Frame(panel, bg=self.white)
        bottom.pack(fill="x", padx=18, pady=(0, 16))

        tk.Label(
            bottom,
            text="Select a row to remove a transaction.",
            bg=self.white,
            fg=self.muted,
            font=("Segoe UI", 9)
        ).pack(side="left")

        tk.Button(
            bottom,
            text="Delete selected",
            command=self.delete_transaction,
            bg=self.red_light,
            fg=self.red,
            activebackground="#F9D9DE",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=8
        ).pack(side="right")

        self.search_var.trace_add(
            "write",
            lambda *args: self.refresh_transactions()
        )

    # ---------------- APP FUNCTIONS ----------------

    def add_transaction(self):
        try:
            title = self.title_var.get().strip()
            amount = self.amount_var.get().strip()
            category = self.category_var.get()
            transaction_type = self.type_var.get()
            transaction_date = self.date_var.get().strip()

            # Prevent placeholder hints from being saved.
            if title == "e.g. Lunch with friends":
                title = ""
            if amount == "e.g. 250":
                amount = ""

            self.tracker.add_transaction(
                title,
                amount,
                category,
                transaction_type,
                transaction_date
            )

            self.refresh_dashboard()
            self.reset_form()

            self.status_label.config(
                text="Transaction saved successfully."
            )

            messagebox.showinfo(
                "Transaction saved",
                "Your transaction has been saved successfully."
            )

        except (ValueError, OSError) as error:
            messagebox.showerror(
                "Unable to save transaction", str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Unexpected error",
                f"Something went wrong:\n{error}"
            )

    def delete_transaction(self):
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No transaction selected",
                "Please select a transaction from the table first."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm deletion",
            "Are you sure you want to delete this transaction?"
        )

        if not confirm:
            return

        try:
            transaction_id = int(selected[0])
            self.tracker.delete_transaction(transaction_id)
            self.refresh_dashboard()

            self.status_label.config(
                text="Transaction deleted successfully."
            )

        except (ValueError, OSError) as error:
            messagebox.showerror(
                "Unable to delete transaction", str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Unexpected error",
                f"Something went wrong:\n{error}"
            )

    def reset_form(self):
        self.title_var.set("")
        self.amount_var.set("")
        self.category_var.set("Food")
        self.type_var.set("Expense")
        self.date_var.set(date.today().isoformat())

        self.status_label.config(text="Form cleared.")

    def refresh_dashboard(self):
        summary = self.tracker.get_summary()

        self.balance_value.config(
            text=f"₹ {summary['balance']:,.2f}"
        )
        self.income_value.config(
            text=f"₹ {summary['income']:,.2f}"
        )
        self.expense_value.config(
            text=f"₹ {summary['expenses']:,.2f}"
        )

        self.refresh_transactions()

    def refresh_transactions(self):
        if not hasattr(self, "table"):
            return

        for row in self.table.get_children():
            self.table.delete(row)

        search = self.search_var.get()
        transactions = self.tracker.get_transactions(search)

        for item in transactions:
            self.table.insert(
                "",
                "end",
                iid=str(item["id"]),
                values=(
                    item["date"],
                    item["title"],
                    item["category"],
                    item["type"],
                    f"{item['amount']:,.2f}"
                ),
                tags=(item["type"],)
            )

        count = len(transactions)
        self.count_label.config(
            text=f"{count} record" + ("" if count == 1 else "s")
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
