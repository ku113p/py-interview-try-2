import uuid
from dataclasses import dataclass
from typing import Any, Generic, Type, TypeVar

# Define a TypeVar that represents our Data Objects
T = TypeVar("T")


class BaseModel(Generic[T]):
    _storages: dict[Type, dict[uuid.UUID, Any]] = {}

    @classmethod
    def _get_storage(cls) -> dict[uuid.UUID, T]:
        if cls not in cls._storages:
            cls._storages[cls] = {}
        return cls._storages[cls]

    @classmethod
    def get_by_id(cls, id: uuid.UUID) -> T | None:
        return cls._get_storage().get(id)

    @classmethod
    def list(cls) -> list[T]:
        return list(cls._get_storage().values())

    @classmethod
    def create(cls, id: uuid.UUID, data: T):
        cls._get_storage()[id] = data

    @classmethod
    def update(cls, id: uuid.UUID, data: T):
        cls.create(id, data)

    @classmethod
    def delete(cls, id: uuid.UUID):
        cls._get_storage().pop(id, None)


class UserFilterMixin(Generic[T]):
    @classmethod
    def list_by_user(cls, user_id: uuid.UUID) -> list[T]:
        return [obj for obj in cls.list() if obj.user_id == user_id]


class AreaFilterMixin(Generic[T]):
    @classmethod
    def list_by_area(cls, area_id: uuid.UUID) -> list[T]:
        return [obj for obj in cls.list() if obj.area_id == area_id]


@dataclass
class User:
    id: uuid.UUID
    name: str
    mode: str


@dataclass(frozen=True)
class History:
    id: uuid.UUID
    data: dict
    user_id: uuid.UUID
    created_ts: float


@dataclass
class LifeArea:
    id: uuid.UUID
    title: str
    parent_id: uuid.UUID | None
    user_id: uuid.UUID


@dataclass
class Criteria:
    id: uuid.UUID
    title: str
    area_id: uuid.UUID


@dataclass
class LifeAreaMessage:
    id: uuid.UUID
    data: str
    area_id: uuid.UUID


class UsersManager(BaseModel[User]):
    pass


class HistoryManager(BaseModel[History], UserFilterMixin[History]):
    pass


class LifeAreaManager(BaseModel[LifeArea], UserFilterMixin[LifeArea]):
    pass


class CriteriaManager(BaseModel[Criteria], AreaFilterMixin[Criteria]):
    pass


class LifeAreaMessagesManager(
    BaseModel[LifeAreaMessage], AreaFilterMixin[LifeAreaMessage]
):
    pass
