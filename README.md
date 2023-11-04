## CPE URI Parser

This Python script is a parser for Common Platform Enumeration (CPE) URI strings. CPE is a structured naming scheme for information technology systems, software, and packages.

### Prerequisites

- Python 3.x

### Usage

To use the CPE URI parser, follow these steps:

1. Clone or download the repository containing the script.

2. Run the script with the CPE URI string as an argument:

   ```
   python3 cpe_parser.py cpe_uri
   ```

   Replace `cpe_uri` with the CPE URI you want to parse.

### Example

```shell
python3 cpe_parser.py cpe:2.3:a:microsoft:internet_explorer:8.0.6001:beta:*:*:*:*:*:*"
```

### Command-Line Options

- `--help`: Display information on how to use the script.

### Features

- Parses CPE URI strings into their components.
- Handles special characters such as asterisk (*) and question mark (?).
- Validates and escapes non-alphanumeric printable characters in attribute values.

### Error Handling

The script provides error handling for various issues that may occur during parsing. It raises exceptions for the following cases:

- Incomplete URI: When the CPE URI has less than 13 attributes.
- Standard Value Error: When there is an issue with the CPE standard value.
- Standard Version Value Error: When there is an issue with the standard version value.
- Part Value Error: When there is an issue with the CPE part value.
- Attribute Value Error: When there is an issue with one or more attribute values.
- Logical Value Error: When there is an issue with logical attribute values.

### License

This script is available under the MIT License.

### Author

[Antonio Daniel Rodriguez-Magierowski]

