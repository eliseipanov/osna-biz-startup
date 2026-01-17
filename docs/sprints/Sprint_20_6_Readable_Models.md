# Sprint 20.6: User and Transaction String Representation

**Issue:** 
- In the Admin panel, the User field in the Transactions table shows as `<core.models.User object...>`.
- We need to define how these models are displayed as strings.

**Tasks:**
1. **Update `User` model in `core/models.py`**:
   - Add a `__str__` method:
     ```python
     def __str__(self):
         return f"{self.full_name or self.username} (ID: {self.id})"
     ```
2. **Update `Transaction` model in `core/models.py`**:
   - Add a `__str__` method:
     ```python
     def __str__(self):
         return f"Trans {self.id}: {self.type} ({self.amount}€)"
     ```

**Verification:**
- Save the file.
- Refresh the Admin panel in the browser.
- The Transactions table should now show names/IDs instead of memory addresses.