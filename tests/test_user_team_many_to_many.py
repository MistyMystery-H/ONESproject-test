import pytest
import requests

BASE_URL = "http://localhost:8080/api"
AUTH_TOKEN = "Bearer fake-token"

@pytest.fixture
def test_users():
    return ["userA", "userB", "userC"]

@pytest.fixture
def test_teams():
    return ["teamX", "teamY"]

def test_user_team_many_to_many(test_users, test_teams):
    # Steps 1-3: establish many-to-many associations
    add_user_to_team("userA", "teamX")
    add_user_to_team("userA", "teamY")
    add_user_to_team("userB", "teamX")

    # Step 4: query members of teamX
    members = get_team_members("teamX")
    assert "userA" in members
    assert "userB" in members

    # Step 5: query teams of userA
    teams = get_user_teams("userA")
    assert "teamX" in teams
    assert "teamY" in teams

def add_user_to_team(user, team):
    resp = requests.post(
        f"{BASE_URL}/teams/{team}/members",
        json={"userId": user},
        headers={"Authorization": AUTH_TOKEN}
    )
    assert resp.status_code in (200, 201)

def get_team_members(team):
    resp = requests.get(
        f"{BASE_URL}/teams/{team}/members",
        headers={"Authorization": AUTH_TOKEN}
    )
    assert resp.status_code == 200
    return [m["id"] for m in resp.json()]

def get_user_teams(user):
    resp = requests.get(
        f"{BASE_URL}/users/{user}/teams",
        headers={"Authorization": AUTH_TOKEN}
    )
    assert resp.status_code == 200
    return [t["name"] for t in resp.json()]
