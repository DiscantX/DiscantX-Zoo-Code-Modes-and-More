# GitHub TestBed Intentional Bug Catalog

This document contains all intentional bugs introduced into the `GitHubTestBed` repository for testing the `GitHub Issue Mode` agent. This file is maintained within the `Modes` repository to keep the execution agent blind to the expected answers during test runs.

---

## Bug Overview & Index

| Bug ID | Target Module | Bug Type | Prompt Title / Area |
| :--- | :--- | :--- | :--- |
| **BUG-1.1** | `config.py` | `TypeError` | Database Port String Concatenation |
| **BUG-1.2** | `config.py` | Logic Override | Environment Var Override Failure |
| **BUG-2.1** | `auth.py` | Off-by-one Error | Password Boundary Validation |
| **BUG-2.2** | `auth.py` | Async / Unawaited Coroutine | Session Fetch Coroutine Return |
| **BUG-3.1** | `database.py` | Resource / Connection Leak | Connection Pool Leak on Exception |
| **BUG-3.2** | `database.py` | Vulnerability / Security | SQL Injection via String Formatting |
| **BUG-4.1** | `api.py` | `KeyError` / `TypeError` | Nested Dict Profile Access |
| **BUG-4.2** | `api.py` | `AttributeError` | Unhandled Null Response Processing |
| **BUG-5.1** | `analytics.py` | `ZeroDivisionError` | Empty Metrics Data List |
| **BUG-5.2** | `analytics.py` | Type Mismatch | String Age Output in Metrics |
| **BUG-6.1** | `utils.py` | Math Logic Defect | Discount Percentage Scale Error |
| **BUG-6.2** | `utils.py` | `IndexError` | ISO Date Time Split Failure |

---

## Detailed Bug Specification & Test Prompts

### 1. `config.py`

#### BUG-1.1: Database Port String Concatenation

* **Location:** `github_testbed/config.py` -> `get_database_url()`
* **Defect:** Concatenates integer `DB_PORT` directly onto a connection string without casting via `str(DB_PORT)`.
* **Test Prompt:**
  > yo config is totally crashing on startup when i try setting DB_PORT=5432 in env. trace says cannot concatenate str and int objects in get_database_url?? please fix fast need to deploy tonight

#### BUG-1.2: Environment Var Override Failure

* **Location:** `github_testbed/config.py` -> `load_config_env()`
* **Defect:** Checks `os.getenv("APP_ENV")`, but an aggressive hardcoded assignment overrides the environment setting back to `"development"`.
* **Test Prompt:**
  > setting APP_ENV=production in environment variables does literally nothing... config always reports environment as development no matter what. check load_config_env implementation cause its ignoring env vars

---

### 2. `auth.py`

#### BUG-2.1: Password Boundary Validation

* **Location:** `github_testbed/auth.py` -> `validate_password_length()`
* **Defect:** Uses `if len(password) > 8:` instead of `>= 8`.
* **Test Prompt:**
  > hey password verification is totally broken. a user is trying to register with a password that is exactly 8 characters long and the system is rejecting it saying it must be at least 8. but 8 is at least 8!! i think someone used a greater than sign instead of greater than or equal to in the validation code please check it immediately

#### BUG-2.2: Session Fetch Coroutine Return

* **Location:** `github_testbed/auth.py` -> `fetch_user_session()`
* **Defect:** Calls `simulate_network_delay()` (`async def`) without an `await` keyword.
* **Test Prompt:**
  > session fetch is weird... user data comes back as <coroutine object simulate_network_delay at 0x7f...> instead of the actual session dict??? probably forgot an await statement somewhere in auth.py when calling network delay

---

### 3. `database.py`

#### BUG-3.1: Connection Pool Leak on Exception

* **Location:** `github_testbed/database.py` -> `get_db_connection()`
* **Defect:** Opens connection context but fails to close or return connection in a `finally:` block when a query error occurs.
* **Test Prompt:**
  > db connections keep maxing out after a few query errors!! someone left the pool connection open when query fails in database.py wrap it in a try finally or something so connection returns to pool even on error

#### BUG-3.2: SQL Injection via String Formatting

* **Location:** `github_testbed/database.py` -> `find_user_by_name()`
* **Defect:** Uses raw f-string formatting (`f"SELECT * FROM users WHERE name='{name}'"`) instead of parameterized binding `(name,)`.
* **Test Prompt:**
  > our security scanner flagged an sql injection vulnerability in database.py in find_user_by_name function. looks like f-string formatting was used directly in the raw sql string instead of parameter bindings please patch

---

### 4. `api.py`

#### BUG-4.1: Nested Dict Profile Access

* **Location:** `github_testbed/api.py` -> `parse_user_payload()`
* **Defect:** Accesses `data["profile"]["settings"]` directly without checking if `"profile"` or `"settings"` exist or are `None`.
* **Test Prompt:**
  > endpoint crashes with 500 when payload is missing optional profile section. parse_user_payload is doing nested dictionary indexing directly without .get() or checking for None please patch so default settings are used if missing

#### BUG-4.2: Unhandled Null Response Processing

* **Location:** `github_testbed/api.py` -> `format_api_response()`
* **Defect:** Calls `response_data.lower()` without checking if `response_data` is `None`.
* **Test Prompt:**
  > api crash on null responses... format_api_response throws AttributeError: 'NoneType' object has no attribute 'lower' when empty payload comes in. add a check for None before calling string methods

---

### 5. `analytics.py`

#### BUG-5.1: Empty Metrics Data List

* **Location:** `github_testbed/analytics.py` -> `calculate_metrics()`
* **Defect:** Divides total sum by `len(data_list)` without guarding against `len(data_list) == 0`, causing `ZeroDivisionError`.
* **Test Prompt:**
  > analytics report generation throws ZeroDivisionError division by zero when data_list is empty. calculate_metrics needs an empty list guard clause to return zeroed metrics instead of exploding

#### BUG-5.2: String Age Output in Metrics

* **Location:** `github_testbed/analytics.py` -> `process_user_ages()`
* **Defect:** Returns average age as a string `"20.0"` rather than a numeric float or integer type.
* **Test Prompt:**
  > assertion error in unit tests for analytics module! result['average'] returns string "20.0" instead of float 20.0 or integer. convert age outputs to actual numeric types in process_user_ages

---

### 6. `utils.py`

#### BUG-6.1: Discount Percentage Scale Error

* **Location:** `github_testbed/utils.py` -> `calculate_discount()`
* **Defect:** Computes `price - (price * percent)` without dividing `percent` by `100`.
* **Test Prompt:**
  > checkout discount calculation is wild a $100 item with a 20 percent discount is coming out as -$1900 dollars lmao... looks like someone forgot to divide percent by 100 in utils.py before subtracting

#### BUG-6.2: ISO Date Time Split Failure

* **Location:** `github_testbed/utils.py` -> `parse_iso_date()`
* **Defect:** Splitting on `"T"` assumes index `1` always exists, throwing an `IndexError` on date-only strings (`"2026-09-06"`).
* **Test Prompt:**
  > parse_iso_date in utils crashes with indexerror list index out of range if someone inputs date without time part like 2026-09-06. split on T needs a check if index 1 exists before accessing