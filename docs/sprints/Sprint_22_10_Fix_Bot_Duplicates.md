# Sprint 22.10: Remove Product Duplicates in Bot

**Objective:** Fix the issue where products appear multiple times in a single category list due to Many-to-Many join logic.

## Task 1: Update Product Query in bot/handlers/store.py
- In `show_category_products` handler, find the SQLAlchemy query.
- Use the `.distinct()` method to ensure unique results.
- **Corrected Query example:**
  `select(Product).distinct().join(Product.categories).where(Category.id == category_id)`

## Definition of Done:
- Selecting any category in the bot shows each associated product only ONCE.