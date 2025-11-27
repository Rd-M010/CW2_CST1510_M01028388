import bcrypt
import os
USER_DATA_FILE = "users.txt"   # File where users will be stored

def hash_password(plain_text_password):
    # Convert the password to bytes (bcrypt needs bytes)
    password_bytes = plain_text_password.encode()

    # Create a random salt to make the hash unique
    salt = bcrypt.gensalt()

    # Create the hashed password
    hashed = bcrypt.hashpw(password_bytes, salt)

    # Convert hash back to string so we can save it
    return hashed.decode()

def verify_password(plain_text_password, hashed_password):
    # Convert both passwords to bytes
    password_bytes = plain_text_password.encode()
    hashed_bytes = hashed_password.encode()

    # Compare the two passwords
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def user_exists(username):
    # If the file does not exist, no users exist yet
    if not os.path.exists(USER_DATA_FILE):
        return False

    # Open the file and check each line
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            saved_username = line.split(",")[0]

            # If username matches → user exists
            if saved_username == username:
                return True

    # Username not found
    return False

def register_user(username, password):
    # Check if username already exists
    if user_exists(username):
        print("Error: Username already exists.")
        return False

    # Hash the password
    hashed = hash_password(password)

    # Save username and hashed password in the file
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username},{hashed}\n")

    print("User registered successfully.")
    return True
def login_user(username, password):
    # Check if file exists
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users registered yet.")
        return False

    # Read each user in the file
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            saved_username, saved_hashed_password = line.strip().split(",")

            # If username matches
            if saved_username == username:

                # Verify password
                if verify_password(password, saved_hashed_password):
                    print(f"Success: Welcome, {username}!")
                    return True
                else:
                    print("Error: Invalid password.")
                    return False

    # Username not found
    print("Error: Username not found.")
    return False
def validate_username(username):
    # Username must be 3–20 characters long
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be between 3 and 20 characters."

    # Username must only contain letters and numbers
    if not username.isalnum():
        return False, "Username must contain only letters and numbers."

    return True, ""

def validate_password(password):
    # Password must be at least 6 characters
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    return True, ""

def display_menu():
    print("\n--- MENU ---")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

def main():
    while True:
        display_menu()

        # Ask user to choose an option
        choice = input("Enter your choice: ")

        if choice == "1":
            # REGISTER
            username = input("Enter username: ")
            valid, msg = validate_username(username)

            # If username is invalid
            if not valid:
                print(msg)
                continue

            password = input("Enter password: ")
            valid, msg = validate_password(password)

            # If password is invalid
            if not valid:
                print(msg)
                continue

            confirm = input("Confirm password: ")

            # Check passwords match
            if password != confirm:
                print("Error: Passwords do not match.")
                continue

            register_user(username, password)

        elif choice == "2":
            # LOGIN
            username = input("Enter username: ")
            password = input("Enter password: ")
            login_user(username, password)

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()
 