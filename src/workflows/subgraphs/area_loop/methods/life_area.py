"""Life area CRUD methods."""

import sqlite3
import uuid

from src.infrastructure.db import repositories as db
from src.shared.ids import new_id


def _str_to_uuid(value: str | None) -> uuid.UUID | None:
    if value is None:
        return None
    return uuid.UUID(value)


class LifeAreaMethods:
    @staticmethod
    def list(user_id: str, conn: sqlite3.Connection | None = None) -> list[db.LifeArea]:
        u_id = _str_to_uuid(user_id)
        return [
            obj for obj in db.LifeAreaManager.list(conn=conn) if obj.user_id == u_id
        ]

    @staticmethod
    def get(
        user_id: str, area_id: str, conn: sqlite3.Connection | None = None
    ) -> db.LifeArea:
        u_id = _str_to_uuid(user_id)
        a_id = _str_to_uuid(area_id)

        if u_id is None or a_id is None:
            raise KeyError("user_id and area_id are required")

        area = db.LifeAreaManager.get_by_id(a_id, conn=conn)
        if area is None:
            raise KeyError(f"LifeArea {area_id} not found")

        if area.user_id != u_id:
            raise KeyError(f"LifeArea {area_id} does not belong to user {user_id}")

        return area

    @staticmethod
    def create(
        user_id: str,
        title: str,
        parent_id: str | None = None,
        conn: sqlite3.Connection | None = None,
    ) -> db.LifeArea:
        u_id = _str_to_uuid(user_id)
        p_id = _str_to_uuid(parent_id)

        if u_id is None:
            raise KeyError("user_id is required")

        area_id = new_id()
        area = db.LifeArea(id=area_id, title=title, parent_id=p_id, user_id=u_id)
        db.LifeAreaManager.create(area_id, area, conn=conn)
        return area

    @staticmethod
    def delete(
        user_id: str, area_id: str, conn: sqlite3.Connection | None = None
    ) -> None:
        u_id = _str_to_uuid(user_id)
        a_id = _str_to_uuid(area_id)

        if u_id is None or a_id is None:
            raise KeyError("user_id and area_id are required")

        area = db.LifeAreaManager.get_by_id(a_id, conn=conn)
        if area is None:
            raise KeyError(f"LifeArea {area_id} not found")
        if area.user_id != u_id:
            raise KeyError(f"LifeArea {area_id} does not belong to user {user_id}")

        db.LifeAreaManager.delete(a_id, conn=conn)
