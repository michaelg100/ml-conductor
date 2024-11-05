from datetime import datetime
from enum import IntEnum
from typing import Dict, Optional, List, Union

from ninja import Schema
from pydantic import BaseModel, Field


class RetreivalT(BaseModel):
    """ Necessary for input to Online compute """
    caching: bool = False
    pass


class RetreivalResponseT(BaseModel):
    """ Necessary for output from Online compute """
    pass