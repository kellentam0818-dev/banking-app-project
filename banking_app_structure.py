import time
from datetime import datetime, timedelta


# Define the User parent class: encapsulate the general logic
# for user login/registration/security verification
class User:
    # class atrribute: The maximum number of password retries
    # shared by all users and the automatic logout timeout period (5 minutes)
    MAX_PASSWORD_RETRIES = 3
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

        # password correct: reset retry count, update login status and last operation time
        if input_password == self._password:
            self._password_retry_count = 0
            self._login_status = True
            self._last_operation_time = datetime.now()
            # Show welcome message and last login time
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return f"Welcome, {self._user_id}! You logged in successfully at {current_datetime}."

        # password incorrect: increment retry count, check for lock condition
        self._password_retry_count += 1
        if self._password_retry_count >= User.MAX_PASSWORD_RETRIES:
            self._is_locked = True
            return f"User {self._user_id} account is locked due to too many incorrect password attempts. Please contact support to unlock."
        else:
            remaining_times = User.MAX_PASSWORD_RETRIES - self._password_retry_count
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
