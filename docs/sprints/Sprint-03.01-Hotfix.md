
### 📝 Sprint 03.1 - Hotfix

**Problem:**
The bot crashes in `bot/handlers/start.py` with `TypeError: 'async_generator' object does not support the asynchronous context manager protocol`. This happens because `get_session()` is an async generator and cannot be used with `async with` directly in the handler.

**Task:**

1. Rewrite `bot/handlers/start.py`.
2. Do **not** use `async with get_session()`.
3. Instead, inside the handler, get the session like this:
```python
session_gen = get_session()
session = await anext(session_gen)
try:
    # ... your logic with session ...
finally:
    await session_gen.aclose()

```


4. Alternatively (better), rewrite `get_session` in `core/database.py` to be a standard async function or use `async_session()` directly in the handler. **Let's go with the second option: use `async_session()` factory directly in the handler.**

**Revised logic for `bot/handlers/start.py`:**

```python
from core.database import async_session
# ...
async with async_session() as session:
    # database logic here

```

---