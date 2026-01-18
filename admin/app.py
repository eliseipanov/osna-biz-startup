import os
import sys

# Додаємо корінь проекту до шляхів
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from flask_admin.menu import MenuLink
from dotenv import load_dotenv

# Import shared extensions
from extensions import db, login_manager, limiter, admin

load_dotenv()

app = Flask(__name__, template_folder='../templates', static_folder='../static')

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit

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

# Initialize extensions with app
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'admin_api.login'
limiter.init_app(app)
admin.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from sqlalchemy import select
    from core.models import User
    with db.session() as session:
        return session.execute(select(User).where(User.id == int(user_id))).scalar_one_or_none()

# Імпортуємо моделі ПІСЛЯ ініціалізації db, щоб уникнути циклічних імпортів
from core.models import User, Product, Order, Category, StaticPage, GlobalSettings, Translation, Farm, Transaction, TransactionType, TransactionStatus, CartItem, OrderItem, Region

# Import views and routes
from admin.admin_views import UserView, ProductView, FarmView, CategoryView, TransactionView, SecureModelView, RegionView
from admin.routes import admin_api


# Register the blueprint
app.register_blueprint(admin_api)

# Add logout menu item
admin.add_link(MenuLink(name='Logout', category='', url='/admin/logout'))

# Додаємо в'юхи правильно
admin.add_view(UserView(User, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(FarmView(Farm, db.session))
admin.add_view(SecureModelView(Order, db.session))
admin.add_view(CategoryView(Category, db.session))
admin.add_view(RegionView(Region, db.session))
admin.add_view(TransactionView(Transaction, db.session))
admin.add_view(SecureModelView(CartItem, db.session))
admin.add_view(SecureModelView(OrderItem, db.session))
admin.add_view(SecureModelView(StaticPage, db.session))
admin.add_view(SecureModelView(GlobalSettings, db.session))
admin.add_view(SecureModelView(Translation, db.session))

if __name__ == '__main__':
    print("🚀 Running on http://localhost:5000/admin")
    app.run(host='0.0.0.0', port=5000, debug=False)