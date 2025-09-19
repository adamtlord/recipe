# Test Suite Documentation

This directory contains comprehensive unit and integration tests for the Recipe API application.

## Test Structure

```
tests/
├── conftest.py                    # Shared fixtures and configuration
├── unit/                          # Unit tests (fast, isolated)
│   ├── api/                       # API endpoint tests
│   ├── core/                      # Core functionality tests
│   ├── models/                    # Model and schema tests
│   └── services/                  # Service layer tests
├── integration/                   # Integration tests (slower, end-to-end)
└── fixtures/                      # Test data and fixtures
```

## Running Tests

### Using the Test Runner Script

```bash
# Run all tests
python run_tests.py all

# Run only unit tests (fast)
python run_tests.py unit

# Run only integration tests
python run_tests.py integration

# Run tests with coverage report
python run_tests.py coverage

# Run fast tests (unit tests without slow markers)
python run_tests.py fast
```

### Using pytest directly

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/api/test_recipes_api.py

# Run tests with specific marker
pytest -m unit

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run tests in verbose mode
pytest -v

# Run tests and stop on first failure
pytest -x
```

## Test Categories

### Unit Tests (`@pytest.mark.unit`)
- **Fast execution** (< 1 second per test)
- **Isolated** - no external dependencies
- **Mocked dependencies** - external services are mocked
- **Comprehensive coverage** of individual components

### Integration Tests (`@pytest.mark.integration`)
- **End-to-end testing** of complete workflows
- **Real database** operations (in-memory SQLite)
- **Full API testing** with actual HTTP requests
- **Slower execution** but more realistic

## Test Coverage

The test suite covers:

### Models & Schemas
- ✅ Database model validation
- ✅ Pydantic schema validation
- ✅ Data serialization/deserialization

### Services
- ✅ Recipe generation service
- ✅ Food search service
- ✅ Error handling and edge cases

### API Endpoints
- ✅ Request validation
- ✅ Response formatting
- ✅ Error responses
- ✅ HTTP status codes

### Database Operations
- ✅ CRUD operations
- ✅ Search functionality
- ✅ Data import/export
- ✅ Connection management

### Configuration
- ✅ Settings validation
- ✅ Environment variable handling
- ✅ Default values

## Writing New Tests

### Unit Test Example

```python
@pytest.mark.unit
class TestMyService:
    def test_my_method_success(self):
        # Arrange
        service = MyService()

        # Act
        result = service.my_method("input")

        # Assert
        assert result == "expected_output"

    def test_my_method_error(self):
        with pytest.raises(ValueError):
            service.my_method(None)
```

### Integration Test Example

```python
@pytest.mark.integration
class TestMyAPI:
    def test_endpoint_integration(self, test_client):
        response = test_client.post("/api/v1/endpoint", json={"data": "value"})

        assert response.status_code == 200
        assert response.json()["result"] == "expected"
```

## Fixtures

### Available Fixtures

- `test_client` - FastAPI test client with test database
- `test_session` - Database session for testing
- `populated_test_session` - Session with sample data
- `sample_food_data` - Sample food items for testing
- `sample_recipe_request` - Sample recipe request data
- `sample_recipes` - Sample recipe data

### Using Fixtures

```python
def test_with_fixture(test_client, sample_food_data):
    response = test_client.get("/api/v1/foods")
    assert response.status_code == 200
```

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Clear Naming**: Test names should describe what they test
3. **Arrange-Act-Assert**: Structure tests clearly
4. **Mock External Dependencies**: Don't rely on external services
5. **Test Edge Cases**: Include error conditions and boundary values
6. **Keep Tests Fast**: Unit tests should run quickly
7. **Use Fixtures**: Share common test data and setup

## Continuous Integration

The test suite is designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions step
- name: Run Tests
  run: |
    pip install -r requirements.txt
    python run_tests.py all
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're running tests from the project root
2. **Database Issues**: Tests use in-memory SQLite, no setup required
3. **Mock Failures**: Check that mocks are properly configured
4. **Slow Tests**: Use `pytest -m "not slow"` to skip slow tests

### Debug Mode

```bash
# Run tests with debug output
pytest -v -s

# Run single test with debug
pytest tests/unit/api/test_recipes_api.py::TestRecipesAPI::test_generate_recipes_success -v -s
```
