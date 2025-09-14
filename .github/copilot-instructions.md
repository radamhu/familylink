# GitHub Copilot Instructions for Family Link Project

## Project Context
This is a Google Family Link automation tool that reverse-engineers Google's web API to programmatically manage children's device restrictions. It's built as both a Python library and CLI tool.

## Code Style & Patterns

### Architecture Patterns
- **Single responsibility**: Each module has a clear purpose (client, models, CLI)
- **Pydantic models**: Use for all data validation and API response parsing
- **HTTPX client**: Preferred HTTP library, maintain session state
- **Rich library**: For CLI output formatting and logging
- Try to keep each file under 350 lines. because you run out token limit
- Split logic into smaller parts
- Ask the model to explain what it’s doing — don’t just let it loop on itself
- Guide it. Don’t let it go rogue
- 12 factor, cleand code, design patterns, solid principles

### Naming Conventions
- **Classes**: PascalCase (e.g., `FamilyLink`, `AppUsage`)
- **Methods**: snake_case (e.g., `get_apps_and_usage()`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `BASE_URL`)
- **Private methods**: Leading underscore (e.g., `_ensure_account_id()`)

### Error Handling
- Use `httpx.HTTPStatusError` for API failures
- Validate data with Pydantic models before processing
- Provide meaningful error messages for common authentication issues
- Use `rich.console` for formatted error output in CLI

## Project-Specific Guidelines

### Authentication
- Always use `_ensure_account_id()` for methods requiring account context
- Generate SAPISIDHASH tokens using the established pattern
- Handle cookie expiration gracefully with clear error messages

### API Methods
- Follow the pattern: `def method_name(self, account_id: str = None, **kwargs) -> ModelType:`
- Use type hints for all parameters and return values
- Document API endpoints in docstrings
- Include examples in docstrings for complex methods

### Configuration
- Support both CSV (current CLI) and JSON (future multi-child) formats
- Validate configuration data before applying changes
- Use `dry_run` parameter for preview functionality

### Data Models
- Inherit from `pydantic.BaseModel`
- Use descriptive field names matching API responses
- Include validation for time formats, app names, etc.
- Add `model_config` for alias handling when needed

## Code Examples

### Adding New API Method
```python
def new_api_method(self, account_id: str = None, **kwargs) -> ResponseModel:
    """
    Brief description of what this method does.
    
    Args:
        account_id: Target account (defaults to supervised child)
        **kwargs: Additional parameters
        
    Returns:
        ResponseModel: Parsed API response
        
    Example:
        >>> client = FamilyLink()
        >>> result = client.new_api_method()
    """
    account_id = self._ensure_account_id(account_id)
    # Implementation here
```

### Adding New CLI Command
```python
@click.command()
@click.argument('config_file', type=click.Path(exists=True))
@click.option('--dry-run', is_flag=True, help='Preview changes without applying')
def new_command(config_file: str, dry_run: bool):
    """Brief description of the new command."""
    console.print(f"[blue]Processing {config_file}...")
    # Implementation here
```

### Adding New Pydantic Model
```python
class NewDataModel(BaseModel):
    """Model for API response data."""
    
    field_name: str
    optional_field: Optional[int] = None
    timestamp: datetime
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )
```

## Common Patterns to Follow

### Configuration Loading
- Use `pathlib.Path` for file operations
- Validate configuration format before processing
- Support both relative and absolute paths
- Provide clear error messages for malformed config

### API Payload Construction
- Use dictionaries for request payloads
- Document magic numbers and API-specific values
- Consider creating constants for reusable payload structures

### Time Handling
- Use timezone-aware datetime objects
- Support multiple time format inputs
- Validate time ranges (start < end)

## Testing Guidelines
- Mock HTTP requests using `httpx_mock`
- Test both success and error scenarios
- Include configuration parsing tests
- Test CLI commands with temporary files

## Security Considerations
- Never log authentication tokens or cookies
- Sanitize file paths in CLI
- Validate all user inputs
- Use secure defaults for sensitive operations

## Performance Notes
- Reuse HTTP sessions for multiple API calls
- Cache member/account lookups when possible
- Use async patterns for bulk operations (future enhancement)
- Consider rate limiting for API calls

## Documentation Standards
- Include usage examples in docstrings
- Document API endpoint URLs and methods
- Explain reverse-engineered payload structures
- Provide troubleshooting tips for common issues