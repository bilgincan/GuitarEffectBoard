import datetime
from abc import ABC, abstractmethod


class BaseModel(ABC):
    id: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    @abstractmethod
    def reverse_map(base_object):
        pass

    @abstractmethod
    def map(self):
        pass