from datetime import datetime
from enum import IntEnum
from typing import Dict, Optional, List, Union

from ninja import Schema
from pydantic import BaseModel, Field


### REQUEST SIDE ###

# FEATURES ------

# RETRIEVE
type Feature = Union[str, int, float, List[str], List[int], List[float], None]

class FeatureTypes(IntEnum):
    string = 1
    integer = 2
    float = 3
    array_integer = 4
    array_string = 5
    array_float = 6


class FetchFormat(BaseModel):
    feature_store: str
    features: List[str]
    entity_ids: List[int]


class FetchFeatures(BaseModel):
    fetchables: List[FetchFormat]


# CREATE
class FeatureCreation(BaseModel):
    feature_name: str
    feature_store: str
    datatype: FeatureTypes
    feature_description: Optional[str] = Field(
        default="no description"
    )
    data_source: Optional[str] = Field(
        default="no datasource was provided"
    )


# UPDATE
class FeatureDataUpload(BaseModel):
    feature_store: str
    entity_id: int
    values: Dict[str, Feature]


# FEATURE TABLE CREATION
class FeatureStoreCreation(BaseModel):
    store_name: str
    description: str

# END FEATURES ------



### RESPONSE SIDE ###

# FEATURES ------

class FeatureFetchResponseData(BaseModel):
    table: str
    data: List[Dict[str, Feature]]


class FeatureFetchResponse(BaseModel):
    data: List[FeatureFetchResponseData]


class FeatureCreationResponseData(BaseModel):
    success: bool

# END FEATURES ------

# FEATURE STORE ------

class FeatureStoreCreationResponseData(BaseModel):
    success: bool

# END FEATURE STORE ------


# FEATURE METADATA ------
class FeatureStoreT(Schema):
    feature_store_name: str
    description: str = None
    created: datetime

class FeatureStoreMetadataT(Schema):
    feature_store_name: str

class FeatureMetadataT(Schema):
    feature_name: str
    feature_store: FeatureStoreMetadataT
    datatype: str
    description: str = None

# END FEATURE METADATA ------