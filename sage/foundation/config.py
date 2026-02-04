from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App
    app_name: str = "sage-ai"
    environment: str = "local"
    
    # SurrealDB
    surreal_url: str = "ws://localhost:8000/rpc"
    surreal_user: str = "root"
    surreal_pass: str = "root"
    surreal_ns: str = "test"
    surreal_db: str = "test"
    
    # Auth (Surreal JWT)
    # The JWT secret used by SurrealDB to sign tokens
    jwt_secret: str = "super_secret_key_change_me" 
    
    # Opik
    opik_url: str = "http://localhost:5173/api"
    opik_project_name: str = "sage-default"
    
    # OpenAI (via Opik/LangChain)
    openai_api_key: str | None = None
    openai_base_url: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
