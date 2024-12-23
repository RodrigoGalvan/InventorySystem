from enum import Enum
from fastapi import status

class SuccessStatus(Enum):
    OK = status.HTTP_200_OK
    CREATED = status.HTTP_201_CREATED
