import pytest
import pytest_asyncio
import starlette.status


@pytest.mark.asyncio
async def test_put(async_client, set_task: None):
	# 完了フラグを立てる
	response = await async_client.put("/tasks/1/done")
	assert response.status_code == starlette.status.HTTP_200_OK


@pytest.mark.asyncio
async def test_delete(async_client, set_done: None):
	# 完了フラグを外す
	response = await async_client.delete("/tasks/1/done")
	assert response.status_code == starlette.status.HTTP_200_OK


@pytest.mark.asyncio
async def test_put_already_exists(async_client, set_done: None):
	# 既に完了フラグが立っているので400を返却
	response = await async_client.put("/tasks/1/done")
	assert response.status_code == starlette.status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_delete_none(async_client, set_task: None):
	# 既に完了フラグが外れているので400を返却
	response = await async_client.delete("/tasks/1/done")
	assert response.status_code == starlette.status.HTTP_404_NOT_FOUND