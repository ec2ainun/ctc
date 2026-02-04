# Project Structure: Sage Service

The `sage` service (Python/FastAPI) is designed to mirror the architectural patterns of the existing `server` (TypeScript/Hono). This ensures cognitive continuity for developers switching between the two services.

## Architecture Mapping

We follow a layered architecture (Separation of Concerns):

| Layer | TypeScript (`server/`) | Python (`sage/`) | Purpose |
| :--- | :--- | :--- | :--- |
| **Foundation** | `server/foundation/` | `sage/foundation/` | Low-level plumbing (Config, DB, Auth, Logger). |
| **Interface** | `server/routes/` | `sage/routes/` | **Controller Layer**. Handles HTTP, Request/Response validation. |
| **Service** | `server/services/` | `sage/services/` | **Business Logic**. Pure logic, agnostic of HTTP/Transport. |
| **Data** | `server/schemas/` | `sage/schemas/` | **Data Models**. Pydantic models (DTOs) for validation. |
| **Adapters** | `server/integrations/` | `sage/integrations/` | **External APIs**. Wrappers for OpenAI, Stripe, Opik, etc. |

## Folder Breakdown

### `sage/`
Root of the Python service.
- **`main.py`**: The application entry point. Wires all components together (Dependency Injection root).
- **`pyproject.toml`**: Dependency management (using `uv`).

### `sage/foundation/`
Infrastructure code that rarely changes.
- **`config.py`**: Environment variable loading using `pydantic-settings`.
- **`database.py`**: Singleton connection management for SurrealDB.
- **`logging.py`**: OpenTelemetry instrumentation setup.
- **`security.py`**: JWT validation middleware (compatible with SurrealDB's signing).

### `sage/routes/`
The API surface area.
- Functions here should be thin wrappers.
- They parse input (using Pydantic), call a Service, and return output.

### `sage/services/`
The "Brain" of the application.
- Contains the actual logic (e.g., LangGraph chains, Agent orchestration).
- Should not depend on FastAPI or HTTP specifics.

### `sage/integrations/`
Anti-corruption layer for external services.
- **`opik_client.py`**: Manages Opik and LLM observability configuration.
