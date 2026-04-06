# Banking App System
A Python-based object-oriented banking management system, designed for learning OOP, Git version control, and core banking business logic.

---

## 📋 Project Overview
This project implements a complete banking system with object-oriented design, covering user security control, multi-type account management, fund transactions, and shared credit limit for credit cards. It is a practice project for Python development and GitHub deployment.

---

## ✨ Core Features
### 1. User Management & Security
- User registration, login, and logout with password verification
- Account lock: 3 consecutive failed login attempts → 24-hour auto-lock
- Auto-logout: Log out automatically after 5 minutes of inactivity
- Daily transfer limit (default: $5000, configurable)
- Shared credit limit for all credit cards under the same user (default: $10000, configurable)

### 2. Multi-type Account Support
- **Savings Account**: Interest calculation (annual/monthly), monthly fee deduction
- **Checking Account**: Overdraft support with configurable overdraft limit
- **Credit Card Account**: Credit limit sharing, consumption & repayment with real-time limit update
- **High-Interest Savings**: Higher interest rate, $200,000 minimum balance requirement
- **Student Savings Account**: No monthly fee, preferential interest rate for students

### 3. Fund Operations
- Deposit, withdraw, and transfer between accounts (support cross-user transfer)
- Credit card consumption & repayment with balance and limit feedback
- Strict amount validation for all transactions (amount > 0)

### 4. Project Specification
- Complete `.gitignore` configuration to exclude unnecessary files
- Standard Git workflow for version control and GitHub deployment

---

## 🏗️ System Architecture
### Core Class Hierarchy






    
