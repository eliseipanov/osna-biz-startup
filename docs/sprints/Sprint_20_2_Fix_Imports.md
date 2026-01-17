# Sprint 20.2: Final Fix for PayPal Simulation Imports

**Issue:** 
- `POST /webhook/paypal/simulate` returns 500 Error.
- Traceback: `NameError: name 'select' is not defined`.

**Tasks:**
1. **Update Imports in `admin/app.py`**:
   - Ensure `from sqlalchemy import select` is added at the top of the file or within the `paypal_simulate` function scope.
   - Also, double-check that `Transaction`, `TransactionType`, and `TransactionStatus` are correctly imported from `core.models`.

2. **Verify Business Logic**:
   - Ensure the simulation route correctly adds the transaction to the session and commits it.

3. **Verification**:
   - Run the server.
   - Execute the `curl` command.
   - Expect `200 OK` and a JSON response with the new balance.