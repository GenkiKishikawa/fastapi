from collections.abc import Generator, AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from api.core.config import settings


DB_URL = str(settings.SQLALCHEMY_DATABASE_URI)
ASYNC_DB_URL = str(settings.ASYNC_SQLALCHEMY_DATABASE_URI)


try:
	db_engine = create_engine(DB_URL, echo=True)
	session = sessionmaker(
		autocommit=False,
		autoflush=False,
		bind=db_engine,
	)
except Exception as e:
	print(f"Error: {e}")
	exit(1)


try:
	async_db_engine = create_async_engine(ASYNC_DB_URL, echo=True)
	async_session = sessionmaker(
		autocommit=False,
		autoflush=False,
		bind=async_db_engine,
		class_=AsyncSession
	)
except Exception as e:
	print(f"Error: {e}")
	exit(1)


Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
	db = session()
	try:
		yield db	
	except Exception:
		db.rollback()
	finally:
		db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None, None]:
	async with async_session() as db:
		try:
			yield db
		except Exception:
			await db.rollback()
		finally:
			await db.close()