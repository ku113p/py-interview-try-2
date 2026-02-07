"""Current area management methods."""

import sqlite3
import uuid

from src.infrastructure.db import repositories as db

from .life_area import LifeAreaMethods


def _str_to_uuid(value: str | None) -> uuid.UUID | None:
    if value is None:
        return None
    return uuid.UUID(value)


class CurrentAreaMethods:
    @staticmethod
    def set_current(
        user_id: str, area_id: str, conn: sqlite3.Connection | None = None
    ) -> db.LifeArea:
        """Set an area as the current area for interview."""
        # Verify area exists and belongs to user
        area = LifeAreaMethods.get(user_id, area_id, conn=conn)

        u_id = _str_to_uuid(user_id)
        if u_id is None:
            raise KeyError("Invalid user_id")

        # Get existing user and update current_area_id
        user = db.UsersManager.get_by_id(u_id, conn=conn)
        if user is None:
            raise KeyError(f"User {user_id} not found")

        updated_user = db.User(
            id=user.id,
            name=user.name,
            mode=user.mode,
            current_area_id=area.id,
        )
        db.UsersManager.update(u_id, updated_user, conn=conn)
        return area
