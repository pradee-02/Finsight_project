import os
import json
import datetime
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="FinSight - Finance & Investment Intelligence",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants & Default Data (Matches React data structures)
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


# Helper functions for data management
def load_database():
    if not os.path.exists(DATA_FILE):
        data = {
            "user": DEFAULT_USER,
            "transactions": DEFAULT_TRANSACTIONS,
            "budgets": DEFAULT_BUDGETS,
            "investments": DEFAULT_INVESTMENTS,
            "goals": DEFAULT_GOALS,
            "tasks": DEFAULT_TASKS
        }
        save_database(data)
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

def save_database(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Initialize Session State
if "db" not in st.session_state:
    st.session_state.db = load_database()

db = st.session_state.db
user = db["user"]
currency = user["currency"]

# Apply cohesive Styling
st.markdown("""
<style>
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
    }
    .metric-header {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #0f172a;
        font-family: monospace;
    }
    .stApp {
        background-color: #f8fafc;
    }
</style>
""", unsafe_allow_html=True)

# SIDEBAR NAVIGATION
with st.sidebar:
    st.image(user["avatarUrl"], width=80)
    st.subheader(user["name"])
    st.caption(f"💼 {user['role']}")
    st.write("---")
    
    navigation = st.radio(
        "Navigation Menu",
        ["Financial Board", "Budgets & Expenses", "Investment Portfolio", "Savings Goals", "Project Milestones"],
        index=0
    )
    
    st.write("---")
    st.caption("⚙️ Profile Preferences")
    email_notify = st.checkbox("Email Alerts Enabled", value=user["preferences"]["emailNotifications"])
    budget_alert = st.checkbox("Budget Warnings Enabled", value=user["preferences"]["budgetAlerts"])
    
    # Sync settings on toggle
    if (email_notify != user["preferences"]["emailNotifications"] or 
        budget_alert != user["preferences"]["budgetAlerts"]):
        db["user"]["preferences"]["emailNotifications"] = email_notify
        db["user"]["preferences"]["budgetAlerts"] = budget_alert
        save_database(db)

# Compute Global Financial Aggregates
total_income = sum(t["amount"] for t in db["transactions"] if t["type"] == "Income")
total_expense = sum(t["amount"] for t in db["transactions"] if t["type"] == "Expense")
net_savings = total_income - total_expense
total_invested = sum(inv["investedValue"] for inv in db["investments"])
total_current = sum(inv["currentValue"] for inv in db["investments"])
portfolio_gains = total_current - total_invested
portfolio_returns_pct = (portfolio_gains / total_invested * 100) if total_invested > 0 else 0

available_liquidity = net_savings + total_current

# APP TITLE HEADER
st.title("FinSight Intelligent Workspace 📊")
st.write(f"Comprehensive finance tracking and project roadmap architecture for **{user['name']}**.")

# 1. FINANCIAL BOARD PAGE
if navigation == "Financial Board":
    st.header("Financial Clarity Board")
    
    # KPI metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">Total Monthly Inflows</div>
            <div class="metric-value">{currency}{total_income:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">Total Outflows</div>
            <div class="metric-value" style="color: #ef4444;">{currency}{total_expense:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">Net Monthly Cashflow</div>
            <div class="metric-value" style="color: #10b981;">{currency}{net_savings:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">Total Capital Net-Worth</div>
            <div class="metric-value" style="color: #6366f1;">{currency}{available_liquidity:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    # Core Charts Section
    chart_col1, chart_col2 = st.columns([3, 2])
    
    with chart_col1:
        st.subheader("Financial Volume Trend & Cumulative Surplus")
        # Generate line graph data
        df_tx = pd.DataFrame(db["transactions"])
        df_tx['date'] = pd.to_datetime(df_tx['date'])
        df_tx = df_tx.sort_values('date')
        
        cumulative_balance = []
        balance = 0
        dates = []
        for index, row in df_tx.iterrows():
            if row['type'] == 'Income':
                balance += row['amount']
            else:
                balance -= row['amount']
            cumulative_balance.append(balance)
            dates.append(row['date'])
            
        trend_df = pd.DataFrame({"Date": dates, "Cumulative Liquidity": cumulative_balance})
        fig_trend = px.area(trend_df, x="Date", y="Cumulative Liquidity", 
                            color_discrete_sequence=["rgba(99, 102, 241, 0.2)"],
                            title="Day-by-Day Capital Aggregation")
        fig_trend.update_traces(line_color="#6366f1", line_width=2.5)
        fig_trend.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                                margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_trend, use_container_width=True)

    with chart_col2:
        st.subheader("Outflow Allocation distribution")
        expenses_only = [t for t in db["transactions"] if t["type"] == "Expense"]
        if expenses_only:
            df_exp = pd.DataFrame(expenses_only)
            fig_pie = px.pie(df_exp, values="amount", names="category", hole=0.4,
                             color_discrete_sequence=px.colors.sequential.Indigo,
                             title="Expense Outflows by Category")
            fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No expense data found to plot category layout.")

    # Transactions list and add transaction form
    st.write("---")
    list_col, form_col = st.columns([3, 2])
    
    with list_col:
        st.subheader("Recent Ledger Book")
        # Search & Filter
        search_query = st.text_input("🔍 Search Description...", "")
        filter_cat = st.selectbox("Category Filter", ["All"] + list(set(t["category"] for t in db["transactions"])))
        
        filtered_tx = db["transactions"]
        if search_query:
            filtered_tx = [t for t in filtered_tx if search_query.lower() in t["description"].lower()]
        if filter_cat != "All":
            filtered_tx = [t for t in filtered_tx if t["category"] == filter_cat]
            
        df_display = pd.DataFrame(filtered_tx)[["date", "description", "category", "type", "amount"]]
        st.dataframe(df_display, use_container_width=True)
        
    with form_col:
        st.subheader("➕ Record Inflow / Outflow")
        with st.form("add_tx_form", clear_on_submit=True):
            tx_desc = st.text_input("Transaction Description", placeholder="e.g. Server hosting, Consulting fees")
            tx_amount = st.number_input("Amount", min_value=1.0, value=5000.0)
            tx_type = st.selectbox("Type", ["Expense", "Income"])
            tx_cat = st.text_input("Category", placeholder="e.g. Software, Consulting, Rent, Travel")
            tx_date = st.date_input("Date", datetime.date.today())
            
            submit = st.form_submit_button("Record Transaction")
            if submit:
                if tx_desc and tx_cat:
                    new_tx = {
                        "id": f"tx_{int(datetime.datetime.now().timestamp())}",
                        "userId": user["id"],
                        "description": tx_desc,
                        "amount": float(tx_amount),
                        "category": tx_cat,
                        "type": tx_type,
                        "date": str(tx_date)
                    }
                    db["transactions"].insert(0, new_tx)
                    save_database(db)
                    st.success("Transaction recorded and database updated successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all the required transaction details.")

# 2. BUDGETS & EXPENSES PAGE
elif navigation == "Budgets & Expenses":
    st.header("Expense Architecture & Budget Thresholds")
    
    st.write("Establish spending control limits per category and track real-time utilization. Generates real-time alerts if transactions break thresholds.")
    
    # Calculate utilization
    expense_by_cat = {}
    for t in db["transactions"]:
        if t["type"] == "Expense":
            expense_by_cat[t["category"]] = expense_by_cat.get(t["category"], 0) + t["amount"]
            
    # Display Budgets
    st.subheader("Budget Threshold Tracking")
    
    col_bud1, col_bud2 = st.columns([2, 1])
    
    with col_bud1:
        for budget in db["budgets"]:
            cat = budget["category"]
            limit = budget["amount"]
            spent = expense_by_cat.get(cat, 0)
            percentage = (spent / limit) * 100 if limit > 0 else 0
            
            # Progress bar colors based on warning threshold
            progress_color = "green"
            if percentage >= 100:
                progress_color = "red"
            elif percentage >= 80:
                progress_color = "orange"
                
            st.markdown(f"**Category: {cat}**")
            col_b1, col_b2, col_b3 = st.columns([3, 1, 1])
            with col_b1:
                st.progress(min(percentage / 100.0, 1.0))
            with col_b2:
                st.write(f"Spent: {currency}{spent:,.0f} / {currency}{limit:,.0f}")
            with col_b3:
                st.write(f"**{percentage:.1f}%**")
                
            if percentage >= 100:
                st.error(f"🚨 **THRESHOLD BREACHED:** {cat} budget has exceeded allocation limit by {currency}{spent-limit:,.0f}!")
            elif percentage >= 80:
                st.warning(f"⚠️ **LIMIT ALERT:** Spent over 80% of allocated budget on {cat}!")
                
            st.write("---")
            
    with col_bud2:
        st.subheader("⚙️ Configure Allocations")
        with st.form("set_budget_form"):
            b_cat = st.selectbox("Category select", list(set(t["category"] for t in db["transactions"] if t["type"] == "Expense")) + ["Other"])
            b_cat_custom = st.text_input("Or type new Category", "")
            final_b_cat = b_cat_custom if b_cat_custom else b_cat
            b_amount = st.number_input("Limit Budget Allocation", min_value=100.0, value=15000.0)
            
            b_submit = st.form_submit_button("Set Limit")
            if b_submit:
                # Find if budget category already exists
                idx = -1
                for i, b in enumerate(db["budgets"]):
                    if b["category"] == final_b_cat:
                        idx = i
                        break
                        
                if idx > -1:
                    db["budgets"][idx]["amount"] = float(b_amount)
                else:
                    db["budgets"].append({
                        "id": f"b_{int(datetime.datetime.now().timestamp())}",
                        "userId": user["id"],
                        "category": final_b_cat,
                        "amount": float(b_amount),
                        "month": "2026-07"
                    })
                save_database(db)
                st.success(f"Budget limit for {final_b_cat} set to {currency}{b_amount:,.0f} successfully.")
                st.rerun()

# 3. INVESTMENT PORTFOLIO PAGE
elif navigation == "Investment Portfolio":
    st.header("Investments Portfolio Analysis")
    
    col_inv1, col_inv2, col_inv3 = st.columns(3)
    with col_inv1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">Invested Capital</div>
            <div class="metric-value">{currency}{total_invested:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_inv2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">Current Portfolio Valuation</div>
            <div class="metric-value" style="color: #6366f1;">{currency}{total_current:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_inv3:
        returns_color = "#10b981" if portfolio_gains >= 0 else "#ef4444"
        sign = "+" if portfolio_gains >= 0 else ""
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">Net Gains / ROI %</div>
            <div class="metric-value" style="color: {returns_color};">{currency}{sign}{portfolio_gains:,.2f} ({sign}{portfolio_returns_pct:.2f}%)</div>
        </div>
        """, unsafe_allow_html=True)

    inv_chart_col1, inv_chart_col2 = st.columns([1, 1])
    
    with inv_chart_col1:
        st.subheader("Asset Allocation Chart")
        df_inv = pd.DataFrame(db["investments"])
        if not df_inv.empty:
            fig_alloc = px.pie(df_inv, values="currentValue", names="category", hole=0.5,
                               color_discrete_sequence=px.colors.sequential.Mint,
                               title="Current Capital Allocation")
            fig_alloc.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_alloc, use_container_width=True)
            
    with inv_chart_col2:
        st.subheader("Relative Asset Yield (ROI %)")
        if not df_inv.empty:
            fig_yield = px.bar(df_inv, x="symbol", y="returnsPercent", color="returnsPercent",
                               color_continuous_scale="Viridis",
                               labels={"returnsPercent": "ROI (%)", "symbol": "Symbol"},
                               title="ROI Comparison by Asset")
            fig_yield.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_yield, use_container_width=True)

    # Investment listings
    st.subheader("Portfolio Holdings Ledger")
    st.dataframe(df_inv[["symbol", "name", "units", "purchasePrice", "currentPrice", "investedValue", "currentValue", "returnsValue", "returnsPercent"]], use_container_width=True)
    
    # Add new holdings
    st.write("---")
    st.subheader("💼 Record New Asset Acquisition")
    with st.form("add_inv_form", clear_on_submit=True):
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            inv_symbol = st.text_input("Asset Ticker/Symbol", placeholder="e.g. TCS, GOOG")
            inv_name = st.text_input("Asset Name", placeholder="e.g. Tata Consultancy, Google LLC")
        with col_f2:
            inv_units = st.number_input("Acquired Units", min_value=0.01, value=10.0)
            inv_buy = st.number_input("Purchase Price Per Unit", min_value=0.1, value=1200.0)
        with col_f3:
            inv_curr = st.number_input("Current Valuation Price Per Unit", min_value=0.1, value=1300.0)
            inv_cat = st.selectbox("Asset Category", ["Equity", "Mutual Funds", "Bonds", "Crypto", "Commodities", "Real Estate"])
            
        submit_inv = st.form_submit_button("Record Capital Holding")
        if submit_inv:
            if inv_symbol and inv_name:
                invested = inv_units * inv_buy
                current = inv_units * inv_curr
                returns_val = current - invested
                returns_pct = (returns_val / invested * 100) if invested > 0 else 0
                
                new_asset = {
                    "id": f"inv_{int(datetime.datetime.now().timestamp())}",
                    "userId": user["id"],
                    "symbol": inv_symbol.upper(),
                    "name": inv_name,
                    "units": float(inv_units),
                    "purchasePrice": float(inv_buy),
                    "currentPrice": float(inv_curr),
                    "category": inv_cat,
                    "investedValue": invested,
                    "currentValue": current,
                    "returnsValue": returns_val,
                    "returnsPercent": round(returns_pct, 2)
                }
                db["investments"].append(new_asset)
                save_database(db)
                st.success(f"Asset {inv_symbol.upper()} recorded successfully!")
                st.rerun()

# 4. SAVINGS GOALS PAGE
elif navigation == "Savings Goals":
    st.header("Financial Goal Mileposts")
    st.write("Structure savings paths for life goals, track current accumulations, and analyze deficits.")
    
    # Active Goals Loop
    for idx, goal in enumerate(db["goals"]):
        progress = (goal["currentAmount"] / goal["targetAmount"]) if goal["targetAmount"] > 0 else 0
        deficit = max(goal["targetAmount"] - goal["currentAmount"], 0)
        
        st.markdown(f"### 🎯 {goal['title']}")
        col_g1, col_g2, col_g3 = st.columns([3, 1, 1])
        with col_g1:
            st.progress(min(progress, 1.0))
            st.write(f"Deficit remaining: **{currency}{deficit:,.2f}**")
        with col_g2:
            st.write(f"Accumulated: **{currency}{goal['currentAmount']:,.0f}** / **{currency}{goal['targetAmount']:,.0f}**")
        with col_g3:
            st.write(f"Target Date: **{goal['targetDate']}**")
            st.write(f"Status: **{goal['status']}**")
            
        # Inline contribution form
        with st.expander(f"Modify Contributions / Log Progress for {goal['title']}"):
            contrib_col, action_col = st.columns([2, 1])
            with contrib_col:
                add_amt = st.number_input("Contribution Amount", min_value=1.0, value=10000.0, key=f"amt_{goal['id']}")
            with action_col:
                contrib_sub = st.button("Log Contribution", key=f"sub_{goal['id']}")
                if contrib_sub:
                    db["goals"][idx]["currentAmount"] += add_amt
                    if db["goals"][idx]["currentAmount"] >= db["goals"][idx]["targetAmount"]:
                        db["goals"][idx]["status"] = "Completed"
                    save_database(db)
                    st.success("Contribution recorded!")
                    st.rerun()
                    
                delete_g = st.button("Delete Goal", key=f"del_{goal['id']}")
                if delete_g:
                    db["goals"].pop(idx)
                    save_database(db)
                    st.success("Goal deleted.")
                    st.rerun()
                    
        st.write("---")
        
    # Create new Goal form
    st.subheader("➕ Create Custom Financial Goal")
    with st.form("new_goal_form", clear_on_submit=True):
        col_go1, col_go2 = st.columns(2)
        with col_go1:
            go_title = st.text_input("Goal Milestone Title", placeholder="e.g. Buy electric vehicle, Downpayment")
            go_target = st.number_input("Target Amount Required", min_value=1.0, value=250000.0)
        with col_go2:
            go_curr = st.number_input("Current Starting Balance", min_value=0.0, value=10000.0)
            go_date = st.date_input("Target Completion Date", datetime.date.today() + datetime.timedelta(days=365))
            
        go_submit = st.form_submit_button("Establish Saving Goal")
        if go_submit:
            if go_title:
                new_g = {
                    "id": f"g_{int(datetime.datetime.now().timestamp())}",
                    "userId": user["id"],
                    "title": go_title,
                    "targetAmount": float(go_target),
                    "currentAmount": float(go_curr),
                    "targetDate": str(go_date),
                    "category": "Custom",
                    "status": "Completed" if go_curr >= go_target else "In Progress"
                }
                db["goals"].append(new_g)
                save_database(db)
                st.success(f"Goal '{go_title}' created!")
                st.rerun()

# 5. PROJECT MILESTONES PAGE
elif navigation == "Project Milestones":
    st.header("Milestone Integration Tracker")
    st.write("Review development status of FinSight dashboard releases (Milestones 1 & 2) and coordinate deliverables.")
    
    # Metrics
    tot_tasks = len(db["tasks"])
    done_tasks = len([t for t in db["tasks"] if t["status"] == "Completed"])
    progress_tasks = (done_tasks / tot_tasks * 100) if tot_tasks > 0 else 0
    
    mcol1, mcol2 = st.columns(2)
    with mcol1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">Total Tasks Tracked</div>
            <div class="metric-value">{tot_tasks}</div>
        </div>
        """, unsafe_allow_html=True)
    with mcol2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">Completion Rate</div>
            <div class="metric-value" style="color: #10b981;">{progress_tasks:.1f}% ({done_tasks}/{tot_tasks})</div>
        </div>
        """, unsafe_allow_html=True)

    # Group tasks by Milestones
    m1_tasks = [t for t in db["tasks"] if t["milestone"] == "Milestone 1"]
    m2_tasks = [t for t in db["tasks"] if t["milestone"] == "Milestone 2"]
    
    st.subheader("Milestone 1: Core Dashboard Core Releases")
    for idx, t in enumerate(db["tasks"]):
        if t["milestone"] == "Milestone 1":
            # Show status with color indicators
            status_color = "🟢" if t["status"] == "Completed" else "🟡" if t["status"] == "In Progress" else "🔴"
            col_t1, col_t2 = st.columns([4, 1])
            with col_t1:
                st.write(f"{status_color} **{t['title']}** (Current: {t['status']})")
            with col_t2:
                btn_label = "Cycle Status"
                if st.button(btn_label, key=f"tsk_{t['id']}"):
                    # Todo -> In Progress -> Completed -> Todo
                    next_status = "In Progress" if t["status"] == "Todo" else "Completed" if t["status"] == "In Progress" else "Todo"
                    db["tasks"][idx]["status"] = next_status
                    save_database(db)
                    st.rerun()
                    
    st.write("---")
    st.subheader("Milestone 2: Persistency, Alerting, Security release")
    for idx, t in enumerate(db["tasks"]):
        if t["milestone"] == "Milestone 2":
            status_color = "🟢" if t["status"] == "Completed" else "🟡" if t["status"] == "In Progress" else "🔴"
            col_t1, col_t2 = st.columns([4, 1])
            with col_t1:
                st.write(f"{status_color} **{t['title']}** (Current: {t['status']})")
            with col_t2:
                btn_label = "Cycle Status"
                if st.button(btn_label, key=f"tsk_{t['id']}"):
                    next_status = "In Progress" if t["status"] == "Todo" else "Completed" if t["status"] == "In Progress" else "Todo"
                    db["tasks"][idx]["status"] = next_status
                    save_database(db)
                    st.rerun()

    st.write("---")
    if st.button("Reset Milestones to Defaults"):
        db["tasks"] = DEFAULT_TASKS
        save_database(db)
        st.success("Milestones reset successfully!")
        st.rerun()
