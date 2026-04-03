# Banking APP Project
A simple banking application built with Python, demonstrating Object-Oriented Programming (OOP) concepts using Class and Subclass.

## Features
- User registration & login with password retry limit and auto-logout
- Account management (deposit, withdrawal, balance inquiry)
- Multi-account binding (one user can own multiple bank cards)
- Hierarchical account types with inheritance:
  - Savings Account (base savings, 2% annual interest, monthly fee)
  - Checking Account (overdraft support)
  - High-Interest Savings Account (5% interest, $200,000 minimum balance)
  - Student Savings Account (3% interest, no monthly fee)
- Annual/monthly interest calculation for savings accounts
- Account lock after 3 failed password attempts (24-hour auto-unlock)

## Project Structure
banking_app_structure.py # Core classes: User, Account, SavingsAccount, CheckingAccount, etc.

## Class Hierarchy
### User Class
- Handles user authentication, account security, and multi-account management
- Core methods: `register()`, `login()`, `check_auto_logout()`, `add_account()`, `show_all_accounts()`

### Account Class (Base Class)
Account
├── SavingsAccount
│ ├── HighInterestSavingsAccount
│ └── StudentSavingsAccount
└── CheckingAccount
- **Account**: Base class with deposit, withdraw, balance inquiry
- **SavingsAccount**: Adds interest calculation and monthly fee
- **CheckingAccount**: Overrides withdraw to support overdraft
- **HighInterestSavingsAccount**: Adds minimum balance restriction
- **StudentSavingsAccount**: Removes monthly fee for student users








    
