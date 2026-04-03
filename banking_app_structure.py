from datetime import datetime, timedelta


# Define the User parent class: encapsulate the general logic
# for user login/registration/security verification
class User:
    # class atrribute: The maximum number of password retries
    # shared by all users and the automatic logout timeout period (5 minutes)
    MAX_FAILED_LOGIN_ATTEMPTS = 3
    AUTO_LOGOUT_MINUTES = 5
    LOCK_DURATION = timedelta(hours=24)

    # Initializer method to set up user attributes
    # Instance attributes (private attributes, starting with _,
    # need to be accessed through methods from outside)
    def __init__(self, user_id):
        self._user_id = user_id
        self._password = None
        self._failed_login_count = 0
        self._lock_start_time = None
        self._is_locked = False
        self._login_status = False
        self._last_operation_time = None

        self.accounts = []

    def add_account(self, account):
        """Add an account to the user's account list."""
        self.accounts.append(account)
        return f"Account {account._account_num} added to user {self._user_id}."

    def show_all_accounts(self):
        """Display all accounts associated with the user."""
        print(f"User {self._user_id} accounts:")
        if not self.accounts:
            return f"User {self._user_id} has no accounts."
        account_info = [
            f"Account Number: {acc._account_num}, Balance: ${acc._balance:.2f}"
            for acc in self.accounts
        ]
        return f"User {self._user_id} accounts:\n" + "\n".join(account_info)

    def check_lock_status(self):
        """Check if the account is currently locked and update lock status based on lock duration."""
        if not self._is_locked:
            return None

        current_time = datetime.now()
        lock_elapsed_time = current_time - self._lock_start_time

        # If the lock duration has passed, unlock the account and reset the failed login count
        if lock_elapsed_time > User.LOCK_DURATION:
            self._is_locked = False
            self._failed_login_count = 0
            self._lock_start_time = None
            return f"User {self._user_id} account has been unlocked after 24 hours."
        return None

    # Method 1: First registration (automatically register with user_id and set password)
    def register(self, password):
        # Check if the lock status has changed(automatic unlock after 24 hours)
        unlock_msg = self.check_lock_status()

        # Checl if the user is already registered
        if self._password is not None:
            # If there is an automatic unlock prompt, concatenate and return it.
            if unlock_msg:
                return f"{unlock_msg} But user {self._user_id} already registered."
            return f"User {self._user_id} already registered."

        # Never register and lock before. New account
        self._password = password
        return f"User {self._user_id} registered successfully."

    def __str__(self):
        """Customize the output format when printing user instances (core status)"""
        lock_start = (
            self._lock_start_time.strftime("%Y-%m-%d %H:%M:%S")
            if self._lock_start_time
            else None
        )
        return (
            f"User ID: {self._user_id}, "
            f"Account Locked: {'Yes' if self._is_locked else 'No'}, "
            f"Failed Login Count: {self._failed_login_count}, "
            f"Lock Start Time: {lock_start}"
        )

    # Method 2: Login method (verify password, update login status and lock logic)
    def login(self, input_password):
        # Check if the account is locked or already logged in
        if self._is_locked:
            return f"User {self._user_id} account is locked. The number of incorrect entries has reached the limit. You need to unlock it in person with valid identification."

        if self._login_status:
            return f"User {self._user_id} is already logged in."

        # password correct: reset failed login count, update login status and last operation time
        if input_password == self._password:
            self._failed_login_count = 0
            self._login_status = True
            self._last_operation_time = datetime.now()
            # Show welcome message and last login time
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return f"Welcome, {self._user_id}! You logged in successfully at {current_datetime}."

        # password incorrect: increment failed login count, check for lock condition
        self._failed_login_count += 1
        if self._failed_login_count >= User.MAX_FAILED_LOGIN_ATTEMPTS:
            self._is_locked = True
            return f"User {self._user_id} account is locked due to too many incorrect password attempts. Please contact support to unlock."
        else:
            remaining_times = User.MAX_FAILED_LOGIN_ATTEMPTS - self._failed_login_count
            return f"Incorrect password. You have {remaining_times} more attempt(s) before your account gets locked."

    # Method 3: Logout method (update login status and reset last operation time)
    def check_auto_logout(self):
        # No need for verification when not logged in or during periods of inactivity
        if not self._login_status:
            return "Not logged in. No need to check for auto logout."

        if self._last_operation_time is None:
            return "No operation record found. Please perform a valid operation first."

        elapsed_time = datetime.now() - self._last_operation_time
        if elapsed_time > timedelta(minutes=User.AUTO_LOGOUT_MINUTES):
            self._login_status = False
            self._last_operation_time = None
            return "Auto logout triggered due to inactivity."
        return "User is active. No auto logout needed."

    # Method 4: Update the last operation time (called after user operation to prevent automatic logout)
    def update_last_operation_time(self):
        if self._login_status:
            self._last_operation_time = datetime.now()
            return f"Last operation time updated for user {self._user_id}."
        return (
            f"User {self._user_id} is not logged in. Cannot update last operation time."
        )

    # Method 5: Acquire user status (for external viewing )
    def get_user_status(self):
        status = {
            "user_id": self._user_id,
            "login_status": self._login_status,
            "is_locked": self._is_locked,
            "last_operation_time": (
                self._last_operation_time.strftime("%Y-%m-%d %H:%M:%S")
                if self._last_operation_time
                else None
            ),
        }
        return status


# Define the account class (general attributes/ behaviors of all accounts)
class Account:
    def __init__(self, account_num, balance):
        self._account_num = account_num
        self._balance = balance

    def check_balance(self):
        return f"Account {self._account_num} balance: ${self._balance:.2f}"

    def deposit(self, amount):
        if amount <= 0:
            return "Deposit must be greater than 0."
        self._balance += amount
        return f"Deposit successful. New balance: ${self._balance:.2f}"

    def withdraw(self, amount):
        if amount <= 0:
            return "Withdrawal must be greater than 0."
        if amount > self._balance:
            return "Insufficient funds."
        self._balance -= amount
        return f"Withdrawal successful. New balance: ${self._balance:.2f}"

    def transfer_to(self, target_account, amount):
        """
        Transfer funds from this account to a target account.

        Supports all transfer scenarios:
        - Self transfers (same user, different accounts, e.g., savings to credit card)
        - Transfers to other users' accounts
        - Cross-account transfers between any valid Account instances

        Args:
            target_account (Account): The target account to receive the transfer.
            amount (float): The amount of money to transfer.

        Returns:
            str: Status message indicating success or failure.
        """
        # Validate transfer amount is positive
        if amount <= 0:
            return "Transfer amount must be greater than 0."

        # Validate sufficient balance in the source account
        if amount > self._balance:
            return "Insufficient funds for transfer."

        # Deduct amount from the current (source) account
        self._balance -= amount

        # Add amount to the target account
        target_account._balance += amount
        return f"Transfer successful. New balance: ${self._balance:.2f}. Target balance: ${target_account._balance:.2f}"


# Inheritance: Define a specific type of account (e.g., SavingsAccount) that inherits from the Account class and adds specific attributes or methods if needed.
class SavingsAccount(Account):
    def __init__(self, account_num, balance, interest_rate=0.02):
        # Call the parent class initializer to set account number and balance
        super().__init__(account_num, balance)
        # Add specific attribute for savings account: interest rate(2% by default)
        self._interest_rate = interest_rate
        self._has_monthly_fee = True

    # # Exclusive Method for Savings Account: Calculate Interest + Auto Deposit to Balance
    def add_interest(self):
        interest = self._balance * self._interest_rate
        self._balance += interest
        return f"Interest added at rate {self._interest_rate*100:.2f}%. New balance: ${self._balance:.2f}"

    # New function: Annual or monthly interest rate
    def add_interest_rate_by_period(self, period="year"):
        if period == "year":
            interest = self._balance * self._interest_rate
            msg = "Yearly interest"

        elif period == "month":
            interest = self._balance * (self._interest_rate / 12)
            msg = "Monthly interest"

        else:
            return "Invalid period. Please choose 'year' or 'month'."

        self._balance += interest
        return f"Interest added at rate {self._interest_rate*100:.2f}%. New balance: ${self._balance:.2f}"

    def has_monthly_fee(self):
        return self._has_monthly_fee


# Inheritance: Define another specific type of account (e.g., CheckingAccount) that inherits from the Account class and adds specific attributes or methods if needed.
class CheckingAccount(Account):
    def __init__(self, account_num, balance, overdraft_limit=500):
        # Call the parent class initializer to set account number and balance
        super().__init__(account_num, balance)
        # Add specific attribute for checking account: overdraft limit
        self._overdraft_limit = overdraft_limit

    # Exclusive Method for Checking Account: Override the withdraw method to allow overdraft within the limit
    def withdraw(self, amount):
        if amount <= 0:
            return "Withdrawal must be greater than 0."
        if amount > self._balance + self._overdraft_limit:
            return "Insufficient funds, including overdraft limit."
        self._balance -= amount
        return f"Withdrawal successful. New balance: ${self._balance:.2f}"


# Inheritance: Define a specific type of credit card account (e.g., CreditCardAccount) that inherits from the Account class and adds specific attributes or methods if needed.
class CreditCardAccount(Account):
    """
    A credit card account that allows negative balance up
    to a certain credit limit. Supports credit limit, balance
    tracking, and repayment.
    """

    def __init__(self, account_num, balance, credit_limit):
        """
        Args:
        account_num (str): Unique account number.
        balance (float): Current balance (negative means owed amount).
        credit_limit (float): Maximum credit limit.
        """
        super().__init__(account_num, balance)
        self._credit_limit = credit_limit

    def get_credit_limit(self):
        return self._credit_limit

    def available_credit(self):
        return self._credit_limit + self._balance  # balance is negative when owed

    def repay(self, amount):
        return self.deposit(
            amount
        )  # Repayment is treated as a deposit to reduce owed amount

    def withdraw(self, amount):
        if amount <= 0:
            return "Withdrawal must be greater than 0."
        if amount > self.available_credit():
            return "Insufficient credit available."
        self._balance -= amount  # Increase owed amount (more negative)
        return f"Withdrawal successful. New balance: ${self._balance:.2f}. Available credit: ${self.available_credit():.2f}"


# Inheritance: Define a specifit type of savings account (e.g., HighInterestSavingsAccount) that inherits from the SavingsAccount class and adds specific attributes or methods if needed.
class HighInterestSavingsAccount(SavingsAccount):
    def __init__(self, account_num, balance, interest_rate=0.05):
        if balance < 200000:
            raise ValueError(
                "High interest savings account requires a minimum balance of $200,000."
            )
        super().__init__(account_num, balance, interest_rate)

    def add_interest(self):
        result = super().add_interest()
        return f"High interest added at rate {self._interest_rate*100:.2f}%. New balance: ${self._balance:.2f}"

    def withdraw(self, amount):
        if self._balance - amount < 200000:
            return "Withdrawal denied. High interest savings account requires a minimum balance of $200,000."
        return super().withdraw(amount)


# Inheritance: Define specific savings account types (e.g., StudentSavingsAccount) that inherit from the SavingsAccount class and add specific attributes or methods for business accounts.
class StudentSavingsAccount(SavingsAccount):
    def __init__(self, account_num, balance, interest_rate=0.03):
        super().__init__(account_num, balance, interest_rate)
        # Student accounts have no monthly fee
        self._has_monthly_fee = False

    def add_interest(self):
        result = super().add_interest()
        return f"Student interest added at rate {self._interest_rate*100:.2f}%. New balance: ${self._balance:.2f}"


# Test case
if __name__ == "__main__":
    # Test case 1: Check_lock_status method test: create a user and simulate lock status change after 24 hours
    user1 = User("123456")
    print("Test case 1: doesn't be locked", user1._is_locked)

    # Test case 2: has been locked, but not yet 24 hours, check_lock_status should return lock status message)
    user1._is_locked = True
    user1._lock_start_time = datetime.now() - timedelta(
        hours=1
    )  # Simulate lock for 1 hour
    print("lock status: ", user1._is_locked)  # should return True
    print(
        "Test case 2: has been locked, but not yet 24 hours", user1.check_lock_status()
    )  # should return None

    # Test case 3: has been locked for more than 24 hours, check_lock_status should return unlock message and reset lock status
    user1._lock_start_time = datetime.now() - timedelta(
        hours=25
    )  # Simulate lock for 25 hours
    print(
        "Test case 3: has been locked for more than 24 hours", user1.check_lock_status()
    )  # should return True
    print("lock status: ", user1._is_locked)  # should return False
    print("failed login count: ", user1._failed_login_count)  # should return 0

    # Test case 4 : try auto logout method
    print("\n===== Test case 4: Auto logout test =====")
    # Step 1: First, register and log in (you must log in to test automatic logout)
    print("Step 1: Register and login...")
    user1.register("123456")  # pw:123456
    login_result = user1.login("123456")
    print("Login result:", login_result)
    print("User status after login:", user1)

    # Step 2: Check the situation where there is no timeout (just logged in, definitely no timeout)
    print("\nStep 2: Check auto logout (immediately after login, < 5 mins)...")
    logout_result1 = user1.check_auto_logout()
    print("Auto logout check result:", logout_result1)

    # Step 3: Simulate "no operation for more than 5 minutes" (⚠️ Note: Waiting for 5 minutes in real time is too long; here, we use manual time modification for simulation)
    print("\nStep 3: Simulate > 5 mins inactivity (modify last operation time)...")
    # Manually change the last operation time to "6 minutes ago" (skip the actual waiting time)
    user1._last_operation_time = datetime.now() - timedelta(minutes=6)
    logout_result2 = user1.check_auto_logout()
    print("Auto logout check result (after 6 mins):", logout_result2)
    print("User status after auto logout:", user1)  # False

    # test account class
    print("\n===== Test case 5: Account class test =====")
    account1 = Account("123456", 1000)
    print(account1.check_balance())
    print(account1.deposit(500))
    print(account1.withdraw(200))
    print(account1.withdraw(1500))  # should return insufficient funds
    print(account1.withdraw(-100))  # should return invalid withdrawal amount

    # test savings account class
    print("\n===== Test case 6: SavingsAccount class test =====")
    savings_account1 = SavingsAccount("654321", 2000)
    print(savings_account1.check_balance())
    print(savings_account1.add_interest())  # should add interest and update balance
    print(savings_account1.withdraw(100))  # should work like normal withdrawal
    print(savings_account1.withdraw(3000))  # should return insufficient funds
    save = SavingsAccount("654321", 2000)
    print(save.add_interest_rate_by_period("year"))
    print(save.add_interest_rate_by_period("month"))
    print(save.has_monthly_fee())  # should return True

    # test checking account class
    print("\n===== Test case 7: CheckingAccount class test =====")
    checking_account1 = CheckingAccount("789012", 500, overdraft_limit=300)
    print(checking_account1.check_balance())
    print(checking_account1.withdraw(200))
    print(
        checking_account1.withdraw(600)
    )  # should return insufficient funds, including overdraft limit
    print(checking_account1.withdraw(-100))  # should return invalid withdrawal amount

    # test high interest savings account class
    print("\n===== Test case 8: HighInterestSavingsAccount class test =====")
    try:
        high_interest_account1 = HighInterestSavingsAccount(
            "987654", 150000
        )  # should raise ValueError
    except ValueError as e:
        print("Error creating high interest savings account:", e)
    high_interest_account2 = HighInterestSavingsAccount(
        "987654", 250000
    )  # should create successfully
    print(high_interest_account2.check_balance())
    print(
        high_interest_account2.add_interest()
    )  # should add high interest and update balance
    print(high_interest_account2.withdraw(60000))  # should work like normal withdrawal
    print(
        high_interest_account2.withdraw(200000)
    )  # should return withdrawal denied due to minimum balance requirement

    # test student savings account class
    print("\n===== Test case 9: StudentSavingsAccount class test =====")
    student_savings_account1 = StudentSavingsAccount("555555", 5000)
    print(student_savings_account1.check_balance())
    print(
        student_savings_account1.add_interest()
    )  # should add student interest and update balance
    print(student_savings_account1.withdraw(1000))  # should work like normal withdrawal
    print(student_savings_account1.withdraw(10000))  # should return insufficient funds
    save2 = StudentSavingsAccount("555555", 5000)
    print(save2.has_monthly_fee())  # should return False

    # test user account management
    print("\n===== Test case 10: User account management test =====")
    # Suppose you have a savings account and a credit card account
    savings = SavingsAccount("123456", 1000.0)
    credit_card = CreditCardAccount("789012", 0.0, 5000.0)

    # Repay 500 dollars of credit card debt using a debit card
    print(savings.transfer_to(credit_card, 500))
    # Output: Transfer successful. New balance: $500.00 Target account new balance: $500.00
    # Tranfer 200 dollars from the debit card to other user's account (e.g., a friend)
    friend_account = Account("654321", 300.0)
    print(savings.transfer_to(friend_account, 200))
    # Output: Transfer successful. New balance: $300.00
