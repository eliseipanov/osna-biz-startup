# Sprint 21.11: Fix Telegram ID Overflow in Database Queries

**Issue:** Bot crashes with 'value out of int32 range' because it uses Telegram ID (BigInt) to query columns designed for Internal User ID (Integer).

**Tasks:**

1. **Fix `bot/handlers/store.py`**:
   - In all queries to `CartItem`, ensure you use the internal `User.id` instead of `callback.from_user.id`.
   - Correct logic: 
     1. Fetch user: `user = await session.scalar(select(User).where(User.tg_id == tg_id))`
     2. Use `user.id` for `CartItem` filters.

2. **Audit all handlers**:
   - Ensure `OrderItem`, `Transaction`, and `CartItem` are always linked via internal `User.id`.

**Definition of Done:**
- Users with long Telegram IDs (like 5165519414) can browse the catalog and add items to the cart without database errors.