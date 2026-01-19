#!/usr/bin/env python3
"""
Seed script for Sprint 25 translations.
Adds cart and checkout related translations.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import async_session
from core.models import Translation
from sqlalchemy import select

async def seed_translations():
    """Add or update translations for Sprint 25."""

    translations_data = [
        {
            'key': 'webapp_items_label',
            'value_uk': 'Товарів:',
            'value_de': 'Artikel:'
        },
        {
            'key': 'webapp_view_cart',
            'value_uk': 'До кошика',
            'value_de': 'Zum Warenkorb'
        },
        {
            'key': 'webapp_total_label',
            'value_uk': 'Всього:',
            'value_de': 'Gesamt:'
        },
        {
            'key': 'webapp_checkout_btn',
            'value_uk': 'Оформити замовлення',
            'value_de': 'Bestellen'
        },
        {
            'key': 'webapp_empty_title',
            'value_uk': 'Кошик порожній',
            'value_de': 'Warenkorb leer'
        },
        {
            'key': 'webapp_empty_desc',
            'value_uk': 'Додайте смачненького!',
            'value_de': 'Fügen Sie Produkte hinzu!'
        },
        {
            'key': 'webapp_order_msg_header',
            'value_uk': '✅ Замовлення отримано!',
            'value_de': '✅ Bestellung erhalten!'
        },
        {
            'key': 'webapp_order_msg_contact',
            'value_uk': 'Менеджер зв\'яжеться з вами.',
            'value_de': 'Ein Manager wird Sie kontaktieren.'
        }
    ]

    async with async_session() as session:
        for trans_data in translations_data:
            # Check if translation already exists
            existing = await session.scalar(
                select(Translation).where(Translation.key == trans_data['key'])
            )

            if existing:
                # Update existing translation
                existing.value_uk = trans_data['value_uk']
                existing.value_de = trans_data['value_de']
                print(f"Updated: {trans_data['key']}")
            else:
                # Create new translation
                new_trans = Translation(
                    key=trans_data['key'],
                    value_uk=trans_data['value_uk'],
                    value_de=trans_data['value_de']
                )
                session.add(new_trans)
                print(f"Created: {trans_data['key']}")

        await session.commit()
        print("✅ Sprint 25 translations seeded successfully!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_translations())