import os #check if the file exists
import hashlib #encrypt password with SHA256
def hash_password(password):
    encoded_text=password.encode("utf-8")# Convert password string to UTF-8 byte format for hashing
    sha_object=hashlib.sha256(encoded_text)# Create a SHA256 hash object with the byte data
    result=sha_object.hexdigest()# Convert hash value to hexadecimal string
    return result

def save_users(user_data):
    with open("users.txt","w",encoding="utf-8")as file:
        for name,pwdh in users_data.items():# Loop through every username and password hash pair
            file.write(f"{name},{pwdh}\n")

def load_users():
    users={}# Create empty dictionary to store username and password hash
    if os.path.exists("users.txt"):# Check whether users.txt file exists
        with open("users.txt"."r",encoding="utf-8")as file:
            for line in file:
                line=line.strip()# Remove blank space and newline symbol of this line
                if line:# Skip empty line, only process non-empty line
                    username,pwd_hash=line.split(",")# Split the line by comma into username and encrypted password
                    users[username]=pwd_hash# Store this pair into users dictionary
return users



def sign_up():
    users=load_users()
    username=input("Enter your username")
    if username in users:
        print("username already exists!")
        return
    password=input("Enter password")
    users[username]=hash_password(password)# Encrypt password and add new user into users dictionary
    save_users(users)# Save updated users dictionary back to text file
    print("Sign up  successful!")

def login():
    users=load_users()# Load all saved user data
    username=input("Username: ")
    password=input("password: ")
    if username in users and users[username]==hash_password(password):
        print("Login successsful!")
        return username
    print("Invalid username or password")
    return None# Return None, means login failed

def change_password(logged_username):
    if not logged_username:
        print("Please log in first")
        return
    users=load_users()# Reload latest user data
    old_pass=input("Enter old password:")
    if users[logged_username]!=hash_password(old_pass)
       print("Old password is incorrect")
       return
    new_pass=input("Enter new password:")
    users[logged_username]=hash_password(new_pass)
    save_users(users)
    print("Password updated successfully")