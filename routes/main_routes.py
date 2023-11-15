from flask import Blueprint, render_template, url_for
from forms.auth_form import RegistrationForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', title='Dashboard', active_page='dashboard')

@main_bp.route('/about')
def about_you():
    return render_template('about.html', title='About You', active_page='about')

@main_bp.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', title='Portfolio Content', active_page='portfolio')

@main_bp.route('/users')
def users():
    return render_template('users.html', title='Authorized Users', active_page='users')

@main_bp.route('/settings')
def settings():
    return render_template('settings.html', title='Settings', active_page='settings')

@main_bp.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Registration logic goes here
        # Create and store the user in the database
        return redirect(url_for('login'))  # Redirect to login page after registration

    return render_template('register.html', title='Create User', form=form)