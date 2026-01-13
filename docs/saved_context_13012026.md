# Osna-biz-startup Project Context Document - January 13, 2026

## Project Overview

**Project Name:** Osnabrück Farm Connect (OFC) 🥩  
**Concept:** A delivery service for local farm products (meat, seasonal vegetables) connecting German farmers with the Ukrainian community within a 50km radius of Osnabrück.  
**Target Audience:** Ukrainian residents in the region, prioritizing simplicity for elderly users ("grandmothers").  
**Primary Language:** Ukrainian (mandatory), German (secondary).  

**Technology Stack:**
- **Backend:** Python 3.11+, SQLAlchemy 2.0 (async), PostgreSQL
- **Bot:** Aiogram 3.x for Telegram integration
- **Admin Panel:** Flask-Admin + Flask-Login
- **Database Tools:** Alembic for migrations, asyncpg for connections
- **Environment:** WSL/Linux (Ubuntu)

**Business Model:**
- Kleinunternehmer status (UStG §19) - no VAT
- Mandatory "Rote Karte" compliance (Belehrung nach §43 IfSG)
- Minimum order: ~25-30€
- Free delivery: from 50-60€ (marketing hook)

## Current Status

The project has progressed through 14 sprints, with core infrastructure completed and advanced features implemented. The system includes a functional Telegram bot MVP, comprehensive admin panel, and robust data management capabilities.

**Database Schema:** Fully implemented with async SQLAlchemy, including all models and relationships.  
**Migrations:** All schema changes up to Sprint 09 applied via Alembic.  
**Authentication:** Dual-mode support (Telegram ID legacy + email/username modern).  
**Multilingual Support:** Ukrainian primary, German secondary across all content.  

## Key Features

### Core Models
- **User:** Telegram ID, email, username, password_hash, admin flags, language preferences
- **Farm:** Producer management with name, descriptions (UK/DE), location, contact info
- **Product:** Catalog items with multilingual names, prices, units (kg/pcs/bundle), SKU, availability status (IN_STOCK/OUT_OF_STOCK/ON_REQUEST), category/farm relationships
- **Category:** Product categorization with multilingual support
- **Order:** Order management with status workflow (NEW/VERIFIED/PROCUREMENT/IN_DELIVERY/COMPLETED/CANCELLED)
- **StaticPage:** CMS for Impressum/Data Policy pages
- **Translation:** Centralized multilingual content management
- **GlobalSettings:** System-wide configuration

### Telegram Bot (MVP)
- `/start`: Automatic user registration/update with keyboard navigation
- Catalog display with available products
- Main menu: Catalog, Cart, Orders, Profile buttons (UI implemented, handlers pending)

### Admin Panel
- Full CRUD for all models
- Secure authentication with password hashing
- Multilingual UI with UK/DE content editing
- Image upload support for products, categories, farms
- Excel import/export functionality
- Professional UI with proper string representations

### Advanced Features
- **SKU Logic:** Automated generation using category-farm-ID format (e.g., PORK-OSNA-001)
  - Prefixes derived from German category names and farm names
  - Script: `scripts/generate_sku.py` for bulk SKU assignment
- **Excel Functionality:** Comprehensive import/export via `core/utils/excel_manager.py`
  - Sync/async versions for Flask-Admin compatibility
  - Atomic transactions with rollback on errors
  - Matching by ID, SKU, or name
  - Handles encoding for SQL_ASCII database
  - Detailed reporting for import operations
- **Media Management:** Image uploads stored in `static/uploads/` with thumbnail previews
- **Data Safety:** Nested transactions, input validation, relationship linking by name

## Recent Changes

### Sprint 09: Farms & Availability (Completed)
- Added Farm model for producer management
- Enhanced Product model with farm_id, sku, unit, availability_status enum
- Updated admin UI with farm dropdowns and new fields
- Implemented availability states replacing boolean flags

### Sprint 10: Media & Excel (Completed)
- Added image_path fields to Product, Category, Farm models
- Created upload directory structure
- Initial Excel export/import logic with pandas

### Sprint 11: Robust Admin (Completed)
- Moved inline HTML to templates
- Added image thumbnails and filters
- Implemented atomic Excel imports with detailed reporting

### Sprint 12: Excel Exchange (Completed)
- Replaced CSV with XLSX format
- Integrated Excel manager into admin UI
- Added import buttons above product table

### Sprint 13: Async Context Fixes (Completed)
- Fixed greenlet errors in Excel operations
- Resolved image rendering issues with MarkupSafe
- Cleaned up template logic

### Sprint 14: Import Polish (In Progress)
- Enhanced relationship linking by name during import
- Improved SQL_ASCII encoding handling
- Better availability status mapping

## Next Steps

### High Priority
1. **Complete Bot Handlers:** Implement Cart, Orders, Profile functionality
2. **Order Workflow:** Add status management in admin panel
3. **Static Pages:** Complete Impressum/Data Policy CMS

### Medium Priority
1. **Web Frontend:** Simplified registration/checkout outside Telegram
2. **Testing:** End-to-end bot and admin testing
3. **Performance:** Optimize database queries and async operations

### Low Priority
1. **Error Handling:** Comprehensive exception management
2. **Documentation:** API docs and user guides
3. **Analytics:** Reporting and metrics dashboard

## Technical Details

### SKU Generation Logic
```python
def slugify(text: str) -> str:
    return text.strip().upper()[:4].replace(" ", "")

# Format: CATEGORY-FARM-ID (e.g., PORK-OSNA-001)
cat_prefix = slugify(category.name_de or "MEAT")
farm_prefix = slugify(farm.name or "OSNA")
sku = f"{cat_prefix}-{farm_prefix}-{product.id:03d}"
```

### Excel Manager Key Features
- **Export:** Dumps all products with relationships to XLSX
- **Import:** Updates existing or creates new products
- **Matching:** ID > SKU > Name priority
- **Safety:** Nested transactions, detailed error reporting
- **Encoding:** Handles SQL_ASCII database charset

### Sprint Progress Summary
- **Sprints 1-7:** Core infrastructure, bot MVP, admin panel
- **Sprints 8-9:** Multilingual CMS, farm management
- **Sprints 10-14:** Media, Excel integration, UI polish
- **Total Progress:** ~85% complete, production-ready core features

This document serves as a comprehensive reference for future development, capturing the current state and technical architecture of the Osna-biz-startup project.