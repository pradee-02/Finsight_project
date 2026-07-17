# 💰 FinSight - Financial Intelligence Platform

FinSight is a comprehensive personal finance management platform developed to help users organize and monitor their financial activities. The application allows users to manage income, expenses, budgets, investments, savings goals, and financial reports through an intuitive and user-friendly interface.
📖 Table of Contents

- Overview
- Features
- Technology Stack
- Modules
- Project Structure
- Installation
- Running the Application
- Portfolio Calculations
- Future Enhancements
- Author

---

# 🌟 Overview

FinSight provides an integrated solution for managing personal finances. It enables users to record financial transactions, analyze spending habits, monitor investments, and generate meaningful financial insights using a centralized dashboard.

---

# 🚀 Features

- 🔐 Secure User Authentication
- 💸 Expense Management
- 💰 Income Tracking
- 📊 Budget Planning
- 📈 Wealth Portfolio Management
- 🎯 Savings Goal Tracking
- 🏦 Account Management
- 📑 Financial Reports
- 📊 Dashboard Analytics
- 📱 Responsive User Interface

---

# 💻 Technology Stack

## Frontend
- HTML5
- CSS3
- JavaScript
- TypeScript
- Vite

## Backend
- Python
- Flask

## Database
- Local JSON Database

## Version Control
- Git
- GitHub

---

# 📂 Modules

## 🏠 Dashboard
Displays an overview of the user's financial information including:
- Total Income
- Total Expenses
- Budget Summary
- Savings Progress
- Investment Portfolio

---

## 💸 Expense Management

Users can:
- Add expenses
- Edit expenses
- Delete expenses
- Categorize transactions
- View expense history

---

## 💰 Income Management

Allows users to:
- Record income
- Manage multiple income sources
- View income history

---

## 📊 Budget Management

Provides functionality to:
- Create monthly budgets
- Monitor spending
- Compare actual expenses with budget

---

## 📈 Wealth Portfolio Manager

Users can maintain investment records including:
- Stocks
- Cryptocurrencies
- Mutual Funds
- ETFs

Portfolio statistics include:
- Total Portfolio Value
- Total Invested Capital
- Current Returns
- Asset Allocation
- Asset Registry

---

## 🎯 Savings Goals

Users can:
- Create savings goals
- Set target amounts
- Monitor progress
- Track completion percentage

---

## 🏦 Account Management

Manage different financial accounts and available balances.

---

## 📑 Reports

Generate reports for:
- Income
- Expenses
- Budgets
- Investments
- Savings

---

# 📁 Project Structure

```
FinSight/
│
├── assets/
├── routes/
├── src/
├── static/
├── templates/
│
├── app.py
├── finsight.py
├── finsight_gui.py
├── finsight_streamlit.py
├── database.py
├── package.json
├── vite.config.ts
├── README.md
└── requirements.txt
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/your-username/FinSight.git
```

Move to the project directory

```bash
cd FinSight
```

Install Python dependencies

```bash
pip install -r requirements.txt
```

If a requirements file is unavailable, install Flask manually:

```bash
pip install flask
```

---

# ▶️ Running the Application

Run the application using:

```bash
python app.py
```

or

```bash
python finsight.py
```

Depending on your project's entry point.

Then open:

```
http://127.0.0.1:5000
```

---

# 📊 Portfolio Calculations

### Invested Value

```
Invested Value = Units Held × Acquisition Price
```

### Current Value

```
Current Value = Units Held × Current Price
```

### Gain/Loss

```
Gain/Loss = Current Value − Invested Value
```

### Total Invested Capital

```
Total Invested Capital = Sum of all Invested Values
```

### Total Portfolio Value

```
Total Portfolio Value = Sum of all Current Values
```

### Total Returns

```
Total Returns = Total Portfolio Value − Total Invested Capital
```

---

# 🔮 Future Enhancements

- Real-time stock and cryptocurrency market data
- AI-powered financial recommendations
- Data visualization using interactive charts
- Export reports as PDF and Excel
- Multi-currency support
- Email notifications and reminders
- Mobile application support

---

# 👨‍💻 Author

# PRADEEBA R S


**Project Title:** FinSight – Financial Intelligence Platform

---

# 📄 License

This project is developed for educational and academic purposes.
