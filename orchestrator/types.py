from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class RetreivalT(BaseModel):
    """ Necessary for input to Online compute """
    caching: bool = False
    ml_model_name: str
    extra_inputs: Optional[Dict[str, Any]]
    entity_ids = Dict[str, List[int]] # feature store -> ids


class RetreivalResponseT(BaseModel):
    """ Necessary for output from Online compute """
    ml_model_name: str
    response_object: Dict[str, Any]