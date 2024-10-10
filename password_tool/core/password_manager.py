# password_manager.py

from cryptography.fernet import Fernet
import os

class PasswordManager:
    def __init__(self, key_file='key.key', password_file='passwords.enc'):
        self.key_file = key_file
        self.password_file = password_file
        self.key = self.load_key()
        self.fernet = Fernet(self.key)

    def load_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as key_file:
                key = key_file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as key_file:
                key_file.write(key)
        return key

    def add_password(self, account, password):
        encrypted = self.fernet.encrypt(password.encode())
        with open(self.password_file, 'ab') as file:
            file.write(f"{account}:{encrypted.decode()}\n".encode())

    def get_password(self, account):
        if not os.path.exists(self.password_file):
            return None
        with open(self.password_file, 'rb') as file:
            lines = file.readlines()
            for line in lines:
                acc, encrypted = line.decode().strip().split(':')
                if acc == account:
                    decrypted = self.fernet.decrypt(encrypted.encode()).decode()
                    return decrypted
        return None
