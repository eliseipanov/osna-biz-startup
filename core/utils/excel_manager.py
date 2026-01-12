import pandas as pd
import os
from sqlalchemy import select
from core.database import async_session
from core.models import Product, Category, Farm

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
    """Import products from Excel file, updating existing or creating new."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")

    df = pd.read_excel(file_path)

    async with async_session() as session:
        updated = 0
        created = 0

        for _, row in df.iterrows():
            product_id = row.get('id')
            name = row.get('name')

            if pd.isna(product_id) and pd.isna(name):
                continue  # Skip invalid rows

            # Try to find existing product by ID or name
            existing_product = None
            if not pd.isna(product_id):
                existing_product = await session.execute(select(Product).where(Product.id == int(product_id)))
                existing_product = existing_product.scalar_one_or_none()
            if not existing_product and not pd.isna(name):
                existing_product = await session.execute(select(Product).where(Product.name == str(name)))
                existing_product = existing_product.scalar_one_or_none()

            if existing_product:
                # Update existing
                existing_product.name_de = row.get('name_de') if not pd.isna(row.get('name_de')) else existing_product.name_de
                existing_product.price = float(row.get('price')) if not pd.isna(row.get('price')) else existing_product.price
                existing_product.unit = row.get('unit') if not pd.isna(row.get('unit')) else existing_product.unit
                existing_product.sku = row.get('sku') if not pd.isna(row.get('sku')) else existing_product.sku
                existing_product.description = row.get('description') if not pd.isna(row.get('description')) else existing_product.description
                existing_product.description_de = row.get('description_de') if not pd.isna(row.get('description_de')) else existing_product.description_de
                existing_product.image_path = row.get('image_path') if not pd.isna(row.get('image_path')) else existing_product.image_path
                # Note: category and farm not updated for simplicity
                updated += 1
            else:
                # Create new (basic, without category/farm for now)
                new_product = Product(
                    name=str(name),
                    name_de=row.get('name_de') if not pd.isna(row.get('name_de')) else None,
                    price=float(row.get('price')) if not pd.isna(row.get('price')) else 0.0,
                    unit=row.get('unit') if not pd.isna(row.get('unit')) else 'kg',
                    sku=row.get('sku') if not pd.isna(row.get('sku')) else None,
                    description=row.get('description') if not pd.isna(row.get('description')) else None,
                    description_de=row.get('description_de') if not pd.isna(row.get('description_de')) else None,
                    image_path=row.get('image_path') if not pd.isna(row.get('image_path')) else None
                )
                session.add(new_product)
                created += 1

        await session.commit()
        return f"Imported: {created} created, {updated} updated"