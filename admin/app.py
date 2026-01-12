import os
import sys

# Додаємо корінь проекту до шляхів
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Імпортуємо моделі ПІСЛЯ ініціалізації db, щоб уникнути циклічних імпортів
from core.models import User, Product, Order, Category, StaticPage

class LoginForm(FlaskForm):

    username = StringField('Username')

    password = PasswordField('Password')

    submit = SubmitField('Login')

class SecureModelView(ModelView):

    def is_accessible(self):

        return current_user.is_authenticated and current_user.is_admin

# Кастомна в'юха для продуктів
class ProductView(SecureModelView):
    column_list = ('id', 'name', 'price', 'unit', 'is_available')
    column_display_pk = True

admin = Admin(app, name='Osna Farm Admin')

# Додаємо в'юхи правильно
admin.add_view(SecureModelView(User, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(SecureModelView(Order, db.session))
admin.add_view(SecureModelView(Category, db.session))
admin.add_view(SecureModelView(StaticPage, db.session))

if __name__ == '__main__':
    # Встановлюємо кодування для виводу в термінал прямо з коду
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("🚀 Running on http://localhost:5000/admin")
    app.run(host='0.0.0.0', port=5000, debug=True)