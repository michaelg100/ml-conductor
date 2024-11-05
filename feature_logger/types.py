from typing import Any, Dict
from pydantic import BaseModel


class FeatureLogT(BaseModel):
    data: Dict[Any, Any]