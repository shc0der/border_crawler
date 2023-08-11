from abc import ABC
from typing import Union, Dict, Any

from pydantic import BaseModel


class BaseDao(ABC):
    @staticmethod
    def _obtain_update(body: Union[BaseModel, Dict[str, Any]]) -> Dict[str, Any]:
        return body if isinstance(body, dict) else body.model_dump(exclude_unset=True)
