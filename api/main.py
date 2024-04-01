from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.core.config import settings
from api.routers import task, done


app = FastAPI()


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
		allow_origins=[
			str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
		],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)


app.include_router(task.router)
app.include_router(done.router)