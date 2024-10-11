# web_app.py

from flask import Flask, render_template, request, redirect, url_for, flash
from core.password_checker import check_password_strength
from core.password_generator import generate_password
from core.password_manager import PasswordManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

# Initialize Password Manager
password_manager = PasswordManager()

# Existing routes
@app.route('/')
def home():
    # Render the page without any messages initially
    return render_template('index.html', 
                           check_strength_message=None, 
                           generate_password_message=None, 
                           save_password_message=None, 
                           retrieve_password_message=None)

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
    return render_template('index.html', 
                           check_strength_message=message, 
                           generate_password_message=None, 
                           save_password_message=None, 
                           retrieve_password_message=None)

@app.route('/generate_password', methods=['POST'])
def generate_new_password():
    try:
        length = int(request.form.get('length', 12))
    except ValueError:
        flash("Invalid input. Please enter a number for password length.", "error")
        return redirect(url_for('home'))
    
    uppercase = 'uppercase' in request.form
    lowercase = 'lowercase' in request.form
    numbers = 'numbers' in request.form
    special_chars = 'special_chars' in request.form

    if length < 8:
        flash("Password length should be at least 8 characters.", "error")
        return redirect(url_for('home'))

    password = generate_password(length, uppercase, lowercase, numbers, special_chars)
    message = f"Generated Password: {password}"
    # Pass the generated password message to the template
    return render_template('index.html', 
                           generate_password_message=message, 
                           check_strength_message=None, 
                           save_password_message=None, 
                           retrieve_password_message=None)

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
    return render_template('index.html', 
                           save_password_message=message, 
                           check_strength_message=None, 
                           generate_password_message=None, 
                           retrieve_password_message=None)

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
    return render_template('index.html', 
                           retrieve_password_message=message, 
                           check_strength_message=None, 
                           generate_password_message=None, 
                           save_password_message=None)

# New routes for sidebar links
@app.route('/my-details')
def my_details():
    return render_template('my_details.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/plan')
def plan():
    return render_template('plan.html')

@app.route('/billing')
def billing():
    return render_template('billing.html')

@app.route('/email')
def email():
    return render_template('email.html')

@app.route('/notifications')
def notifications():
    return render_template('notifications.html')

@app.route('/integrations')
def integrations():
    # Example integration data. In a real application, fetch this from a database or API.
    integrations = [
        {'id': 'google', 'name': 'Google', 'description': 'Synchronize your passwords with Google services.', 'connected': False},
        {'id': 'slack', 'name': 'Slack', 'description': 'Receive notifications and updates via Slack.', 'connected': True},
        {'id': 'dropbox', 'name': 'Dropbox', 'description': 'Backup your passwords to Dropbox.', 'connected': False},
        # Add more integrations as needed
    ]
    return render_template('integrations.html', integrations=integrations)

@app.route('/api')
def api():
    return render_template('api.html')

# New routes for header links
@app.route('/dashboard')
def dashboard():
    # Example data for the dashboard
    total_passwords = password_manager.get_total_passwords()
    last_password_added = password_manager.get_last_password_added()
    security_alerts = password_manager.get_security_alerts()

    # Example dashboard metrics
    dashboard_metrics = [
        ["Total Passwords", total_passwords],
        ["Last Password Added", last_password_added],
        ["Security Alerts", security_alerts],
    ]

    return render_template('dashboard.html', 
                           total_passwords=total_passwords, 
                           last_password_added=last_password_added, 
                           security_alerts=security_alerts, 
                           dashboard_metrics=dashboard_metrics)

@app.route('/projects')
def projects():
    # Example data for projects
    projects = password_manager.get_projects()
    return render_template('projects.html', projects=projects)

@app.route('/tasks')
def tasks():
    # Example data for tasks
    tasks = password_manager.get_tasks()
    return render_template('tasks.html', tasks=tasks)

@app.route('/reporting')
def reporting():
    # Example data for reporting
    reports = password_manager.get_reports()
    return render_template('reporting.html', reports=reports)

@app.route('/users')
def users():
    # Example data for users
    users = password_manager.get_users()
    return render_template('users.html', users=users)

# New routes for adding and editing projects
@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        project_name = request.form.get('project_name')
        description = request.form.get('description')
        password_policy = request.form.get('password_policy')

        if not project_name or not description or not password_policy:
            flash("All fields are required to add a new project.", "error")
            return redirect(url_for('add_project'))

        password_manager.add_project(project_name, description, password_policy)
        flash(f"Project '{project_name}' added successfully.", "success")
        return redirect(url_for('projects'))
    
    return render_template('add_project.html')

@app.route('/edit_project/<int:project_index>', methods=['GET', 'POST'])
def edit_project(project_index):
    projects = password_manager.get_projects()
    if project_index < 0 or project_index >= len(projects):
        flash("Project not found.", "error")
        return redirect(url_for('projects'))
    
    if request.method == 'POST':
        project_name = request.form.get('project_name')
        description = request.form.get('description')
        password_policy = request.form.get('password_policy')

        if not project_name or not description or not password_policy:
            flash("All fields are required to edit the project.", "error")
            return redirect(url_for('edit_project', project_index=project_index))

        success = password_manager.edit_project(project_index, project_name, description, password_policy)
        if success:
            flash(f"Project '{project_name}' updated successfully.", "success")
        else:
            flash("Failed to update the project. Please try again.", "error")
        return redirect(url_for('projects'))
    
    project = projects[project_index]
    return render_template('edit_project.html', project=project, project_index=project_index)

@app.route('/delete_project/<int:project_index>', methods=['POST'])
def delete_project(project_index):
    projects = password_manager.get_projects()
    if project_index < 0 or project_index >= len(projects):
        flash("Project not found.", "error")
        return redirect(url_for('projects'))

    project_name = projects[project_index]['project_name']
    success = password_manager.delete_project(project_index)
    if success:
        flash(f"Project '{project_name}' deleted successfully.", "success")
    else:
        flash("Failed to delete the project. Please try again.", "error")
    return redirect(url_for('projects'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
