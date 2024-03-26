import pytest_asyncio


@pytest_asyncio.fixture
async def set_task(async_client) -> None:
    await async_client.post("/tasks", json={"title": "テストタスク"})
    

@pytest_asyncio.fixture
async def set_done(async_client, set_task: None) -> None:
	await async_client.put("/tasks/1/done")