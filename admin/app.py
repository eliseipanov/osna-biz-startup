import os
import sys

# Додаємо корінь проекту до шляхів
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("BOT_TOKEN", "dev-secret")

# Налаштування бази
DATABASE_URL = os.getenv("DATABASE_URL").replace("postgresql+asyncpg", "postgresql")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Це примусово лікує UnicodeDecodeError на рівні підключення
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {
        "options": "-c client_encoding=utf8"
    }
}

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from sqlalchemy import select
    from core.models import User
    with db.session() as session:
        return session.execute(select(User).where(User.id == int(user_id))).scalar_one_or_none()

# Імпортуємо моделі ПІСЛЯ ініціалізації db, щоб уникнути циклічних імпортів
from core.models import User, Product, Order, Category, StaticPage

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

# Кастомна в'юха для продуктів
class ProductView(SecureModelView):
    column_list = ('id', 'name', 'price', 'unit', 'is_available', 'category')
    column_display_pk = True

admin = Admin(app, name='Osna Farm Admin')

# Додаємо в'юхи правильно
admin.add_view(SecureModelView(User, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(SecureModelView(Order, db.session))
admin.add_view(SecureModelView(Category, db.session))
admin.add_view(SecureModelView(StaticPage, db.session))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        from sqlalchemy import select
        with db.session() as session:
            user = session.execute(select(User).where(User.tg_id == int(form.username.data))).scalar_one_or_none()
        if user and user.password_hash and check_password_hash(user.password_hash, form.password.data) and user.is_admin:
            login_user(user)
            return redirect(url_for('admin.index'))
        flash('Invalid username or password')
    return f'''
    <!DOCTYPE html>
    <html lang="uk">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: #f4f4f4; }}
            form {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 90%; max-width: 320px; }}
            input {{ width: 100%; padding: 10px; margin: 10px 0; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }}
            button {{ width: 100%; padding: 10px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; }}
        </style>
    </head>
    <body>
        <form method="POST">
            {form.csrf_token()}
            <h3>Osna Farm Admin</h3>
            {form.username(placeholder="TG ID")}
            {form.password(placeholder="Password")}
            <button type="submit">Log In</button>
        </form>
    </body>
    </html>
    '''

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Встановлюємо кодування для виводу в термінал прямо з коду
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("🚀 Running on http://localhost:5000/admin")
    app.run(host='0.0.0.0', port=5000, debug=True)