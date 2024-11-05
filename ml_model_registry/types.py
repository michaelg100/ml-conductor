from enum import Enum
from datetime import datetime
from typing import Dict, Optional, List, Union

from ninja import Schema
from pydantic import BaseModel, ConfigDict, Field


class FramworkTypesT(str, Enum):
    Tensorflow = "TENSORFLOW"
    Pytorch = "PYTORCH"
    Scikit = "SCIKIT"


# Create Expirement and Model
class ModelExpirementInsertT(BaseModel):
    # model metadata specific
    model_name: str
    location: str
    model_type: Optional[FramworkTypesT] = FramworkTypesT.Scikit
    model_description: Optional[str] = None
    feature_set: Optional[List[str]] = None
    # expirement specific
    metrics: Optional[Dict[str, Union[str, int, float, List[str], List[int], List[float]]]] = None
    target_field: Optional[str] = None
    expirement_description: Optional[str] = None

    model_config = ConfigDict(protected_namespaces=())


# Retreive Expirement
class MLModelSchema(Schema):
    model_name: str
    location: str
    model_type: Optional[FramworkTypesT] = None
    feature_set: Optional[List[str]] = None
    description: Optional[str] = None
    created: datetime

    model_config = ConfigDict(protected_namespaces=())


class MLModelExpirementSchema(Schema):
    model: MLModelSchema
    metrics: Optional[Dict[str, Union[str, int, float, List[str], List[int], List[float]]]] = None
    target_field: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(protected_namespaces=())