import os
import sys

# Додаємо корінь проекту до шляхів
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_admin import Admin
from flask_admin.theme import Bootstrap4Theme
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import FileUploadField
from flask_admin.menu import MenuLink
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from markupsafe import Markup

# Імпортуємо моделі ПІСЛЯ ініціалізації db, щоб уникнути циклічних імпортів
from core.models import User, Product, Order, Category, StaticPage, GlobalSettings, Translation, Farm, Transaction, TransactionType, TransactionStatus, CartItem, OrderItem

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

# Кастомна в'юха для продуктів
class ProductView(SecureModelView):
    column_list = ('id', 'name', 'name_de', 'price', 'unit', 'sku', 'availability_status', 'categories', 'farm', 'image_path')
    column_display_pk = True
    # can_export = True  # Disabled to use custom XLSX export
    column_filters = ['categories', 'farm', 'availability_status']
    column_searchable_list = ['name', 'sku']
    column_sortable_list = ['id', 'name', 'name_de', 'sku', 'price', 'unit', 'availability_status', ('categories', 'categories.name'), ('farm', 'farm.name')]
    column_editable_list = ['price', 'availability_status', 'unit']
    list_template = 'admin/model/product_list.html'
    column_labels = {
        'id': 'ID',
        'name': 'Назва (Укр)',
        'name_de': 'Назва (Нім)',
        'price': 'Ціна',
        'unit': 'Одиниця виміру',
        'sku': 'Артикул (SKU)',
        'availability_status': 'Статус наявності',
        'categories': 'Категорії',
        'farm': 'Ферма/Виробник',
        'image_path': 'Зображення'
    }
    column_formatters = {
        'price': lambda v, c, m, p: f"{m.price:.2f} €".replace('.', ',') if m.price else '0,00 €',
        'image_path': lambda v, c, m, p: Markup(f'<img src="/static/uploads/{m.image_path}" width="50" height="50" alt="No image">') if m.image_path else 'No image'
    }
    form_extra_fields = {
        'image_path': FileUploadField('Зображення', base_path='static/uploads')
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
        'description_de': 'Опис (Нім)',
        'image_path': 'Шлях до зображення'
    }
    column_formatters = {
        'image_path': lambda v, c, m, p: Markup(f'<img src="/static/uploads/{m.image_path}" width="50" height="50" alt="No image">') if m.image_path else 'No image'
    }
    form_extra_fields = {
        'image_path': FileUploadField('Зображення', base_path='static/uploads', allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])
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
        'is_active': 'Активний',
        'image_path': 'Шлях до зображення'
    }
    column_formatters = {
        'image_path': lambda v, c, m, p: Markup(f'<img src="/static/uploads/{m.image_path}" width="50" height="50" alt="No image">') if m.image_path else 'No image'
    }
    form_extra_fields = {
        'image_path': FileUploadField('Зображення', base_path='static/uploads', allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])
    }

# Кастомна в'юха для користувачів
class UserView(SecureModelView):
    column_list = ('id', 'tg_id', 'full_name', 'email', 'username', 'phone', 'is_trusted', 'is_admin', 'language_pref', 'balance', 'created_at')
    column_exclude_list = ['password_hash']  # Hide password hash from list view
    form_excluded_columns = ['password_hash']  # Hide from form, handle separately if needed
    column_labels = {
        'id': 'ID',
        'tg_id': 'Telegram ID',
        'full_name': 'Повне ім\'я',
        'email': 'Email',
        'username': 'Ім\'я користувача',
        'phone': 'Телефон',
        'is_trusted': 'Довірений',
        'is_admin': 'Адмін',
        'language_pref': 'Мова',
        'balance': 'Баланс',
        'created_at': 'Дата створення'
    }

# Кастомна в'юха для транзакцій
class TransactionView(SecureModelView):
    column_list = ('id', 'user', 'amount', 'type', 'status', 'external_id', 'created_at')
    column_labels = {
        'id': 'ID',
        'user': 'Користувач',
        'amount': 'Сума',
        'type': 'Тип',
        'status': 'Статус',
        'external_id': 'Зовнішній ID',
        'created_at': 'Дата створення'
    }
#    </content>
# </xai:function_call name="update_todo_list">
# <parameter name="todos">["Update core/models.py: Create junction table and modify Product/Category relationships", "Create admin/admin_views.py: Move all ModelView classes and LoginForm", "Create admin/routes.py: Move all routes to Blueprint", "Update admin/app.py: Simplify to main entry point only", "Run alembic migration for schema changes", "Create implementation report in docs/reports/"]