from enum import Enum
from typing import List

# ENUMS
class BaseEnum(Enum):

    def __str__(self):
        return self.value

    @classmethod
    def allowed_values(cls, attribute_name: str = "value") -> List[str]:
        assert attribute_name in ["name", "value"]
        return [getattr(enum_values, attribute_name) for enum_values in cls]


class LogicalValuesEnum(BaseEnum):
    ANY = "*"
    NA = "-"


class UriStandardValuesEnum(BaseEnum):
    CPE = "cpe"


class StandardVersionValuesEnum(BaseEnum):
    NO_VERSION = "/"
    VERSION = "2.3"


class PartValuesEnum(BaseEnum):
    APP = "a"
    OS = "o"
    HW = "h"