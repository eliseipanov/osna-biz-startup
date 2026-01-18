import os
import sys
import traceback
from datetime import datetime

# Додаємо корінь проекту до шляхів
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Blueprint, redirect, url_for, flash, request, render_template, send_file, jsonify
import tempfile
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash, check_password_hash

# Import the views and forms
from admin.admin_views import LoginForm
from core.models import User, Transaction, TransactionType, TransactionStatus, Farm, Category, Product, AvailabilityStatus, Region, Translation

# Import shared db instance
from extensions import db, admin

# Create the blueprint
admin_api = Blueprint('admin_api', __name__)

@admin_api.route('/login', methods=['GET', 'POST'])
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
    return render_template('admin/login.html', form=form)

@admin_api.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_api.login'))

@admin_api.route('/admin/export_products')
@login_required
def export_products():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('admin.index'))
    import tempfile
    import os
    from core.utils.excel_manager import export_products_to_excel_sync

    # Find the ProductView instance
    product_view = None
    for view in admin._views:
        if hasattr(view, 'model') and view.model == Product:
            product_view = view
            break

    if product_view:
        # Get filter context from request.args
        v_args = product_view._get_list_extra_args()
        # Use official get_list method with large page_size to get all results
        count, products = product_view.get_list(
            page=0,
            sort_column=v_args.sort,
            sort_desc=v_args.sort_desc,
            search=v_args.search,
            filters=v_args.filters,
            page_size=10000  # Large number to get all matching records
        )
    else:
        products = None

    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        try:
            export_products_to_excel_sync(db.session, tmp.name, products=products)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"products_{timestamp}.xlsx"
            return send_file(tmp.name, as_attachment=True, download_name=filename)
        except Exception as e:
            print(f"Export error: {str(e)}")
            traceback.print_exc()
            flash(f'Помилка експорту: {str(e)}')
            return redirect(url_for('product.index_view'))

@admin_api.route('/admin/import_products', methods=['GET', 'POST'])
@login_required
def import_products():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('admin.index'))
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename.endswith('.xlsx'):
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                file.save(tmp.name)
                try:
                    from core.utils.excel_manager import import_products_from_excel_sync
                    result = import_products_from_excel_sync(db.session, tmp.name)
                    flash(f'Імпорт завершено: {result}')
                except Exception as e:
                    flash(f'Помилка імпорту: {str(e)}')
                finally:
                    os.unlink(tmp.name)
        else:
            flash('Будь ласка, виберіть файл .xlsx')
        return redirect(url_for('product.index_view'))
    return render_template('admin/import_products.html')

@admin_api.route('/webhook/paypal/simulate', methods=['POST'])
def paypal_simulate():
    data = request.get_json()
    if not data or 'user_id' not in data or 'amount' not in data or 'paypal_id' not in data:
        return jsonify({"error": "Invalid data"}), 400

    user_id = data['user_id']
    amount = data['amount']
    paypal_id = data['paypal_id']

    with db.session() as session:
        user = session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Create transaction
        transaction = Transaction(
            user_id=user_id,
            amount=amount,
            type=TransactionType.DEPOSIT,
            status=TransactionStatus.COMPLETED,
            external_id=paypal_id
        )
        session.add(transaction)

        # Update balance
        user.balance = (user.balance or 0.0) + amount

        session.commit()

        return jsonify({"success": True, "new_balance": user.balance})

@admin_api.route('/webapp')
def webapp():
    """Serve the WebApp interface."""
    return render_template('webapp/index.html')

# WebApp API Endpoints
@admin_api.route('/api/ui/translations')
def api_ui_translations():
    """Return all UI translations for the WebApp."""
    lang = request.args.get('lang', 'uk')
    with db.session() as session:
        translations = session.execute(select(Translation)).scalars().all()
        translations_dict = {}
        for trans in translations:
            if lang == 'de' and trans.value_de:
                translations_dict[trans.key] = trans.value_de
            else:
                translations_dict[trans.key] = trans.value_uk or trans.key
        return jsonify(translations_dict)

@admin_api.route('/api/catalog/regions')
def api_regions():
    """Return list of regions for the WebApp."""
    with db.session() as session:
        regions = session.execute(select(Region)).scalars().all()
        regions_data = []
        for region in regions:
            regions_data.append({
                'id': region.id,
                'name': region.name,
                'name_de': region.name_de,
                'slug': region.slug
            })
        return jsonify(regions_data)

@admin_api.route('/api/catalog/farms')
def api_farms():
    """Return list of active farms for the WebApp, optionally filtered by region_id and farm_type."""
    region_id = request.args.get('region_id', type=int)
    farm_type = request.args.get('farm_type', type=str)

    with db.session() as session:
        query = select(Farm).where(Farm.is_active == True)

        if region_id:
            query = query.where(Farm.region_id == region_id)
        if farm_type:
            query = query.where(Farm.farm_type == farm_type)

        farms = session.execute(query).scalars().all()
        farms_data = []
        for farm in farms:
            farms_data.append({
                'id': farm.id,
                'name': farm.name,
                'description_uk': farm.description_uk,
                'description_de': farm.description_de,
                'location': farm.location,
                'contact_info': farm.contact_info,
                'image_path': farm.image_path,
                'region_id': farm.region_id,
                'farm_type': farm.farm_type
            })
        return jsonify(farms_data)

@admin_api.route('/api/catalog/categories')
def api_categories():
    """Return list of categories for the WebApp."""
    with db.session() as session:
        categories = session.execute(select(Category)).scalars().all()
        categories_data = []
        for category in categories:
            categories_data.append({
                'id': category.id,
                'name': category.name,
                'name_de': category.name_de,
                'slug': category.slug,
                'description': category.description,
                'description_de': category.description_de,
                'image_path': category.image_path
            })
        return jsonify(categories_data)

@admin_api.route('/api/catalog/products')
def api_products():
    """Return products for the WebApp, optionally filtered by category_id."""
    category_id = request.args.get('category_id', type=int)

    with db.session() as session:
        query = select(Product).where(Product.availability_status == AvailabilityStatus.IN_STOCK)

        if category_id:
            # Join with categories for filtering
            query = query.join(Product.categories).where(Category.id == category_id)

        products = session.execute(query).scalars().all()
        products_data = []
        for product in products:
            # Get category names
            category_names = [cat.name for cat in product.categories]
            category_names_de = [cat.name_de for cat in product.categories] if product.categories else []

            products_data.append({
                'id': product.id,
                'name': product.name,
                'name_de': product.name_de,
                'price': product.price,
                'unit': product.unit,
                'sku': product.sku,
                'description': product.description,
                'description_de': product.description_de,
                'categories': category_names,
                'categories_de': category_names_de,
                'farm_name': product.farm.name if product.farm else None,
                'farm_name_de': product.farm.name if product.farm else None,  # Assuming farm names are the same
                'image_path': product.image_path
            })
        return jsonify(products_data)