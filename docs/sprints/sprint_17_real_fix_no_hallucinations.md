## Sprint 17: Fix Hallucinated Method and Implement Real Filter Capture

**Issue:**
The previous sprint failed because `get_filters_arg()` is not a valid Flask-Admin method. This was an error in the instructions. We must use the actual internal methods to capture the filter state.

**Requirements:**
1. **Remove Hallucinated Method:** In `admin/app.py`, remove the call to `view.get_filters_arg()`.
2. **Correct Argument Capture:**
   - Flask-Admin captures filters, search, and sort through `view._get_list_extra_args()`.
   - The correct call to get the filtered data is:
     `view_args = product_view._get_list_extra_args()`
     `count, products = product_view.get_list(page=0, sort_column=view_args.sort_column, sort_desc=view_args.sort_desc, search=view_args.search, filters=view_args.filters, page_size=9999)`
3. **Robustness:** This approach uses the internal `view_args` object that Flask-Admin itself uses to render the table.

**Task for Agent Kilo:**
- Refactor the `export_products` route in `admin/app.py`.
- Use `product_view._get_list_extra_args()` to gather all active UI states.
- Pass these parameters into `get_list` to fetch the correct records.