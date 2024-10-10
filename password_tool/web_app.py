# web_app.py

from flask import Flask, render_template, request, redirect, url_for
from core.password_checker import check_password_strength
from core.password_generator import generate_password
from core.password_manager import PasswordManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

# Initialize Password Manager
password_manager = PasswordManager()

@app.route('/')
def home():
    # Render the page without any messages initially
    return render_template('index.html', check_strength_message=None, generate_password_message=None, save_password_message=None, retrieve_password_message=None)

@app.route('/check_strength', methods=['POST'])
def check_strength():
    password = request.form.get('password')
    message = ""
    if not password:
        message = "Please enter a password."
    else:
        strength, feedback = check_password_strength(password)
        feedback_text = "<br>".join(feedback)
        message = f"Strength: {strength}<br>{feedback_text}"
    # Pass the message to be displayed inside the card
    return render_template('index.html', check_strength_message=message, generate_password_message=None, save_password_message=None, retrieve_password_message=None)

@app.route('/generate_password', methods=['POST'])
def generate_new_password():
    try:
        length = int(request.form.get('length', 12))
    except ValueError:
        return render_template('index.html', generate_password_message="Invalid input. Please enter a number for password length.", check_strength_message=None, save_password_message=None, retrieve_password_message=None)
    
    uppercase = 'uppercase' in request.form
    lowercase = 'lowercase' in request.form
    numbers = 'numbers' in request.form
    special_chars = 'special_chars' in request.form

    if length < 8:
        return render_template('index.html', generate_password_message="Password length should be at least 8 characters.", check_strength_message=None, save_password_message=None, retrieve_password_message=None)

    password = generate_password(length, uppercase, lowercase, numbers, special_chars)
    message = f"Generated Password: {password}"
    # Pass the generated password message to the template
    return render_template('index.html', generate_password_message=message, generated_password=password, check_strength_message=None, save_password_message=None, retrieve_password_message=None)

@app.route('/save_password', methods=['POST'])
def save_password():
    account = request.form.get('account')
    password = request.form.get('password')
    message = ""

    if not account or not password:
        message = "Please enter both account name and password."
    else:
        password_manager.add_password(account, password)
        message = f"Password for {account} saved successfully."
    # Pass the save message to the template
    return render_template('index.html', save_password_message=message, check_strength_message=None, generate_password_message=None, retrieve_password_message=None)

@app.route('/retrieve_password', methods=['POST'])
def retrieve_password():
    account = request.form.get('account')
    message = ""

    if not account:
        message = "Please enter the account name."
    else:
        password = password_manager.get_password(account)
        if password:
            message = f"Password for {account} is: {password}"
        else:
            message = f"No password found for {account}."
    # Pass the retrieval message to the template
    return render_template('index.html', retrieve_password_message=message, check_strength_message=None, generate_password_message=None, save_password_message=None)

if __name__ == '__main__':
    app.run(debug=True)
