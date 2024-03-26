import pytest
import pytest_asyncio
import starlette.status

from tests.test_main import async_client


@pytest.mark.asyncio
async def test_create_and_read(async_client):
	response = await async_client.post("/tasks", json={"title": "テストタスク"})
	assert response.status_code == starlette.status.HTTP_200_OK
	response_obj = response.json()
	assert response_obj["title"] == "テストタスク"

	response = await async_client.get("/tasks")
	assert response.status_code == starlette.status.HTTP_200_OK
	response_obj = response.json()
	assert len(response_obj) == 1
	assert response_obj[0]["title"] == "テストタスク"
	assert response_obj[0]["done"] is False


@pytest.mark.asyncio
@pytest.mark.parametrize(
	"input_param, expectation",
	[
		("2024-12-01", starlette.status.HTTP_200_OK),
		("2024-12-32", starlette.status.HTTP_422_UNPROCESSABLE_ENTITY),
		("2024/12/01", starlette.status.HTTP_422_UNPROCESSABLE_ENTITY),
		("2024-1201", starlette.status.HTTP_422_UNPROCESSABLE_ENTITY),
	],
)
async def test_due_date(input_param, expectation, async_client):
	response = await async_client.post("/tasks", json={"title": "テストタスク", "due_date": input_param})
	assert response.status_code == expectation


@pytest.mark.asyncio
async def test_update_task(async_client):
    response = await async_client.post("/tasks", json={"title": "テストタスク3"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "テストタスク3"
    
    # タスクの更新
    response = await async_client.put("/tasks/1", json={"title": "更新タスク"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "更新タスク"
    
    # 存在しないタスクの更新
    response = await async_client.put("/tasks/2", json={"title": "更新タスク"})
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND
    
    
@pytest.mark.asyncio
async def test_delete_task(async_client):
	response = await async_client.post("/tasks", json={"title": "テストタスク4"})
	assert response.status_code == starlette.status.HTTP_200_OK
	response_obj = response.json()
	assert response_obj["title"] == "テストタスク4"
	
	# タスクの削除
	response = await async_client.delete("/tasks/1")
	assert response.status_code == starlette.status.HTTP_200_OK
	
	# 存在しないタスクの削除
	response = await async_client.delete("/tasks/2")
	assert response.status_code == starlette.status.HTTP_404_NOT_FOUND