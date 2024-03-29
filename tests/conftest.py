import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.core.db import get_async_db, Base
from api.main import app


ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
	async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
	async_session = sessionmaker(
		autocommit=False,
		autoflush=False,
		bind=async_engine,
		class_=AsyncSession,
	)
	async with async_engine.begin() as conn:
		await conn.run_sync(Base.metadata.drop_all)
		await conn.run_sync(Base.metadata.create_all)

	async def get_test_db():
		async with async_session() as session:
			yield session

	app.dependency_overrides[get_async_db] = get_test_db

	async with AsyncClient(app=app, base_url="http://test") as client:
		yield client