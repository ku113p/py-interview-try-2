"""Criteria CRUD methods."""

import sqlite3
import uuid

from src.infrastructure.db import repositories as db
from src.shared.ids import new_id

from .life_area import LifeAreaMethods


def _str_to_uuid(value: str | None) -> uuid.UUID | None:
    if value is None:
        return None
    return uuid.UUID(value)


class CriteriaMethods:
    @staticmethod
    def list(
        user_id: str, area_id: str, conn: sqlite3.Connection | None = None
    ) -> list[db.Criteria]:
        area = LifeAreaMethods.get(user_id, area_id, conn=conn)

        return [
            obj for obj in db.CriteriaManager.list(conn=conn) if obj.area_id == area.id
        ]

    @staticmethod
    def delete(
        user_id: str, criteria_id: str, conn: sqlite3.Connection | None = None
    ) -> None:
        u_id = _str_to_uuid(user_id)
        c_id = _str_to_uuid(criteria_id)
        if u_id is None or c_id is None:
            raise KeyError("user_id and criteria_id are required")
        criteria = db.CriteriaManager.get_by_id(c_id, conn=conn)
        if criteria is None:
            raise KeyError(f"Criteria {criteria_id} not found")
        area = LifeAreaMethods.get(user_id, str(criteria.area_id), conn=conn)
        if area.user_id != u_id:
            raise KeyError(f"Criteria {criteria_id} does not belong to user {user_id}")
        db.CriteriaManager.delete(c_id, conn=conn)

    @staticmethod
    def create(
        user_id: str,
        area_id: str,
        title: str,
        conn: sqlite3.Connection | None = None,
    ) -> db.Criteria:
        area = LifeAreaMethods.get(user_id, area_id, conn=conn)

        criteria_id = new_id()
        criteria = db.Criteria(id=criteria_id, title=title, area_id=area.id)
        db.CriteriaManager.create(criteria_id, criteria, conn=conn)
        return criteria
