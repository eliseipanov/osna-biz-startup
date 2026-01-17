# Sprint 21.1: Database for Cart and Order Details

**Context:** We need to track specific products within carts and finalized orders to support weight adjustments.

**Tasks:**
1. **New Model `CartItem` in `core/models.py`**:
   - `id`, `user_id` (FK), `product_id` (FK), `quantity` (Float, default=1.0).
   - Relationships: `User.cart_items`, `Product.cart_items`.

2. **New Model `OrderItem` in `core/models.py`**:
   - `id`, `order_id` (FK), `product_id` (FK), `quantity` (Float), `final_weight` (Float, nullable), `price_at_time` (Float).
   - Relationships: `Order.items`, `Product.order_items`.

3. **Admin UI in `admin/app.py`**:
   - Register `CartItem` and `OrderItem` so they are visible in the Admin Panel.
   - Update `Order` view to show associated `OrderItem`s (if possible via inline or relationship list).

4. **Migration**:
   - `alembic revision --autogenerate -m "Add cart and order items"`
   - `alembic upgrade head`