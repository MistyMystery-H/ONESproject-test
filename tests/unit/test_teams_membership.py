"""Unit tests for ones.teams (User ↔ Team many-to-many)."""

from ones.teams import TeamService


def test_user_team_many_to_many():
    svc = TeamService()
    svc.add_user_to_team("userA", "teamX")
    svc.add_user_to_team("userA", "teamY")
    svc.add_user_to_team("userB", "teamX")

    members = svc.get_team_members("teamX")
    assert "userA" in members
    assert "userB" in members

    teams = svc.get_user_teams("userA")
    assert "teamX" in teams
    assert "teamY" in teams
