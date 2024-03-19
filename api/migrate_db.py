from sqlalchemy import create_engine

from api.models.task import Base
from api.core.config import settings

DB_URL = str(settings.SQLALCHEMY_DATABASE_URI)

engine = create_engine(DB_URL, echo=True)


def reset_database():
	Base.metadata.drop_all(bind=engine)
	Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
	reset_database()