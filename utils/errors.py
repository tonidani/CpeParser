from typing import Union, List, Dict
from utils.enums import (LogicalValuesEnum, UriStandardValuesEnum, 
                         StandardVersionValuesEnum, PartValuesEnum)


class BaseValueException(Exception):
    def __init__(self, value):
        self.value = value
        self.base_enum_class = None

    def __str__(self) -> str:
        self.message = f"""{self.__class__.__name__}: `{self.value}` allowed values: `{', '.join(self.base_enum_class.allowed_values())}`"""
        return self.message


class IncompleteUriError(BaseValueException):
    def __init__(self, value: str):
        super().__init__(value)
        self.base_enum_class = UriStandardValuesEnum

    def __str__(self):
        self.message = f"""{self.__class__.__name__}: `{self.value}` required attributes: 13"""
        return self.message


class StandardValueError(BaseValueException):
    def __init__(self, value: str):
        super().__init__(value)
        self.base_enum_class = UriStandardValuesEnum


class StandardVersionValueError(BaseValueException):
    def __init__(self, value: str):
        super().__init__(value)
        self.base_enum_class = StandardVersionValuesEnum


class PartValueError(BaseValueException):
    def __init__(self, value: str):
        super().__init__(value)
        self.base_enum_class = PartValuesEnum


class LogicalValueError(BaseValueException):
    def __init__(self, value: str):
        super().__init__(value)
        self.base_enum_class = LogicalValuesEnum


class AttributeValueError(Exception):
    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        self.message = f"""{self.__class__.__name__}: `{self.value}` is an invalid cpe value"""
        return self.message