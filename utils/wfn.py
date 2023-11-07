import re

from typing import Union, List, Dict
from utils.errors import (IncompleteUriError, PartValuesEnum,
                          StandardValueError, StandardVersionValueError,
                          PartValueError, LogicalValueError, AttributeValueError)
from utils.enums import (LogicalValuesEnum, UriStandardValuesEnum, 
                         StandardVersionValuesEnum, PartValuesEnum)


# CONSTANS
DELIMITER = r'(?<!\\):'
SPECIAL_CHARACTERS = """!\"#$%&'()*+,/:;<=>?@[]^`{|}~]"""


class WFN:
    def __init__(self, part: Union[PartValuesEnum, None] = None, vendor: Union[str, None] = None,
                 product: Union[str, None] = None, version: Union[str, None] = None,
                 update: Union[str, None] = None, edition: Union[str, None] = None,
                 sw_edition: Union[str, None] = None, target_sw: Union[str, None] = None,
                 targer_hw: Union[str, None] = None, language: Union[str, None] = None,
                 other: Union[str, None] = None):
        self.part = part
        self.vendor = vendor
        self.product = product
        self.version = version
        self.update = update
        self.edition = edition
        self.sw_edition = sw_edition
        self.target_sw = target_sw
        self.targer_hw = targer_hw
        self.language = language
        self.other = other

    def get_attributes(self) -> Dict[str, str]:
        return vars(self).items()
    
    def to_dict(self):
        dict_cpe = '{\n'
        for attribute, value in self.get_attributes():
            dict_cpe += f'"{attribute}":"{value}",\n'
        dict_cpe += '}'
        return dict_cpe

    @classmethod
    def parse(cls, data: str) -> "WFN":
        parts = re.split(DELIMITER, data)
        try:
            assert len(parts) == 13
        except:
            raise IncompleteUriError(len(parts))

        standard, standard_v, part = parts[0], parts[1], parts[2]
        attributes = [attr for attr in parts[3:]]

        try:
            standard = UriStandardValuesEnum(standard)
        except:
            raise StandardValueError(standard)

        try:
            standard_v = StandardVersionValuesEnum(standard_v)
        except:
            raise StandardVersionValueError(standard_v)

        try:
            part = PartValuesEnum(part)
        except:
            raise PartValueError(part)

        validated_attributes_list = [str(part)]

        for attribute in attributes:
            validated_attr = WFN.validate_pattern(attribute)

            if not validated_attr:
                raise AttributeValueError(attribute)
            validated_attributes_list.append(validated_attr)

        return cls(*validated_attributes_list)

    def parse_uri(self) -> str:

        parsed_cpe = f'{UriStandardValuesEnum.CPE.value}:{StandardVersionValuesEnum.NO_VERSION.value}'
        for attribute, value in self.get_attributes():

            if value in LogicalValuesEnum.allowed_values("name"):
                # Parse Logical Values (ANY, NA => * and -)
                final_value_string = getattr(LogicalValuesEnum, value)
            parsed_cpe += f":{final_value_string}"

        return parsed_cpe

    @staticmethod
    def validate_pattern(attribute: str) -> Union[str, LogicalValuesEnum, None]:
        # Logical Values
        if len(attribute) == 1 and attribute in LogicalValuesEnum.allowed_values():
            try:
                attribute = LogicalValuesEnum(attribute)
            except:
                raise LogicalValueError(attribute)

            return attribute.name

        special_characters_to_escape = SPECIAL_CHARACTERS

        if len(attribute) == 1 and attribute in SPECIAL_CHARACTERS:
            return None

        # Looking for \ before a special character
        for index in range(len(attribute)-1):
            char = attribute[index]
            if char in special_characters_to_escape:
                if index - 1 == 0 or attribute[index - 1] != '\\':
                    return None

        # Replace whitespaces
        return attribute
