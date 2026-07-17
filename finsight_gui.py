import os
import json
import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# Data Persistence (Matches Streamlit and React formats)
DATA_FILE = "finsight_data.json"

DEFAULT_USER = {
    "id": "u_arjun_mehta",
    "name": "Arjun Mehta",
    "email": "arjun.mehta@example.com",
    "role": "Lead Product Architect",
    "avatarUrl": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&h=150&q=80",
    "currency": "₹",
    "joinedDate": "2026-01-15",
    "preferences": {
        "emailNotifications": True,
        "budgetAlerts": True,
        "theme": "light"
    }
}

DEFAULT_TRANSACTIONS = [
    {"id": "tx_1", "userId": "u_arjun_mehta", "description": "Consulting Retainer", "amount": 125000, "category": "Consulting", "type": "Income", "date": "2026-07-02"},
    {"id": "tx_2", "userId": "u_arjun_mehta", "description": "Office Workspace Rental", "amount": 28000, "category": "Rent", "type": "Expense", "date": "2026-07-03"},
    {"id": "tx_3", "userId": "u_arjun_mehta", "description": "Cloud Servers Subscription", "amount": 14200, "category": "Software", "type": "Expense", "date": "2026-07-05"},
    {"id": "tx_4", "userId": "u_arjun_mehta", "description": "Corporate Dinner client kickoff", "amount": 8500, "category": "Dining Out", "type": "Expense", "date": "2026-07-08"},
    {"id": "tx_5", "userId": "u_arjun_mehta", "description": "Dividends Payout", "amount": 12000, "category": "Dividends", "type": "Income", "date": "2026-07-10"},
    {"id": "tx_6", "userId": "u_arjun_mehta", "description": "High-Speed Internet Provider", "amount": 3200, "category": "Utilities", "type": "Expense", "date": "2026-07-11"},
    {"id": "tx_7", "userId": "u_arjun_mehta", "description": "Ergonomic Desk & Chair Set", "amount": 35000, "category": "Furniture", "type": "Expense", "date": "2026-07-12"}
]

DEFAULT_BUDGETS = [
    {"id": "b_1", "userId": "u_arjun_mehta", "category": "Rent", "amount": 30000, "month": "2026-07"},
    {"id": "b_2", "userId": "u_arjun_mehta", "category": "Software", "amount": 15000, "month": "2026-07"},
    {"id": "b_3", "userId": "u_arjun_mehta", "category": "Dining Out", "amount": 10000, "month": "2026-07"},
    {"id": "b_4", "userId": "u_arjun_mehta", "category": "Utilities", "amount": 5000, "month": "2026-07"},
    {"id": "b_5", "userId": "u_arjun_mehta", "category": "Furniture", "amount": 40000, "month": "2026-07"}
]

DEFAULT_INVESTMENTS = [
    {"id": "inv_1", "userId": "u_arjun_mehta", "symbol": "NIFTYBEES", "name": "Nifty 50 ETF", "units": 240, "purchasePrice": 210.50, "currentPrice": 235.80, "category": "Equity", "investedValue": 50520.0, "currentValue": 56592.0, "returnsValue": 6072.0, "returnsPercent": 12.02},
    {"id": "inv_2", "userId": "u_arjun_mehta", "symbol": "GOLDSHARE", "name": "Sovereign Gold Fund", "units": 45, "purchasePrice": 5200.00, "currentPrice": 5580.00, "category": "Commodities", "investedValue": 234000.0, "currentValue": 251100.0, "returnsValue": 17100.0, "returnsPercent": 7.31},
    {"id": "inv_3", "userId": "u_arjun_mehta", "symbol": "REIT_IR", "name": "Embassy Office Parks REIT", "units": 150, "purchasePrice": 340.00, "currentPrice": 325.00, "category": "Real Estate", "investedValue": 51000.0, "currentValue": 48750.0, "returnsValue": -2250.0, "returnsPercent": -4.41},
    {"id": "inv_4", "userId": "u_arjun_mehta", "symbol": "INFY", "name": "Infosys Ltd.", "units": 60, "purchasePrice": 1450.00, "currentPrice": 1580.00, "category": "Equity", "investedValue": 87000.0, "currentValue": 94800.0, "returnsValue": 7800.0, "returnsPercent": 8.97}
]

DEFAULT_GOALS = [
    {"id": "g_1", "userId": "u_arjun_mehta", "title": "Emergency Fund Reserves", "targetAmount": 300000, "currentAmount": 180000, "targetDate": "2026-12-31", "category": "Emergency", "status": "In Progress"},
    {"id": "g_2", "userId": "u_arjun_mehta", "title": "Core Portfolio Expansion", "targetAmount": 1000000, "currentAmount": 451242, "targetDate": "2027-06-30", "category": "Investments", "status": "In Progress"},
    {"id": "g_3", "userId": "u_arjun_mehta", "title": "Next-Gen Workstation Setup", "targetAmount": 150000, "currentAmount": 150000, "targetDate": "2026-08-15", "category": "Lifestyle", "status": "Completed"}
]

DEFAULT_TASKS = [
    {"id": "task_1", "milestone": "Milestone 1", "title": "Integrate real-time transaction engine", "status": "Completed"},
    {"id": "task_2", "milestone": "Milestone 1", "title": "Configure client budgets UI boundaries", "status": "Completed"},
    {"id": "task_3", "milestone": "Milestone 1", "title": "Build responsive dashboard graphs", "status": "Completed"},
    {"id": "task_4", "milestone": "Milestone 2", "title": "Establish cloud SQL persistent syncing", "status": "In Progress"},
    {"id": "task_5", "milestone": "Milestone 2", "title": "Deploy automated threshold alerting service", "status": "Todo"},
    {"id": "task_6", "milestone": "Milestone 2", "title": "Perform user security & penetration audit", "status": "Todo"}
]

class FinSightApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FinSight - Finance & Investment Intelligence")
        self.root.geometry("1100x750")
        self.root.configure(bg="#f8fafc")
        
        # Load Data
        self.db = self.load_database()
        self.currency = self.db["user"]["currency"]
        
        # Configure Styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#f8fafc', borderwidth=0)
        style.configure('TNotebook.Tab', font=('Helvetica', 10, 'bold'), padding=[15, 6])
        style.map('TNotebook.Tab', background=[('selected', '#4f46e5')], foreground=[('selected', '#ffffff')])
        
        # Main Header
        header_frame = tk.Frame(root, bg="#ffffff", height=80, bd=0, highlightthickness=1, highlightbackground="#e2e8f0")
        header_frame.pack(fill="x", side="top")
        
        title_label = tk.Label(header_frame, text=" FinSight Platform ", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#1e293b")
        title_label.pack(side="left", padx=25, pady=20)
        
        profile_frame = tk.Frame(header_frame, bg="#ffffff")
        profile_frame.pack(side="right", padx=25, pady=20)
        
        tk.Label(profile_frame, text=f"{self.db['user']['name']}", font=("Helvetica", 11, "bold"), bg="#ffffff", fg="#334155").pack(anchor="e")
        tk.Label(profile_frame, text=f"{self.db['user']['role']}", font=("Helvetica", 9), bg="#ffffff", fg="#64748b").pack(anchor="e")
        
        # Main Notebook (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Build Tabs
        self.create_dashboard_tab()
        self.create_budgets_tab()
        self.create_investments_tab()
        self.create_goals_tab()
        self.create_milestones_tab()
        
    def load_database(self):
        if not os.path.exists(DATA_FILE):
            data = {
                "user": DEFAULT_USER,
                "transactions": DEFAULT_TRANSACTIONS,
                "budgets": DEFAULT_BUDGETS,
                "investments": DEFAULT_INVESTMENTS,
                "goals": DEFAULT_GOALS,
                "tasks": DEFAULT_TASKS
            }
            self.save_database(data)
            return data
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {
                "user": DEFAULT_USER,
                "transactions": DEFAULT_TRANSACTIONS,
                "budgets": DEFAULT_BUDGETS,
                "investments": DEFAULT_INVESTMENTS,
                "goals": DEFAULT_GOALS,
                "tasks": DEFAULT_TASKS
            }
            
    def save_database(self, data=None):
        if data is None:
            data = self.db
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def calculate_aggregates(self):
        income = sum(t["amount"] for t in self.db["transactions"] if t["type"] == "Income")
        expense = sum(t["amount"] for t in self.db["transactions"] if t["type"] == "Expense")
        savings = income - expense
        invested = sum(inv["investedValue"] for inv in self.db["investments"])
        current = sum(inv["currentValue"] for inv in self.db["investments"])
        net_worth = savings + current
        return income, expense, savings, invested, current, net_worth

    # ==================== TAB 1: FINANCIAL BOARD ====================
    def create_dashboard_tab(self):
        tab = tk.Frame(self.notebook, bg="#f8fafc")
        self.notebook.add(tab, text=" Financial Board ")
        
        # KPI Row
        kpi_frame = tk.Frame(tab, bg="#f8fafc")
        kpi_frame.pack(fill="x", pady=10)
        
        inc, exp, sav, _, _, nw = self.calculate_aggregates()
        
        self.kpi_widgets = {}
        kpis = [
            ("Monthly Inflows", inc, "#10b981", 0),
            ("Monthly Outflows", exp, "#ef4444", 1),
            ("Net Cashflow", sav, "#6366f1", 2),
            ("Net Assets Worth", nw, "#4f46e5", 3)
        ]
        
        for title, val, color, col_idx in kpis:
            f = tk.Frame(kpi_frame, bg="#ffffff", bd=1, relief="solid", highlightthickness=0)
            f.config(highlightbackground="#e2e8f0", highlightcolor="#e2e8f0")
            f.grid(row=0, column=col_idx, padx=10, sticky="nsew")
            kpi_frame.grid_columnconfigure(col_idx, weight=1)
            
            tk.Label(f, text=title.upper(), font=("Helvetica", 9, "bold"), bg="#ffffff", fg="#64748b").pack(anchor="w", padx=15, pady=(10, 2))
            lbl = tk.Label(f, text=f"{self.currency}{val:,.2f}", font=("Courier", 16, "bold"), bg="#ffffff", fg=color)
            lbl.pack(anchor="w", padx=15, pady=(0, 10))
            self.kpi_widgets[title] = lbl
            
        # Lower Content split
        lower_frame = tk.Frame(tab, bg="#f8fafc")
        lower_frame.pack(fill="both", expand=True, pady=10)
        
        # Ledger table frame
        ledger_frame = tk.LabelFrame(lower_frame, text=" Recent Financial Ledger Book ", bg="#ffffff", font=("Helvetica", 11, "bold"), fg="#1e293b", padx=15, pady=15)
        ledger_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        # Scrollable Treeview
        tree_scroll = ttk.Scrollbar(ledger_frame)
        tree_scroll.pack(side="right", fill="y")
        
        self.tx_tree = ttk.Treeview(ledger_frame, columns=("date", "desc", "cat", "type", "amount"), show="headings", yscrollcommand=tree_scroll.set)
        self.tx_tree.pack(fill="both", expand=True)
        tree_scroll.config(command=self.tx_tree.yview)
        
        self.tx_tree.heading("date", text="Date")
        self.tx_tree.heading("desc", text="Description")
        self.tx_tree.heading("cat", text="Category")
        self.tx_tree.heading("type", text="Type")
        self.tx_tree.heading("amount", text="Amount")
        
        self.tx_tree.column("date", width=90, anchor="center")
        self.tx_tree.column("desc", width=200, anchor="w")
        self.tx_tree.column("cat", width=100, anchor="center")
        self.tx_tree.column("type", width=80, anchor="center")
        self.tx_tree.column("amount", width=100, anchor="e")
        
        self.populate_tx_tree()
        
        # Form frame
        form_frame = tk.LabelFrame(lower_frame, text=" Record Flow Entry ", bg="#ffffff", font=("Helvetica", 11, "bold"), fg="#1e293b", padx=15, pady=15)
        form_frame.pack(side="right", fill="both", padx=10)
        
        tk.Label(form_frame, text="Description:", bg="#ffffff", fg="#475569").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_desc = tk.Entry(form_frame, width=22)
        self.ent_desc.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Amount:", bg="#ffffff", fg="#475569").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_amount = tk.Entry(form_frame, width=22)
        self.ent_amount.grid(row=1, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Flow Type:", bg="#ffffff", fg="#475569").grid(row=2, column=0, sticky="w", pady=5)
        self.cmb_type = ttk.Combobox(form_frame, values=["Expense", "Income"], width=20, state="readonly")
        self.cmb_type.set("Expense")
        self.cmb_type.grid(row=2, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Category:", bg="#ffffff", fg="#475569").grid(row=3, column=0, sticky="w", pady=5)
        self.ent_cat = tk.Entry(form_frame, width=22)
        self.ent_cat.grid(row=3, column=1, pady=5, padx=5)
        
        btn_add = tk.Button(form_frame, text="Record Entry", bg="#4f46e5", fg="#ffffff", font=("Helvetica", 10, "bold"), command=self.add_transaction)
        btn_add.grid(row=4, column=0, columnspan=2, pady=20)
        
    def populate_tx_tree(self):
        self.tx_tree.delete(*self.tx_tree.get_children())
        for tx in self.db["transactions"]:
            self.tx_tree.insert("", "end", values=(tx["date"], tx["description"], tx["category"], tx["type"], f"{self.currency}{tx['amount']:,.2f}"))

    def add_transaction(self):
        desc = self.ent_desc.get().strip()
        amt_str = self.ent_amount.get().strip()
        f_type = self.cmb_type.get()
        cat = self.ent_cat.get().strip()
        
        if not desc or not amt_str or not cat:
            messagebox.showerror("Error", "Please fill in all transaction details.")
            return
        try:
            amt = float(amt_str)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric amount.")
            return
            
        new_tx = {
            "id": f"tx_{int(datetime.datetime.now().timestamp())}",
            "userId": self.db["user"]["id"],
            "description": desc,
            "amount": amt,
            "category": cat,
            "type": f_type,
            "date": str(datetime.date.today())
        }
        
        self.db["transactions"].insert(0, new_tx)
        self.save_database()
        
        # Clear fields
        self.ent_desc.delete(0, tk.END)
        self.ent_amount.delete(0, tk.END)
        self.ent_cat.delete(0, tk.END)
        
        # Refresh widgets
        self.populate_tx_tree()
        self.refresh_kpis()
        self.refresh_budgets_tab()
        messagebox.showinfo("Success", "Transaction recorded and logged successfully.")

    def refresh_kpis(self):
        inc, exp, sav, _, _, nw = self.calculate_aggregates()
        self.kpi_widgets["Monthly Inflows"].config(text=f"{self.currency}{inc:,.2f}")
        self.kpi_widgets["Monthly Outflows"].config(text=f"{self.currency}{exp:,.2f}")
        self.kpi_widgets["Net Cashflow"].config(text=f"{self.currency}{sav:,.2f}")
        self.kpi_widgets["Net Assets Worth"].config(text=f"{self.currency}{nw:,.2f}")

    # ==================== TAB 2: BUDGETS & EXPENSES ====================
    def create_budgets_tab(self):
        self.budget_tab = tk.Frame(self.notebook, bg="#f8fafc")
        self.notebook.add(self.budget_tab, text=" Budgets & Thresholds ")
        
        # Splitting Left (List) and Right (Set Form)
        self.b_left = tk.Frame(self.budget_tab, bg="#f8fafc")
        self.b_left.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        self.b_right = tk.LabelFrame(self.budget_tab, text=" Configure Allocation ", bg="#ffffff", font=("Helvetica", 11, "bold"), fg="#1e293b", padx=15, pady=15)
        self.b_right.pack(side="right", fill="both", padx=10, pady=10)
        
        # Build set budget form inside b_right
        tk.Label(self.b_right, text="Category Name:", bg="#ffffff", fg="#475569").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_b_cat = tk.Entry(self.b_right, width=22)
        self.ent_b_cat.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(self.b_right, text="Limit Amount:", bg="#ffffff", fg="#475569").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_b_amount = tk.Entry(self.b_right, width=22)
        self.ent_b_amount.grid(row=1, column=1, pady=5, padx=5)
        
        btn_set_b = tk.Button(self.b_right, text="Set Budget Limit", bg="#4f46e5", fg="#ffffff", font=("Helvetica", 10, "bold"), command=self.set_budget_limit)
        btn_set_b.grid(row=2, column=0, columnspan=2, pady=20)
        
        self.refresh_budgets_tab()
        
    def refresh_budgets_tab(self):
        # Clear left frame
        for widget in self.b_left.winfo_children():
            widget.destroy()
            
        tk.Label(self.b_left, text="Active Budget Threshold Progress", font=("Helvetica", 13, "bold"), bg="#f8fafc", fg="#0f172a").pack(anchor="w", pady=(0, 15))
        
        # Calculate spent per category
        expense_by_cat = {}
        for t in self.db["transactions"]:
            if t["type"] == "Expense":
                expense_by_cat[t["category"]] = expense_by_cat.get(t["category"], 0) + t["amount"]
                
        for budget in self.db["budgets"]:
            cat = budget["category"]
            limit = budget["amount"]
            spent = expense_by_cat.get(cat, 0)
            percentage = (spent / limit) * 100 if limit > 0 else 0
            
            card = tk.Frame(self.b_left, bg="#ffffff", bd=1, relief="solid", highlightthickness=0)
            card.config(highlightbackground="#e2e8f0")
            card.pack(fill="x", pady=5)
            
            lbl_info = tk.Label(card, text=f"Category: {cat.upper()}", font=("Helvetica", 10, "bold"), bg="#ffffff", fg="#334155")
            lbl_info.pack(side="left", padx=15, pady=10)
            
            # Progress display
            progress_bar = ttk.Progressbar(card, length=200, mode="determinate")
            progress_bar.pack(side="left", padx=15, pady=10)
            progress_bar['value'] = min(percentage, 100)
            
            lbl_spent = tk.Label(card, text=f"Spent: {self.currency}{spent:,.0f} / {self.currency}{limit:,.0f} ({percentage:.1f}%)", font=("Courier", 10, "bold"), bg="#ffffff", fg="#4f46e5" if percentage < 85 else "#ef4444")
            lbl_spent.pack(side="right", padx=15, pady=10)
            
    def set_budget_limit(self):
        cat = self.ent_b_cat.get().strip()
        amt_str = self.ent_b_amount.get().strip()
        
        if not cat or not amt_str:
            messagebox.showerror("Error", "Please specify both the Category and Budget limit amount.")
            return
        try:
            amt = float(amt_str)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid budget threshold numeric amount.")
            return
            
        # Update or append
        idx = -1
        for i, b in enumerate(self.db["budgets"]):
            if b["category"].lower() == cat.lower():
                idx = i
                break
                
        if idx > -1:
            self.db["budgets"][idx]["amount"] = amt
        else:
            self.db["budgets"].append({
                "id": f"b_{int(datetime.datetime.now().timestamp())}",
                "userId": self.db["user"]["id"],
                "category": cat,
                "amount": amt,
                "month": "2026-07"
            })
            
        self.save_database()
        self.ent_b_cat.delete(0, tk.END)
        self.ent_b_amount.delete(0, tk.END)
        self.refresh_budgets_tab()
        messagebox.showinfo("Success", f"Budget limit updated successfully for category '{cat}'.")

    # ==================== TAB 3: INVESTMENTS ====================
    def create_investments_tab(self):
        tab = tk.Frame(self.notebook, bg="#f8fafc")
        self.notebook.add(tab, text=" Investment Portfolio ")
        
        # Portfolio stats summary
        summary_frame = tk.Frame(tab, bg="#f8fafc")
        summary_frame.pack(fill="x", pady=10)
        
        _, _, _, invested, current, returns = self.calculate_aggregates()
        returns_pct = (returns / invested * 100) if invested > 0 else 0
        
        self.lbl_inv_sum = tk.Label(summary_frame, text=f"Invested Capital: {self.currency}{invested:,.2f}  |  Portfolio Value: {self.currency}{current:,.2f}  |  Returns: {self.currency}{returns:,.2f} ({returns_pct:.2f}%)", font=("Helvetica", 12, "bold"), bg="#ffffff", fg="#4f46e5", pady=12, bd=1, relief="solid")
        self.lbl_inv_sum.pack(fill="x", padx=10)
        
        # Holdings split
        holdings_box = tk.LabelFrame(tab, text=" Investment Holdings Portfolio Ledger ", bg="#ffffff", font=("Helvetica", 11, "bold"), fg="#1e293b", padx=15, pady=15)
        holdings_box.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollable table
        inv_scroll = ttk.Scrollbar(holdings_box)
        inv_scroll.pack(side="right", fill="y")
        
        self.inv_tree = ttk.Treeview(holdings_box, columns=("sym", "name", "units", "buy", "curr", "invested", "current", "returns"), show="headings", yscrollcommand=inv_scroll.set)
        self.inv_tree.pack(fill="both", expand=True)
        inv_scroll.config(command=self.inv_tree.yview)
        
        self.inv_tree.heading("sym", text="Symbol")
        self.inv_tree.heading("name", text="Asset Name")
        self.inv_tree.heading("units", text="Units")
        self.inv_tree.heading("buy", text="Buy Price")
        self.inv_tree.heading("curr", text="Current Price")
        self.inv_tree.heading("invested", text="Invested Value")
        self.inv_tree.heading("current", text="Current Value")
        self.inv_tree.heading("returns", text="ROI %")
        
        self.inv_tree.column("sym", width=80, anchor="center")
        self.inv_tree.column("name", width=180, anchor="w")
        self.inv_tree.column("units", width=70, anchor="center")
        self.inv_tree.column("buy", width=90, anchor="e")
        self.inv_tree.column("curr", width=90, anchor="e")
        self.inv_tree.column("invested", width=110, anchor="e")
        self.inv_tree.column("current", width=110, anchor="e")
        self.inv_tree.column("returns", width=80, anchor="center")
        
        self.populate_inv_tree()
        
    def populate_inv_tree(self):
        self.inv_tree.delete(*self.inv_tree.get_children())
        for inv in self.db["investments"]:
            self.inv_tree.insert("", "end", values=(
                inv["symbol"],
                inv["name"],
                inv["units"],
                f"{self.currency}{inv['purchasePrice']:,.2f}",
                f"{self.currency}{inv['currentPrice']:,.2f}",
                f"{self.currency}{inv['investedValue']:,.2f}",
                f"{self.currency}{inv['currentValue']:,.2f}",
                f"{inv['returnsPercent']}%"
            ))

    # ==================== TAB 4: SAVINGS GOALS ====================
    def create_goals_tab(self):
        self.goals_tab = tk.Frame(self.notebook, bg="#f8fafc")
        self.notebook.add(self.goals_tab, text=" Savings Goals ")
        self.refresh_goals_tab()
        
    def refresh_goals_tab(self):
        for widget in self.goals_tab.winfo_children():
            widget.destroy()
            
        tk.Label(self.goals_tab, text="Active Life Saving Goals Progress", font=("Helvetica", 14, "bold"), bg="#f8fafc", fg="#0f172a").pack(anchor="w", pady=(5, 15), padx=10)
        
        for idx, goal in enumerate(self.db["goals"]):
            progress = (goal["currentAmount"] / goal["targetAmount"]) if goal["targetAmount"] > 0 else 0
            deficit = max(goal["targetAmount"] - goal["currentAmount"], 0)
            
            card = tk.LabelFrame(self.goals_tab, text=f" 🎯 {goal['title']} ", font=("Helvetica", 11, "bold"), bg="#ffffff", fg="#4f46e5", padx=15, pady=12)
            card.pack(fill="x", padx=10, pady=6)
            
            p_bar = ttk.Progressbar(card, length=300, mode="determinate")
            p_bar.pack(side="left", padx=15)
            p_bar['value'] = min(progress * 100, 100)
            
            tk.Label(card, text=f"Saved: {self.currency}{goal['currentAmount']:,.0f} / {self.currency}{goal['targetAmount']:,.0f}", font=("Courier", 10, "bold"), bg="#ffffff", fg="#334155").pack(side="left", padx=15)
            tk.Label(card, text=f"Deficit Remaining: {self.currency}{deficit:,.0f}", font=("Helvetica", 10, "bold"), bg="#ffffff", fg="#ef4444" if deficit > 0 else "#10b981").pack(side="left", padx=15)
            
            # Action frame inside card
            act_frame = tk.Frame(card, bg="#ffffff")
            act_frame.pack(side="right", padx=10)
            
            # Contribution entry and button
            ent = tk.Entry(act_frame, width=10)
            ent.pack(side="left", padx=5)
            ent.insert(0, "15000")
            
            btn = tk.Button(act_frame, text="Contribute", bg="#10b981", fg="#ffffff", font=("Helvetica", 9, "bold"), command=lambda i=idx, e=ent: self.contribute_to_goal(i, e))
            btn.pack(side="left", padx=5)

    def contribute_to_goal(self, index, entry_widget):
        val_str = entry_widget.get().strip()
        try:
            val = float(val_str)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric value.")
            return
            
        self.db["goals"][index]["currentAmount"] += val
        if self.db["goals"][index]["currentAmount"] >= self.db["goals"][index]["targetAmount"]:
            self.db["goals"][index]["status"] = "Completed"
            
        self.save_database()
        self.refresh_goals_tab()
        self.refresh_kpis()
        messagebox.showinfo("Success", "Contribution logged successfully!")

    # ==================== TAB 5: PROJECT MILESTONES ====================
    def create_milestones_tab(self):
        self.milestones_tab = tk.Frame(self.notebook, bg="#f8fafc")
        self.notebook.add(self.milestones_tab, text=" Project Milestones ")
        self.refresh_milestones_tab()
        
    def refresh_milestones_tab(self):
        for widget in self.milestones_tab.winfo_children():
            widget.destroy()
            
        tk.Label(self.milestones_tab, text="FinSight Deliverables Release Tracker", font=("Helvetica", 14, "bold"), bg="#f8fafc", fg="#0f172a").pack(anchor="w", pady=(5, 15), padx=10)
        
        m1_frame = tk.LabelFrame(self.milestones_tab, text=" Milestone 1: Core Release ", font=("Helvetica", 11, "bold"), bg="#ffffff", fg="#1e293b", padx=15, pady=12)
        m1_frame.pack(fill="x", padx=10, pady=8)
        
        m2_frame = tk.LabelFrame(self.milestones_tab, text=" Milestone 2: Production Stability Release ", font=("Helvetica", 11, "bold"), bg="#ffffff", fg="#1e293b", padx=15, pady=12)
        m2_frame.pack(fill="x", padx=10, pady=8)
        
        for idx, task in enumerate(self.db["tasks"]):
            target_frame = m1_frame if task["milestone"] == "Milestone 1" else m2_frame
            
            t_row = tk.Frame(target_frame, bg="#ffffff")
            t_row.pack(fill="x", pady=4)
            
            indicator = "🟢" if task["status"] == "Completed" else "🟡" if task["status"] == "In Progress" else "🔴"
            tk.Label(t_row, text=f"{indicator} {task['title']}", font=("Helvetica", 10), bg="#ffffff", fg="#334155").pack(side="left", padx=10)
            
            btn = tk.Button(t_row, text=f"Cycle: {task['status']}", bg="#e2e8f0", fg="#334155", font=("Helvetica", 8, "bold"), command=lambda i=idx: self.cycle_task_status(i))
            btn.pack(side="right", padx=10)
            
        # Reset Milestones
        btn_reset = tk.Button(self.milestones_tab, text="Reset Milestones", bg="#64748b", fg="#ffffff", font=("Helvetica", 10, "bold"), command=self.reset_milestones)
        btn_reset.pack(anchor="e", padx=15, pady=15)

    def cycle_task_status(self, index):
        curr = self.db["tasks"][index]["status"]
        nxt = "In Progress" if curr == "Todo" else "Completed" if curr == "In Progress" else "Todo"
        self.db["tasks"][index]["status"] = nxt
        self.save_database()
        self.refresh_milestones_tab()

    def reset_milestones(self):
        self.db["tasks"] = DEFAULT_TASKS
        self.save_database()
        self.refresh_milestones_tab()
        messagebox.showinfo("Success", "Project deliverables reset to initial milestone standards.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinSightApp(root)
    root.mainloop()
