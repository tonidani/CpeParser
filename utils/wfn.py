import re

from typing import Union, List, Dict
from utils.errors import (IncompleteUriError, PartValuesEnum,
                          StandardValueError, StandardVersionValueError,
                          PartValueError, LogicalValueError, AttributeValueError)
from utils.enums import (LogicalValuesEnum, UriStandardValuesEnum, 
                         StandardVersionValuesEnum, PartValuesEnum)


# CONSTANS
DELIMITER = ":"
SPECIAL_CHARACTERS = "!\"#$%&'()*+,/:;<=>?@[]^`{|}~"


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

    @classmethod
    def parse(cls, data: str) -> "WFN":

        # Validation function
        original_uri = data.split(DELIMITER)
        splitted_uri = data.strip().lower().split(DELIMITER)

        try:
            assert len(splitted_uri) == 13
        except:
            raise IncompleteUriError(len(splitted_uri))

        standard, standard_v, part = splitted_uri[0], splitted_uri[1], splitted_uri[2]
        attributes = [attr for attr in splitted_uri[3:]]

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

    def parse_value_backslash(self) -> str:

        parsed_cpe = f'{UriStandardValuesEnum.CPE.value}:{StandardVersionValuesEnum.NO_VERSION.value}'

        for attribute, value in self.get_attributes():

            if value in LogicalValuesEnum.allowed_values("name"):
                # Parse Logical Values (ANY, NA => * and -)
                final_value_string = getattr(LogicalValuesEnum, value)
            else:
                # Define a regular expression pattern to match special characters
                special_char_pattern = r'\\[?*]'

                # Replace escaped special characters with a placeholder to temporarily preserve them
                value_string = re.sub(special_char_pattern, r'PLACE', value)

                # Quote all other non-alphanumeric printable characters except for space
                quoted_value_string = re.sub(r'([^\w\s])', r'\\\1', value)

                # Restore the escaped special characters
                final_value_string = re.sub(
                    r'PLACE', lambda match: '\\' + match.group()[1], quoted_value_string)

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

        special_characters_to_escape = set(SPECIAL_CHARACTERS)

        # Looking for \ before a special character
        for index in range(len(attribute)-1):
            char = attribute[index]
            if char in special_characters_to_escape:
                if index - 1 == 0 or attribute[index - 1] != "\\":
                    return None

        # Replace whitespaces
        attribute = attribute.replace(" ", "_")
        return attribute
