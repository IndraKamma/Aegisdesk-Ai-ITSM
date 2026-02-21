from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AegisDesk AI ITSM"
    API_PREFIX: str = "/api"

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    # IMPORTANT: replace these 3 with REAL values from infra/docker-compose.yml
    DB_NAME: str = "aegisdesk"
    DB_USER: str = "aegis"
    DB_PASSWORD: str = "aegis_password"

    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    OLLAMA_BASE_URL: str = "http://localhost:11434"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

settings = Settings()