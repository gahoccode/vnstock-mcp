# ADR-003: Lazy Import Strategy

## Status

Accepted

## Context

The vnstock library has a complex import structure that can cause circular dependencies and slow startup times when imported at module level. The original implementation had imports at the top of files:

```python
# Module-level imports (problematic)
from vnstock.explorer.vci import Finance, Company
from vnstock.explorer.fmarket.fund import Fund

async def get_income_statement(symbol: str):
    finance = Finance(symbol=symbol)
    # ...
```

This caused:
1. **Circular import errors** between vnstock modules
2. **Slow startup times** as all vnstock modules loaded on server start
3. **Memory overhead** from loading unused modules

## Decision

We moved vnstock imports inside service methods (lazy imports):

```python
async def get_income_statement(self, symbol: str) -> IncomeStatementResult:
    # Lazy import inside method
    from vnstock.explorer.vci import Finance

    finance = Finance(symbol=symbol.upper())
    # ...
```

## Rationale

### Avoiding Circular Dependencies

vnstock's internal module structure can cause circular imports:

```
vnstock.__init__.py
    → vnstock.explorer.vci.__init__.py
        → vnstock.explorer.vci.finance.py
            → vnstock.core.utils.transform.py
                → (potential circular reference back)
```

By importing only when needed, we break these cycles at the application level.

### Faster Startup

With lazy imports, the MCP server starts without loading vnstock modules:

```python
# server.py starts fast
mcp = FastMCP(SERVICE_NAME)  # No vnstock import here

@mcp.tool()
async def get_income_statement(symbol: str) -> str:
    # vnstock loaded only when tool is called
    result = await financial_service.get_income_statement(symbol)
    return result.to_json()
```

### Memory Efficiency

Only the necessary vnstock modules are loaded:

| Tool Called | Modules Loaded |
|-------------|---------------|
| `get_income_statement` | `vnstock.explorer.vci.Finance` |
| `get_fund_listing` | `vnstock.explorer.fmarket.fund.Fund` |
| `get_company_info` | `vnstock.explorer.vci.Company` |

## Consequences

### Positive

- **No Circular Imports**: Avoids vnstock's internal circular dependencies
- **Fast Startup**: Server starts in milliseconds without loading vnstock
- **Memory Efficient**: Only loads modules that are actually used
- **Isolation**: Each service method is self-contained

### Negative

- **Import Overhead on First Call**: First tool call is slightly slower
- **IDE Support**: Some IDEs may not recognize the imports
- **Pattern Discipline**: Developers must remember to use lazy imports

## Implementation Pattern

### Service Layer

```python
# core/financial.py
class FinancialService(BaseService):
    async def get_income_statement(self, symbol: str, lang: str = "en"):
        # Lazy import at method level
        from vnstock.explorer.vci import Finance

        finance = Finance(symbol=symbol.upper())
        df = await self.run_sync(
            lambda: finance.income_statement(period="year", lang=lang)
        )
        # ...
```

### Utils Module

The `utils/data_transform.py` module also uses lazy imports for vnstock utilities:

```python
def flatten_dataframe(df: pd.DataFrame, ...):
    if not isinstance(df.columns, pd.MultiIndex):
        return df

    # Lazy import when actually needed
    from vnstock.core.utils.transform import flatten_hierarchical_index

    return flatten_hierarchical_index(df, ...)
```

## What NOT to Do

```python
# ❌ Module-level import (causes issues)
from vnstock.explorer.vci import Finance

class FinancialService(BaseService):
    async def get_income_statement(self, symbol: str):
        finance = Finance(symbol=symbol)
```

```python
# ✅ Lazy import inside method
class FinancialService(BaseService):
    async def get_income_statement(self, symbol: str):
        from vnstock.explorer.vci import Finance
        finance = Finance(symbol=symbol)
```

## Alternatives Considered

### 1. Import in `__init__.py`

Would load all vnstock modules on any import, defeating the purpose.

### 2. Create a vnstock wrapper module

```python
# lib/vnstock_wrapper.py
from vnstock.explorer.vci import Finance, Company
from vnstock.explorer.fmarket.fund import Fund
```

Would still cause the same circular import issues.

### 3. Use `importlib.import_module()`

```python
import importlib

Finance = importlib.import_module("vnstock.explorer.vci").Finance
```

More verbose with no additional benefit over the standard import statement.

## References

- [Python Import System](https://docs.python.org/3/reference/import.html)
- [Circular Imports in Python](https://stackabuse.com/python-circular-imports/)
- [Lazy Loading in Python](https://pypi.org/project/lazy-import/)