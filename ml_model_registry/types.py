from datetime import datetime
from enum import IntEnum
from typing import Dict, Any, Optional, List, Union

from ninja import Schema
from pydantic import BaseModel, ConfigDict


# Create Expirement and Model
class ModelExpirementInsertT(BaseModel):
    # model metadata specific
    model_name: str
    location: str
    model_description: Optional[str] = None
    # expirement specific
    metrics: Optional[Dict[str, Union[str, int, float, List[str], List[int], List[float]]]] = None
    feature_set: Optional[List[str]] = None
    target_field: Optional[str] = None
    expirement_description: Optional[str] = None

    model_config = ConfigDict(protected_namespaces=())


# Retreive Expirement
class MLModelSchema(Schema):
    model_name: str
    location: str
    description: Optional[str] = None
    created: datetime

    model_config = ConfigDict(protected_namespaces=())


class MLModelExpirementSchema(Schema):
    model: MLModelSchema
    metrics: Optional[Dict[str, Union[str, int, float, List[str], List[int], List[float]]]] = None
    feature_set: Optional[List[str]] = None
    target_field: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(protected_namespaces=())