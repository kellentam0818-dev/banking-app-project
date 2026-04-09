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
- Transfer and credit limit adjustment: Users can lower limits independently; only admins can increase limits. Requests exceeding maximum limits require stricter review.

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

## Project Update Log

### 2026-04-08 Update
✅ **Complete getter encapsulation for all classes (OOP encapsulation standard)**
- Centralized getter management for User class (get_user_id, get_daily_transfer_limit, etc.)
- Added get_balance() for Account parent class to avoid direct private property access
- Unified getter style for SavingsAccount / CheckingAccount
- Followed the enterprise-level specification of "private attributes first, unified getters later"
- Improved code security and maintainability

✅ **Implement salary disbursement business logic**
- Support batch salary payment to multiple employee accounts
- Automatically log each transfer (account, amount, status, timestamp)
- Balance check + security validation
- Return complete payment result list for reconciliation
- Clear code structure for future expansion

### 2026-04-09 Update
✅ **Implement Secure Password Hashing with bcrypt**
- Replaced plaintext password storage with industry-standard bcrypt hashing
- Added `set_password()` method with empty password validation and salted hashing
- Implemented `check_password()` method for secure password verification
- Updated `login()` flow to work with hashed passwords, maintaining all security checks
- Eliminated plaintext password storage risks, meeting financial security compliance
- Improved system security and data protection for user credentials



    
