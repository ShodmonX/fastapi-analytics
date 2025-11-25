from httpx import AsyncClient

async def test_health_check(client: AsyncClient):
    # test health check
    response = await client.get("/")
    assert response.status_code == 200

    # test analytics
    response = await client.get("/analytics/")
    assert response.status_code == 200

    response_with_limit = await client.get("/analytics/?limit=10")
    assert response_with_limit.status_code == 200

    response_with_skip = await client.get("/analytics/?skip=10")
    assert response_with_skip.status_code == 200

    response_with_limit_and_skip = await client.get("/analytics/?limit=10&skip=10")
    assert response_with_limit_and_skip.status_code == 200

    # test analytics post
    response = await client.post("/analytics/", json={"event_type": "login", "user_id": 1})
    assert response.status_code == 201

    response = await client.post("/analytics/", json={"event_type": "logout"})
    assert response.status_code == 422

    # test analytics get by user id
    response = await client.get("/analytics/users/1/")
    assert response.status_code == 200

    # test analytics stats
    response = await client.get("/analytics/stats/")
    assert response.status_code == 200

    # test analytics top events
    response = await client.get("/analytics/top-events/")
    assert response.status_code == 200

    # test analytics last seen
    response = await client.get("/analytics/users/1/last-seen/")
    assert response.status_code == 200