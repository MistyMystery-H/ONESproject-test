"""User ↔ Team (many-to-many) membership management."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TeamService:
    """In-memory many-to-many membership store."""

    team_members: dict[str, set[str]] = field(default_factory=dict)
    user_teams: dict[str, set[str]] = field(default_factory=dict)

    def add_user_to_team(self, user_id: str, team_id: str) -> None:
        self.team_members.setdefault(team_id, set()).add(user_id)
        self.user_teams.setdefault(user_id, set()).add(team_id)

    def remove_user_from_team(self, user_id: str, team_id: str) -> None:
        if team_id in self.team_members:
            self.team_members[team_id].discard(user_id)
        if user_id in self.user_teams:
            self.user_teams[user_id].discard(team_id)

    def get_team_members(self, team_id: str) -> list[str]:
        return sorted(self.team_members.get(team_id, set()))

    def get_user_teams(self, user_id: str) -> list[str]:
        return sorted(self.user_teams.get(user_id, set()))
