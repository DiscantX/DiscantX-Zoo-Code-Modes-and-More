# Inventory of Intentionally Introduced Bugs

Based on an analysis of the Python implementation files (`analytics.py`, `auth.py`, `database.py`) and unit tests (`test_analytics.py`, `test_database.py`), here is the remaining inventory of intentionally introduced bugs:

## 1. analytics.py

### Unbound Local Variable / Variable Scope Error
* **Function:** `process_user_ages`
* **Location:** Lines 28–29
* **Defect:** `multiplier` is referenced on line 28 (`final_score = total_age * multiplier`) before it is assigned on line 29 (`multiplier = 1.5`), causing an `UnboundLocalError` at runtime.

### Incorrect Division & Return Type
* **Function:** `calculate_metrics`
* **Location:** Line 16
* **Defect:** `average = total // len(data_list)` uses integer floor division (`//`) instead of float division (`/`). Additionally, `test_analytics.py` expects a formatted string `"20.0"` for the average rather than a numeric value, causing `test_calculate_metrics_success` to fail.

### Unhandled ZeroDivisionError
* **Function:** `calculate_metrics`
* **Location:** Line 16
* **Defect:** Passing an empty list `[]` causes `len(data_list)` to be zero, throwing an unhandled `ZeroDivisionError` instead of returning `{ "total": 0, "average": 0 }` as expected by `test_empty_list_handling`.

### Dead Code / Dead None Guard
* **Function:** `format_percentage`
* **Location:** Lines 39–43
* **Defect:** The `if value == None:` check is placed after `value` has already been formatted on line 40 (`formatted = f"{value * 100:.2f}%"`), rendering the guard useless and raising a `TypeError` if `None` is passed.

---

## 2. auth.py

### Hardcoded Secret Token Leak
* **Location:** Line 6
* **Defect:** `SECRET_TOKEN = "super_secret_production_key_12345"` is hardcoded directly in code rather than being fetched securely from environment variables (e.g., via `os.getenv`).

### Unawaited Asynchronous Coroutine
* **Function:** `fetch_user_session`
* **Location:** Line 28
* **Defect:** `session = await simulate_network_delay(user_id)` was missing the `await` keyword, returning an unawaited coroutine object instead of resolving session metadata.

### Strict Inequality Logic Error
* **Function:** `is_password_valid`
* **Location:** Lines 40–44
* **Defect:** In some code states during testing, the check used strict inequality `>` instead of inclusive `>=` (`len(password) >= 8`), causing 8-character valid passwords to be rejected.

---

## 3. database.py

### Duplicate Code & Stale Implementation Drift
* **Location:** Lines 33–64
* **Defect:** `database.py` duplicates utility functions from `auth.py` (`verify_admin`, `fetch_user_session`, `simulate_network_delay`, `is_password_valid`), creating maintainability issues where fixes applied to one file do not apply to the other.

### Resource Leak / Connection Leak on Early Exit
* **Function:** `batch_updates`
* **Location:** Lines 66–77
* **Defect:** Prior to cleanup fixes, returning early upon encountering an unauthorized `"DROP"` query bypassed closing `conn.close()`, leading to leaked active database connections in `ConnectionPool`.
