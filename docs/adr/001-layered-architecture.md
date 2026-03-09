# ADR-001: Layered Architecture Separation

## Status

Accepted

## Context

The VNStock MCP Server needed to evolve from a single-file architecture where all logic was contained in `server.py`. This made the code difficult to test, maintain, and extend as the number of tools grew to 11.

The original structure looked like:

```
src/vnstock_mcp/
├── __init__.py
└── server.py  # All logic in one file (~300+ lines)
```

## Decision

We separated the codebase into three distinct layers:

1. **API Layer** (`server.py`) - Thin MCP tool definitions with `@mcp.tool()` decorators
2. **Service Layer** (`core/`) - Business logic, data fetching, parameter validation
3. **Model Layer** (`models/`) - Result types and data structures

```
src/vnstock_mcp/
├── __init__.py
├── server.py           # API Layer
├── config.py           # Configuration constants
├── exceptions.py       # Custom exceptions
├── core/
│   ├── __init__.py
│   ├── base.py         # BaseService
│   ├── financial.py    # FinancialService
│   ├── company.py      # CompanyService
│   └── fund.py         # FundService
├── models/
│   ├── __init__.py
│   ├── base.py         # ServiceResult, DataFrameResult
│   ├── financial.py    # Financial result types
│   ├── company.py      # Company result types
│   └── fund.py         # Fund result types
└── utils/
    ├── __init__.py
    └── data_transform.py
```

## Rationale

### Separation of Concerns

Each layer has a single responsibility:

| Layer | Responsibility |
|-------|---------------|
| API | MCP protocol handling, tool registration, JSON serialization |
| Service | Business logic, data fetching, validation, transformation |
| Model | Data structures, serialization logic, error states |

### Testability

Services can be unit tested without MCP context:

```python
# Unit test without MCP
async def test_get_income_statement():
    service = FinancialService()
    result = await service.get_income_statement("VCI")
    assert result.success
    assert result.data is not None
```

### Maintainability

- Adding a new tool only requires changes to one layer
- Business logic changes don't affect API contracts
- Result types can be extended independently

### Code Organization

- Related functionality is grouped by domain (financial, company, fund)
- Clear import boundaries prevent circular dependencies
- Each file has a focused purpose

## Consequences

### Positive

- **Testability**: Each layer can be tested independently
- **Maintainability**: Changes are isolated to specific layers
- **Readability**: Code is organized by purpose and domain
- **Extensibility**: Adding new tools or data sources is straightforward

### Negative

- **Complexity**: More files and directories to navigate
- **Indirection**: Following a request requires jumping between files
- **Boilerplate**: Some code is duplicated across result types

## Alternatives Considered

### 1. Keep Single File

Would result in a large, monolithic file that's difficult to navigate and test.

### 2. Feature-Based Organization

Organize by feature (e.g., `financial/`, `company/`, `fund/` with their own service and model). This would create more directories and make shared utilities harder to manage.

## References

- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Python Application Layouts](https://realpython.com/python-application-layouts/)