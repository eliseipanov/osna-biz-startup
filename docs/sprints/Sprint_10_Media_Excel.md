# Sprint 10: Media & Data Exchange

Goal: Implement image uploads for core models and create Excel import/export logic.

## 1. Database Updates (core/models.py)
- Add `image_path` field (String 255, nullable) to:
  - Product
  - Category
  - Farm

## 2. Media Infrastructure
- Create directory: `static/uploads/`
- Configure `admin/app.py` to use `FileUploadField` for the new image fields.
- Set base path for uploads to `static/uploads/`.
- Add help text for managers: "Розмір фото буде уточнено пізніше."

## 3. Excel Integration (core/utils/excel_manager.py)
- Dependency: Add `pandas` and `openpyxl` to requirements.txt.
- Implement Export: Function to dump all Products into an .xlsx file.
- Implement Import: Function to read .xlsx and update/create Products.
- Mapping: Use ID or Name as the unique key for updates.

## 4. Migrations
- Generate Alembic migration for the new `image_path` fields.