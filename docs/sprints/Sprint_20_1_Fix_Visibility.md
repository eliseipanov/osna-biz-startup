# Sprint 20.1: Fix PayPal Route and Admin Visibility

**Issue:** 
- Route `/webhook/paypal/simulate` returns 404.
- `balance` field is missing from User view in Admin panel.
- `Transaction` model is not visible in Admin panel.

**Tasks:**
1. **Fix Routing in `admin/app.py`**:
   - Ensure `@app.route('/webhook/paypal/simulate', ...)` is defined **before** the `if __name__ == '__main__':` block.
   - Check if `jsonify` is imported and used for the response.

2. **Update Admin UI in `admin/app.py`**:
   - Find `UserView` class.
   - Add `balance` to `column_list`.
   - Add `balance` to `column_labels`.

3. **Register Transactions in `admin/app.py`**:
   - Create a `TransactionView(SecureModelView)` class.
   - Register it with `admin.add_view(TransactionView(Transaction, db.session))`.

4. **Verification**:
   - After saving, restart the Flask server.
   - Check if the route `POST /webhook/paypal/simulate` returns 200.