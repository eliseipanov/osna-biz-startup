import pandas as pd
import os
from sqlalchemy import select
from core.database import async_session
from core.models import Product, Category, Farm

# Sync versions for Flask-Admin
def export_products_to_excel_sync(db_session, file_path: str):
    """Sync version for Flask-Admin: Export all products to an Excel file."""
    result = db_session.execute(select(Product))
    products = result.scalars().all()

    data = []
    for p in products:
        data.append({
            'id': p.id,
            'name': p.name,
            'name_de': p.name_de,
            'price': p.price,
            'unit': p.unit,
            'sku': p.sku,
            'availability_status': p.availability_status.value if p.availability_status else None,
            'description': p.description,
            'description_de': p.description_de,
            'category_name': p.category.name if p.category else None,
            'farm_name': p.farm.name if p.farm else None,
            'image_path': p.image_path
        })

    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)
    return f"Exported {len(products)} products to {file_path}"

def import_products_from_excel_sync(db_session, file_path: str):
    """Sync version for Flask-Admin: Import products with atomic transactions."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")

    df = pd.read_excel(file_path)

    report = []
    success_count = 0

    # Use nested transaction for atomicity
    with db_session.begin_nested():
        try:
            for index, row in df.iterrows():
                row_num = index + 2  # Assuming header is row 1
                product_id = row.get('id')
                sku = row.get('sku')
                name = row.get('name')

                # Skip invalid rows
                if pd.isna(product_id) and pd.isna(sku) and pd.isna(name):
                    report.append(f"Row {row_num}: Skipped - no ID, SKU, or Name")
                    continue

                # Find existing product: by id first, then by sku
                existing_product = None
                if not pd.isna(product_id):
                    existing_product = db_session.execute(select(Product).where(Product.id == int(product_id))).scalar_one_or_none()
                if not existing_product and not pd.isna(sku):
                    existing_product = db_session.execute(select(Product).where(Product.sku == str(sku))).scalar_one_or_none()

                try:
                    if existing_product:
                        # Update existing
                        if not pd.isna(row.get('name')):
                            existing_product.name = str(row.get('name'))
                        if not pd.isna(row.get('name_de')):
                            existing_product.name_de = str(row.get('name_de'))
                        if not pd.isna(row.get('price')):
                            existing_product.price = float(row.get('price'))
                        if not pd.isna(row.get('unit')):
                            existing_product.unit = str(row.get('unit'))
                        if not pd.isna(row.get('sku')):
                            existing_product.sku = str(row.get('sku'))
                        if not pd.isna(row.get('description')):
                            existing_product.description = str(row.get('description'))
                        if not pd.isna(row.get('description_de')):
                            existing_product.description_de = str(row.get('description_de'))
                        if not pd.isna(row.get('image_path')):
                            existing_product.image_path = str(row.get('image_path'))
                        report.append(f"Row {row_num}: Updated product {existing_product.name}")
                    else:
                        # Create new
                        if pd.isna(name):
                            raise ValueError("Name is required for new products")
                        new_product = Product(
                            name=str(name),
                            name_de=str(row.get('name_de')) if not pd.isna(row.get('name_de')) else None,
                            price=float(row.get('price')) if not pd.isna(row.get('price')) else 0.0,
                            unit=str(row.get('unit')) if not pd.isna(row.get('unit')) else 'kg',
                            sku=str(row.get('sku')) if not pd.isna(row.get('sku')) else None,
                            description=str(row.get('description')) if not pd.isna(row.get('description')) else None,
                            description_de=str(row.get('description_de')) if not pd.isna(row.get('description_de')) else None,
                            image_path=str(row.get('image_path')) if not pd.isna(row.get('image_path')) else None
                        )
                        db_session.add(new_product)
                        report.append(f"Row {row_num}: Created new product {name}")
                    success_count += 1
                except Exception as e:
                    report.append(f"Row {row_num}: Error - {str(e)}")
                    raise  # Rollback the nested transaction

            # If no errors, commit the nested transaction
            db_session.commit()
            report.insert(0, f"Import successful: {success_count} rows processed")
        except Exception:
            # Rollback will happen automatically
            report.insert(0, "Import failed: rolled back all changes")
            raise

    return "\n".join(report)

async def export_products_to_excel(file_path: str):
    """Export all products to an Excel file."""
    async with async_session() as session:
        result = await session.execute(select(Product))
        products = result.scalars().all()

        data = []
        for p in products:
            data.append({
                'id': p.id,
                'name': p.name,
                'name_de': p.name_de,
                'price': p.price,
                'unit': p.unit,
                'sku': p.sku,
                'availability_status': p.availability_status.value if p.availability_status else None,
                'description': p.description,
                'description_de': p.description_de,
                'category_name': p.category.name if p.category else None,
                'farm_name': p.farm.name if p.farm else None,
                'image_path': p.image_path
            })

        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)
        return f"Exported {len(products)} products to {file_path}"

async def import_products_from_excel(file_path: str):
    """Import products from Excel file with atomic transactions and detailed report."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")

    df = pd.read_excel(file_path)

    async with async_session() as session:
        report = []
        success_count = 0

        # Use nested transaction for atomicity
        async with session.begin_nested():
            try:
                for index, row in df.iterrows():
                    row_num = index + 2  # Assuming header is row 1
                    product_id = row.get('id')
                    sku = row.get('sku')
                    name = row.get('name')

                    # Skip invalid rows
                    if pd.isna(product_id) and pd.isna(sku) and pd.isna(name):
                        report.append(f"Row {row_num}: Skipped - no ID, SKU, or Name")
                        continue

                    # Find existing product: by id first, then by sku
                    existing_product = None
                    if not pd.isna(product_id):
                        existing_product = await session.execute(select(Product).where(Product.id == int(product_id)))
                        existing_product = existing_product.scalar_one_or_none()
                    if not existing_product and not pd.isna(sku):
                        existing_product = await session.execute(select(Product).where(Product.sku == str(sku)))
                        existing_product = existing_product.scalar_one_or_none()

                    try:
                        if existing_product:
                            # Update existing
                            if not pd.isna(row.get('name')):
                                existing_product.name = str(row.get('name'))
                            if not pd.isna(row.get('name_de')):
                                existing_product.name_de = str(row.get('name_de'))
                            if not pd.isna(row.get('price')):
                                existing_product.price = float(row.get('price'))
                            if not pd.isna(row.get('unit')):
                                existing_product.unit = str(row.get('unit'))
                            if not pd.isna(row.get('sku')):
                                existing_product.sku = str(row.get('sku'))
                            if not pd.isna(row.get('description')):
                                existing_product.description = str(row.get('description'))
                            if not pd.isna(row.get('description_de')):
                                existing_product.description_de = str(row.get('description_de'))
                            if not pd.isna(row.get('image_path')):
                                existing_product.image_path = str(row.get('image_path'))
                            report.append(f"Row {row_num}: Updated product {existing_product.name}")
                        else:
                            # Create new
                            if pd.isna(name):
                                raise ValueError("Name is required for new products")
                            new_product = Product(
                                name=str(name),
                                name_de=str(row.get('name_de')) if not pd.isna(row.get('name_de')) else None,
                                price=float(row.get('price')) if not pd.isna(row.get('price')) else 0.0,
                                unit=str(row.get('unit')) if not pd.isna(row.get('unit')) else 'kg',
                                sku=str(row.get('sku')) if not pd.isna(row.get('sku')) else None,
                                description=str(row.get('description')) if not pd.isna(row.get('description')) else None,
                                description_de=str(row.get('description_de')) if not pd.isna(row.get('description_de')) else None,
                                image_path=str(row.get('image_path')) if not pd.isna(row.get('image_path')) else None
                            )
                            session.add(new_product)
                            report.append(f"Row {row_num}: Created new product {name}")
                        success_count += 1
                    except Exception as e:
                        report.append(f"Row {row_num}: Error - {str(e)}")
                        raise  # Rollback the nested transaction

                # If no errors, commit the nested transaction
                await session.commit()
                report.insert(0, f"Import successful: {success_count} rows processed")
            except Exception:
                # Rollback will happen automatically
                report.insert(0, "Import failed: rolled back all changes")
                raise

        return "\n".join(report)