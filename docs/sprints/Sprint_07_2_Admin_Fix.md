# Sprint 07.2: Fix Admin Login TypeError
**File:** `/var/www/osna-biz-startup/admin/app.py`

**Task for Kilo Code Agent:**
The `login` route in `admin/app.py` is currently failing with `TypeError: can only concatenate str (not "CSRFTokenField") to str`. This happens because form fields are being concatenated as objects instead of strings or function calls.

1. **Update `login` route:** Modify the string return in the `login()` function. Ensure all `form` fields (like `form.csrf_token`, `form.username`, `form.password`) are either called as functions or wrapped in `str()`.
2. **Proper HTML structure:** Wrap the form in a basic container with CSS for better visibility (Mobile First).

**Code Update (Target block around line 83):**
Replace the return statement with:
```python
        return f'''
        <!DOCTYPE html>
        <html lang="uk">
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: #f4f4f4; }}
                form {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 90%; max-width: 320px; }}
                input {{ width: 100%; padding: 10px; margin: 10px 0; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }}
                button {{ width: 100%; padding: 10px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; }}
            </style>
        </head>
        <body>
            <form method="POST">
                {form.csrf_token()}
                <h3>Osna Farm Admin</h3>
                {form.username(placeholder="TG ID")}
                {form.password(placeholder="Password")}
                <button type="submit">Log In</button>
            </form>
        </body>
        </html>
        '''