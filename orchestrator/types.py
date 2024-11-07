from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict


class RetreivalT(BaseModel):
    """ Necessary for input to Online compute """
    ml_model_name: str
    caching: bool = False
    log_response: bool = False
    extra_inputs: Optional[Dict[str, Any]] = None
    entity_ids: Dict[str, List[int]] # feature store -> ids

    model_config = ConfigDict(protected_namespaces=())


class ModelResponseT(BaseModel):
    """ Structure for handling model response """
    response_object: Optional[Dict[str, Any]] = {}
    error_object: Optional[Dict[str, str]] = {}


class RetreivalResponseT(BaseModel):
    """ Necessary for output from Online compute """
    ml_model_name: str
    response_object: ModelResponseT
    result_time: datetime

    model_config = ConfigDict(protected_namespaces=())