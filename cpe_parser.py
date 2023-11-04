import sys

from typing import List, Union
from utils.errors import (IncompleteUriError, PartValuesEnum,
                          StandardValueError, StandardVersionValueError,
                          PartValueError, LogicalValueError, AttributeValueError)
from utils.wfn import WFN


def commands(args: List) -> Union[None, str]:
    # Check input
    try:
        assert len(args) == 2
    except:
        return "Please provide only one argument with cpe uri string, use --help for more information."

    # Commands
    if args[1] == '--help':
        return f"Script usage:\n python3 {args[0]} <cpe_uri>\n Example: python3 {args[0]} cpe:2.3:a:microsoft:internet_explorer:8.0.6001:beta:*:*:*:*:*:*"

    return None


def print_result(wfn: WFN, uri: str) -> None:
    print("---------------------------------------------")
    print(f"original uri -> {uri}\n")
    print(f'wfn -> {wfn.parse_value_backslash()}\n')
    print(wfn.__dict__)
    print("---------------------------------------------")


def menu():
    args = sys.argv
    command = commands(args)

    if command:
        print(command)
        return

    try:
        uri = args[1]
        wfn = WFN.parse(uri)
        print_result(wfn, uri)

    except (PartValueError, StandardValueError,
            IncompleteUriError, StandardVersionValueError,
            AttributeValueError) as error:
        print(error)

    finally:
        return


if __name__ == "__main__":
    menu()
