import pytest
import pytest_asyncio
import starlette.status
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create(async_client):
	response = await async_client.post("/tasks", json={"title": "テストタスク"})
	assert response.status_code == starlette.status.HTTP_200_OK
	response_obj = response.json()
	assert response_obj["title"] == "テストタスク"


@pytest.mark.asyncio
async def test_read(async_client, set_task: None):
	response = await async_client.get("/tasks")
	assert response.status_code == starlette.status.HTTP_200_OK
	response_obj = response.json()
	assert len(response_obj) == 1
	assert response_obj[0]["title"] == "テストタスク"
	assert response_obj[0]["done"] is False


@pytest.mark.asyncio
async def test_update(async_client, set_task: None):
    # タスクの更新
    response = await async_client.put("/tasks/1", json={"title": "更新タスク"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "更新タスク"


@pytest.mark.asyncio
async def test_delete_task(async_client, set_task: None):
	# タスクの削除
	response = await async_client.delete("/tasks/1")
	assert response.status_code == starlette.status.HTTP_200_OK


@pytest.mark.asyncio
async def test_update_none_task(async_client):
    # 存在しないタスクの更新
    response = await async_client.put("/tasks/1", json={"title": "更新タスク"})
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND
	

@pytest.mark.asyncio
async def test_delete_none_task(async_client):
	# 存在しないタスクの削除
	response = await async_client.delete("/tasks/1")
	assert response.status_code == starlette.status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_title, expectation",
    [
		("テストタスク", starlette.status.HTTP_200_OK),
		(1, starlette.status.HTTP_422_UNPROCESSABLE_ENTITY),
		(["テストタスク", "テストラスク"], starlette.status.HTTP_422_UNPROCESSABLE_ENTITY),
		({"title": "テストタスク"}, starlette.status.HTTP_422_UNPROCESSABLE_ENTITY),
	]
)
async def test_title_type(async_client, input_title, expectation):
    response = await async_client.post("/tasks", json={"title": input_title})
    assert response.status_code == expectation


@pytest.mark.asyncio
@pytest.mark.parametrize(
	[
		"input_due_date",
        "expectation"
    ],
	[
		("2024-12-01", starlette.status.HTTP_200_OK),
		("2024-12-32", starlette.status.HTTP_422_UNPROCESSABLE_ENTITY),
		("2024/12/01", starlette.status.HTTP_422_UNPROCESSABLE_ENTITY),
		("2024-1201", starlette.status.HTTP_422_UNPROCESSABLE_ENTITY),
	],
)
async def test_due_date_type(async_client, input_due_date, expectation, set_task: None):
	response = await async_client.post("/tasks", json={"due_date": input_due_date})
	assert response.status_code == expectation