# Family Link Code Review & Analysis

## 1. Main Purpose & Architecture Analysis

### **Primary Purpose**
This is a **Google Family Link automation tool** that allows parents to programmatically manage their children's device restrictions through an unofficial API client. It reverse-engineers Google's Family Link web interface to control app time limits, blocking, and device management.

### **Project Structure**

**Core Modules:**
- **`src/familylink/client.py`** - Main API client (`FamilyLink` class) that handles authentication and all API calls
- **`src/familylink/models.py`** - Pydantic data models for API responses (apps, usage, members, etc.)
- **`src/familylink/cli.py`** - Command-line interface with CSV-based configuration
- **`src/familylink/__init__.py`** - Package entry point, exports `FamilyLink` class

**Configuration Files:**
- **`config.csv`** - App restrictions in tabular format (used by CLI)
- **`.env`** - Environment variables (parent credentials, timezone, etc.)
- **`children_config.json`** - Multi-child JSON configuration (referenced but not implemented)

**Infrastructure:**
- **`pyproject.toml`** - Modern Python packaging with uv dependency management
- **Docker setup** - Containerized deployment with cron scheduling
- **GitHub Actions** - CI/CD pipeline for PyPI publishing

## 2. Data Flow Analysis

### **Authentication Flow:**
1. Extract SAPISID cookie from browser (Firefox/Chrome) or cookie file
2. Generate SAPISIDHASH token using timestamp + SHA1 hash
3. Create HTTP session with Google API headers

### **CLI Workflow:**
```
config.csv → _load_config() → _apply_config() → FamilyLink API calls → Google servers
```

### **API Client Flow:**
```
FamilyLink() → get_members() → find supervised children → get_apps_and_usage() → apply restrictions
```

## 3. Current Functionality (Junior Dev Explanation)

**Think of this as a "remote control" for Google Family Link:**

1. **Authentication**: The app pretends to be a web browser by stealing cookies and creating the right authentication tokens
2. **Discovery**: It finds all your family members and identifies which ones are supervised children
3. **App Management**: It can set time limits, block apps, or allow apps unlimited access
4. **Device Control**: It can lock/unlock devices and set downtime schedules
5. **Configuration**: You define rules in a CSV file (like Excel) with columns for app names, time limits, days, and time ranges
6. **Automation**: The CLI reads your rules and applies them automatically, with a "dry run" mode to preview changes

## 4. Mental Map & Extension Points

### **Entry Points:**
- **CLI**: `python -m familylink.cli config.csv`
- **Library**: `from familylink import FamilyLink`
- **Docker**: Cron-scheduled execution

### **Key Dependencies:**
- **httpx**: HTTP client for API calls
- **pydantic**: Data validation and parsing
- **browser_cookie3**: Cookie extraction from browsers
- **rich**: Pretty CLI output and logging

### **Safe Extension Areas:**
- **New CLI commands**: Add to `src/familylink/cli.py` argument parser
- **New API methods**: Add to `FamilyLink` class in `src/familylink/client.py`
- **New data models**: Add to `src/familylink/models.py`
- **Multi-child support**: Extend CLI to handle JSON config

## 5. Potential Issues & Tech Debt

### **Major Concerns:**
1. **Hardcoded API payloads**: Device control methods use magic JSON arrays that are fragile
2. **Mixed configuration approaches**: CSV (CLI) vs JSON (mentioned but not implemented)
3. **Error handling**: Limited validation of API responses
4. **Authentication fragility**: Relies on browser cookies which can expire

### **Code Quality Issues:**
1. **Inconsistent parameter handling**: Some methods don't use `self._ensure_account_id()` consistently
2. **Magic numbers**: Hardcoded values in device control payloads
3. **Missing validation**: No checks for valid time formats, app names, etc.
4. **Duplicate logic**: `enable_time_limits_device()` just calls `set_time_limits_device()`

### **Missing Features I Notice:**
- Multi-child support in CLI (mentioned in SpecStory files but not implemented)
- Configuration validation
- Better error messages for common failures
- API rate limiting/retry logic

## Questions for Clarification

I notice some discrepancies:

1. **Is there a `main.py` file?** It's referenced in SpecStory files but not provided
2. **Children config JSON**: The `.env` references `children_config.json` but I don't see this implemented in the CLI
3. **Docker environment**: The `docker-compose.yml` still references `CHILD_NAME` but `.env` uses `CHILDREN_CONFIG_FILE`

This is a well-structured project with good separation of concerns. The reverse-engineered API approach is clever, though inherently fragile. Ready to help with any features, refactoring, or bug fixes you'd like to