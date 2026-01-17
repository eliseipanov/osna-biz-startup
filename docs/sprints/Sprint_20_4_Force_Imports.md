# Sprint 20.4: Force Import Sync in admin/app.py

**Context:** The simulation route is still failing with 500 errors because of missing symbols (select, Transaction, etc.).

**Task: Replace Imports**
1. **In `admin/app.py`**, find the Flask imports (around line 10) and ensure they are EXACTLY:
   `from flask import Flask, redirect, url_for, flash, request, render_template, send_file, jsonify`
2. **Find the SQLAlchemy imports** and ensure they are:
   `from flask_sqlalchemy import SQLAlchemy`
   `from sqlalchemy import select`
3. **Find the `core.models` imports** (around line 52) and ensure they include EVERYTHING:
   `from core.models import User, Product, Order, Category, StaticPage, GlobalSettings, Translation, Farm, Transaction, TransactionType, TransactionStatus`

**Task: Function Audit**
1. Ensure the function `paypal_simulate` uses the variable `User` (which is imported) and `Transaction` (which is now imported).
2. Ensure it uses `TransactionType.DEPOSIT` and `TransactionStatus.COMPLETED`.

**Note:** Do NOT attempt to restart the server. Just save the file correctly.