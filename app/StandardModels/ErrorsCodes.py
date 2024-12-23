from enum import Enum, IntEnum
from fastapi import status

class ErrorResponse(Enum):
    PRICE_NEGATIVE = "Price cannot be negative"
    STOCK_NEGATIVE = "Stock cannot be negative"
    PAGINATION_INVALID = "Pagination is not valid"
    PRODUCT_NOT_FOUND = "The id of the product does not exist. Try using a valid id"
    INTERNAL_SERVER_ERROR = "Internal server error"
    CATEGORY_NOT_FOUND = "The id of the category does not exist. Try using a valid id"
    PRODUCT_IN_STOCK = "The product is in stock. Cannot delete"
    ERROR_DELETING_PRODUCT = "Error while deleting the product"
    STORE_NOT_FOUND = "The id of the store does not exist. Try using a valid id"
    STOCK_INSUFICIENT = "The stock is insufficient. Cannot transfer"
    ERROR_DELETING_INVENTORY = "Error while deleting the inventory"
    ERROR_CREATING_PRODUCT = "Error while creating the product"
    ERROR_TRANSFERRING_INVENTORY = "Error while transferring the product"
    ERROR_UPDATING_PRODUCT = "Error while updating the product"

class ErrorStatus(IntEnum):
    BAD_REQUEST = status.HTTP_400_BAD_REQUEST
    NOT_FOUND = status.HTTP_404_NOT_FOUND
    INTERNAL_SERVER_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR
    NO_CONTENT = status.HTTP_204_NO_CONTENT
