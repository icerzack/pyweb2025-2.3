import os
from pathlib import Path


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Glossary API")
    ENV: str = os.getenv("ENV", "development")

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")

    OPENAPI_URL: str = os.getenv("OPENAPI_URL", "/openapi.json")
    DOCS_URL: str = os.getenv("DOCS_URL", "/docs")
    REDOC_URL: str = os.getenv("REDOC_URL", "/redoc")

    def ensure_data_dir(self) -> Path:
        data_dir = Path(os.getenv("DATA_DIR", "./data")).resolve()
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir


settings = Settings()

