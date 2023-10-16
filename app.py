from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import plotly.express as pe

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Set a secret key for sessions

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Пожалуйста, войдите в систему, чтобы получить доступ к этой странице"

# Define a simple User class for demonstration purposes
class User(UserMixin):
    def __init__(self, user_id, email, password):
        self.id = user_id
        self.email = email
        self.password = password


# Sample user data (replace with your own authentication logic)
users = {
    1: User(1, 'a@r', '12345')
}


# Helper function to find a user by email
def find_user_by_email(email):
    for user in users.values():
        if user.email == email:
            return user
    return None

@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = find_user_by_email(email)

        # Debug messages
        print(f"Email entered: {email}")
        print(f"Password entered: {password}")
        print(f"User found: {user}")

        if user:
            if user["password"] == password:  # Check if the passwords match
                login_user(User(user['email']))  # Log in the user
                flash('Вход в систему успешен!', 'success')
                return redirect(url_for('analysis'))
            else:
                flash('Неверный пароль', 'error')
        else:
            flash('Пользователь не найден', 'error')

    return render_template('login.html')


@app.route('/logout')
#@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('login'))

@app.route('/reg', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Replace this with your registration logic
        user_id = len(users) + 1
        users[user_id] = User(user_id, email, password)

        flash('Регистрация прошла успешно! Пожалуйста, войдите в систему.', 'success')
        return redirect(url_for('login'))

    return render_template('registration.html')

@app.route('/analysis')
#@login_required
def analysis():
    return render_template('analysis.html')



@app.route('/plot', methods=['POST'])  # через эту функцию строятся графики
@login_required
def plot():
    # Сбор данных с формы
    ind = request.form['ind']
    type_ = request.form['type']
    vendor = request.form['vendor']
    if vendor == 'all_v':
        vendor = None
    dealer = request.form['dealer']
    if dealer == 'all_d':
        dealer = None
    startdate = request.form['startdate']
    enddate = request.form['enddate']

    # Постройка графиков в зависимости от выбранного индекса
    if ind == 'Ins_mov':
        data = indexes.instant_moving_index_interval(type_, startdate, enddate, dealer, vendor)
    elif ind == 'Ins_y-y':
        data = indexes.instant_year_year_index_interval(type_, startdate, enddate, dealer, vendor)
    elif ind == 'Cur_mov':
        data = indexes.current_moving_index_interval(type_, startdate, enddate, dealer, vendor)
    elif ind == 'Cur_y-y':
        data = indexes.current_year_year_index_interval(type_, startdate, enddate, dealer, vendor)
    elif ind == 'Long_mov':
        data = indexes.long_moving_index_interval(type_, startdate, enddate, dealer, vendor)
    elif ind == 'Long_y-y':
        data = indexes.long_year_year_index_interval(type_, startdate, enddate, dealer, vendor)

    fig = pe.line(x=data['date'], y=data['index'])

    fig_json = fig.to_json()
    return jsonify({'fig_json': fig_json})

if __name__ == '__main__':
    app.run(debug=True)