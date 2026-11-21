import os
import hashlib
def hash_password(password):
    encoded_text=password.encode("utf-8")
    sha_object=hashlib.sha256(encoded_text)
    result=sha_object.hexdigest()
    return result

def load_users():
    users={}
    if os.path.exists("users.txt"):
        with open("users.txt"."r",encoding="utf-8")as file:
            for line in file:
                line=line.strip()
                if line:
                    username,pwd_hash=line.split(",")
                    users[username=pwd_hash]
    return users

def save users(user_data):
    with open("users.txt,"w",encoding="utf-8")as file:
        for name,pwdh in users_data.items():
            file.write(f"{name},{pwdh}\n")