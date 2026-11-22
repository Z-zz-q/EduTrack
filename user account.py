import os
import hashlib
def hash_password(password):
    encoded_text=password.encode("utf-8")
    sha_object=hashlib.sha256(encoded_text)
    result=sha_object.hexdigest()
    return result

def save_users(user_data):
    with open("users.txt","w",encoding="utf-8")as file:
        for name,pwdh in users_data.items():
            file.write(f"{name},{pwdh}\n")

def load_users():
    users={}
    if os.path.exists("users.txt"):
        with open("users.txt"."r",encoding="utf-8")as file:
            for line in file:
                line=line.strip()
                if line:
                    username,pwd_hash=line.split(",")
                    users[username]=pwd_hash
return users



def sign_up():
    users=load_users()
    username=input("Enter your username")
    if username in users:
        print("username already exists!")
        return
    password=input("Enter password")
    user[username]=hash_password(password)
    save_users(users)
    print("Sign up  successful!")

def login():
    users=load_users()
    username=input("Username: ")
    password=input("password: ")
    if username in users and users[username]==hash_password(password):
        print("Login successsful!")
        return username
    print("Invalid username or password")
    return None

def change_password(logged_username):
    if not logged_username:
        print("Please log in first")
        return
    users=load_users()
    old_pass=input("Enter old password:")
    if users[logged_username]!=hash_password(old_pass)
       print("Old password is incorrect")
       return
    new_pass=input("Enter new password:")
    users[logged_username]=hash_password(new_pass)
    save_users(users)
    print("Password updated successfully")