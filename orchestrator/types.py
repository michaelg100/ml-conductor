from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class RetreivalT(BaseModel):
    """ Necessary for input to Online compute """
    ml_model_name: str
    caching: bool = False
    log_response: bool = False
    extra_inputs: Optional[Dict[str, Any]]
    entity_ids = Dict[str, List[int]] # feature store -> ids


class ModelResponseT(BaseModel):
    """ Structure for handling model response """
    response_object: Dict[str, Any]
    error_object: Dict[str, str]


class RetreivalResponseT(BaseModel):
    """ Necessary for output from Online compute """
    ml_model_name: str
    response_object: ModelResponseT