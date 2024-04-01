from typing import Annotated, Any

from pydantic import (
	AnyUrl,
	BeforeValidator,
	PostgresDsn
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(value: Any) -> list[str] | str:
	if isinstance(value, str) and not value.startswith("["):
		return [i.strip() for i in value.split(",")]
	elif isinstance(value, list | str):
		return value
	raise ValueError(value)


class Settings(BaseSettings):
	model_config = SettingsConfigDict(
		env_file=".env", env_ignore_empty=True, extra="ignore"
	)

	POSTGRES_SERVER: str
	POSTGRES_PORT: int = 5432
	POSTGRES_USER: str
	POSTGRES_PASSWORD: str
	POSTGRES_DB: str
	
	@property
	def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
		return MultiHostUrl.build(
			scheme="postgresql+psycopg2",
			username=self.POSTGRES_USER,
			password=self.POSTGRES_PASSWORD,
			host=self.POSTGRES_SERVER,
			port=self.POSTGRES_PORT,
			path=self.POSTGRES_DB
		)

	@property
	def ASYNC_SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
		return MultiHostUrl.build(
			scheme="postgresql+asyncpg",
			username=self.POSTGRES_USER,
			password=self.POSTGRES_PASSWORD,
			host=self.POSTGRES_SERVER,
			port=self.POSTGRES_PORT,
			path=self.POSTGRES_DB
		)


	BACKEND_CORS_ORIGINS: Annotated[
		list[AnyUrl] | str, BeforeValidator(parse_cors)
	] = []


settings = Settings()