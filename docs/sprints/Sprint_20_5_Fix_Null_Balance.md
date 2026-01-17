# Sprint 20.5: Handle NULL balance for existing users

**Issue:** 
- `POST /webhook/paypal/simulate` returns 500.
- Traceback: `TypeError: unsupported operand type(s) for +=: 'NoneType' and 'float'`.
- Cause: Existing users have `NULL` in the `balance` column.

**Tasks:**
1. **Update `paypal_simulate` function in `admin/app.py`**:
   - Change the line `user.balance += amount` to a safer version:
     `user.balance = (user.balance or 0.0) + amount`
   - This ensures that if the balance is `None`, it is treated as `0.0`.

2. **Data Consistency (Optional but recommended)**:
   - Ensure the transaction is still created and committed correctly.

**Verification:**
- Just save the file.
- The next `curl` should finally return `{"success": true, ...}`.