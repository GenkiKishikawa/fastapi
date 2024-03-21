from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas.done as done_schema
import api.cruds.done as done_crud
from api.core.db import get_async_db
from api.exceptions.core import APIException
from api.exceptions.error_messages import ErrorMessage


router = APIRouter()


@router.put("/tasks/{task_id}/done", response_model=done_schema.DoneResponse)
async def mark_task_as_done(task_id: int, db: AsyncSession = Depends(get_async_db)):
	done = await done_crud.get_done(db, task_id=task_id)
	if done is not None:
		raise APIException(ErrorMessage.ALREADY_EXISTS("Done"))
	
	return await done_crud.create_done(db, task_id)


@router.delete("/tasks/{task_id}/done", response_model=None)
async def unmark_task_as_done(task_id: int, db: AsyncSession = Depends(get_async_db)):
	done = await done_crud.get_done(db, task_id=task_id)
	if done is None:
		raise APIException(ErrorMessage.ID_NOT_FOUND)
	
	return await done_crud.delete_done(db, original=done)