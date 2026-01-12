import os
import sys

# Додаємо корінь проекту до шляхів
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
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
from core.models import User, Product, Order, Category, StaticPage, GlobalSettings, Translation, Farm

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

# Кастомна в'юха для продуктів
class ProductView(SecureModelView):
    column_list = ('id', 'name', 'name_de', 'price', 'unit', 'sku', 'availability_status', 'category', 'farm')
    column_display_pk = True
    column_labels = {
        'id': 'ID',
        'name': 'Назва (Укр)',
        'name_de': 'Назва (Нім)',
        'price': 'Ціна',
        'unit': 'Одиниця виміру',
        'sku': 'Артикул (SKU)',
        'availability_status': 'Статус наявності',
        'category': 'Категорія',
        'farm': 'Ферма/Виробник'
    }

# Кастомна в'юха для категорій
class CategoryView(SecureModelView):
    column_labels = {
        'id': 'ID',
        'name': 'Назва (Укр)',
        'name_de': 'Назва (Нім)',
        'slug': 'Слаг',
        'image_url': 'URL зображення',
        'description': 'Опис (Укр)',
        'description_de': 'Опис (Нім)'
    }

# Кастомна в'юха для ферм
class FarmView(SecureModelView):
    column_labels = {
        'id': 'ID',
        'name': 'Назва',
        'description_uk': 'Опис (Укр)',
        'description_de': 'Опис (Нім)',
        'location': 'Місцезнаходження',
        'contact_info': 'Контактна інформація',
        'is_active': 'Активний'
    }

# Кастомна в'юха для користувачів
class UserView(SecureModelView):
    column_list = ('id', 'tg_id', 'full_name', 'email', 'username', 'phone', 'is_trusted', 'is_admin', 'language_pref', 'created_at')
    column_exclude_list = ['password_hash']  # Hide password hash from list view
    form_excluded_columns = ['password_hash']  # Hide from form, handle separately if needed

admin = Admin(app, name='Osna Farm Admin')

# Add logout menu item
admin.add_link(MenuLink(name='Logout', category='', url='/admin/logout'))

# Додаємо в'юхи правильно
admin.add_view(UserView(User, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(FarmView(Farm, db.session))
admin.add_view(SecureModelView(Order, db.session))
admin.add_view(CategoryView(Category, db.session))
admin.add_view(SecureModelView(StaticPage, db.session))
admin.add_view(SecureModelView(GlobalSettings, db.session))
admin.add_view(SecureModelView(Translation, db.session))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        print(f"Login attempt for: {form.username.data}")
        from sqlalchemy import select
        with db.session() as session:
            # First try Telegram ID (backward compatibility)
            try:
                tg_id = int(form.username.data)
                user = session.execute(select(User).where(User.tg_id == tg_id)).scalar_one_or_none()
                print(f"Found user by TG ID: {user.full_name if user else 'None'}")
            except ValueError:
                # Not a number, try email or username
                user = session.execute(select(User).where(
                    (User.email == form.username.data) | (User.username == form.username.data)
                )).scalar_one_or_none()
                print(f"Found user by email/username: {user.full_name if user else 'None'}")

            if user:
                print(f"User is_admin: {user.is_admin}")
                if user.password_hash:
                    # Has password, check it
                    if check_password_hash(user.password_hash, form.password.data):
                        print("Password match")
                        if user.is_admin:
                            login_user(user)
                            print("Login successful, redirecting")
                            return redirect(url_for('admin.index'))
                        else:
                            print("User is not admin")
                            flash('Access denied')
                    else:
                        print("Password mismatch")
                        flash('Invalid password')
                else:
                    # No password set, allow login via TG ID only
                    if str(user.tg_id) == form.username.data:
                        print("No password required, login via TG ID")
                        if user.is_admin:
                            login_user(user)
                            print("Login successful, redirecting")
                            return redirect(url_for('admin.index'))
                        else:
                            print("User is not admin")
                            flash('Access denied')
                    else:
                        print("No password set, but not logging in via TG ID")
                        flash('Invalid credentials')
            else:
                print("User not found")
                flash('User not found')
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
            {form.username(placeholder="Email or Username")}
            {form.password(placeholder="Password")}
            <button type="submit">Log In</button>
        </form>
    </body>
    </html>
    '''

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>404 - Page Not Found</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background-color: #f4f4f4; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            h1 { color: #e74c3c; font-size: 100px; margin: 0; }
            p { font-size: 18px; color: #666; }
            a { color: #3498db; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>404</h1>
            <p>Page not found / Сторінку не знайдено</p>
            <p>The page you are looking for might have been removed or is temporarily unavailable.</p>
            <p><a href="/admin">Go back to Admin</a></p>
        </div>
    </body>
    </html>
    ''', 404

if __name__ == '__main__':
    # Встановлюємо кодування для виводу в термінал прямо з коду
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("🚀 Running on http://localhost:5000/admin")
    app.run(host='0.0.0.0', port=5000, debug=True)