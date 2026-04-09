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

### 2026-04-10 Update
✅ **Fixed Critical Login & Account Lock Logic Bugs**
- Corrected `login()` method: Moved failed login count increment to `else` branch, preventing count increase on successful login
- Fixed indentation error in `login()` method, ensuring lock account logic only executes on incorrect password
- Added `_lock_start_time` initialization on account lock, avoiding `TypeError` in `check_lock_status()`
- Implemented full null check for `_lock_start_time` in `check_lock_status()`, preventing datetime subtraction errors
- Fixed typo `_failed_login_conut` to `_failed_login_count` in `check_lock_status()`
- Verified `check_auto_logout()` logic, ensuring correct auto-logout trigger and audit log recording
- Strengthened account security flow, ensuring compliance with financial system access control requirements