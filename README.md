# ISC-Multiplex-Source

This Python script updates JSON objects based on data from a CSV file and a static configuration JSON file, with support for type validation and flexible operations.

- **Author**: Pavankalyan D.
- **Date**: 2025-02-21
- **Version**: 1.0

## Features

1. **CSV-Based Updates**:

   - Updates JSON fields using data from a CSV file.
   - Validates and preserves existing data types (e.g., int, bool, list).
   - Creates missing paths with inferred types if they don’t exist.

2. **Static Configuration Updates**:

   - Supports two operations:
     - `update`: Adds or updates fields with type validation.
     - `remove`: Deletes specified keys or list indices.
   - Creates new paths as needed for `update` operations.

3. **Execution Flow**:

   - Applies CSV updates first, followed by static config updates.

4. **Type Safety**:

   - Ensures type consistency between existing JSON values and new updates.
   - Logs warnings for type mismatches without forcing invalid updates.

5. **Logging**:
   - Detailed logging for debugging, including updates, creations, removals, and errors.

## Requirements

- Python 3.6+
- Required package: `jsonpath_ng`
  - Install via: `pip install jsonpath-ng`

## Files

- `script.py`: The main Python script.
- `input.json`: The input JSON file to be updated (example provided).
- `updates.csv`: CSV file with update data (example provided).
- `mapping.json`: JSON file mapping CSV columns to JSONPaths (example provided).
- `static_config.json`: JSON file with static updates/removals (example provided).

## Usage

### Command-Line Syntax

```bash
python script.py -j <input.json> -c <updates.csv> -m <mapping.json> -s <static_config.json> [-o <output.json>]
```

- **-j, --json-file**: Input JSON file (required).
- **-c, --csv-file**: CSV file with updates (required).
- **-m, --mapping-file**: JSON file mapping CSV columns to JSONPaths (required).
- **-s, --static-file**: Static config JSON file with operations (required).
- **-o, --output-file**: Output JSON file (optional, defaults to input file).

## File Formats

### Input JSON (`input.json`)

A single JSON object or a list of objects. Example:

```json
{
  "id": "5961b4af88c94ab285d07a36323f5548",
  "description": "Visual Graphics",
  "connectorAttributes": {
    "formPath": null
  },
  "features": ["NO_RANDOM_ACCESS", "DIRECT_PERMISSIONS"]
}
```

### CSV File (`updates.csv`)

Contains update data with an **"ID"** column for matching. Example:

```
ID,DESCRIPTION,OWNER_TYPE
5961b4af88c94ab285d07a36323f5548,Omini,IDENTITY
```

### Mapping File (`mapping.json`)

Maps CSV columns to JSONPaths. Example:

```json
{
  "DESCRIPTION": "$.description",
  "OWNER_TYPE": "$.owner.type"
}
```

### Static Config File (`static_config.json`)

A list of operations. Example:

```json
[
  {
    "path": "$.description",
    "operation": "update",
    "value": "Updated Description"
  },
  { "path": "$.connectorAttributes.formPath", "operation": "remove" },
  { "path": "$.features[0]", "operation": "remove" }
]
```

## Example Command

```bash
python script.py -j input.json -c updates.csv -m mapping.json -s static_config.json -o output.json
```

### Output

The script:

1. Updates `$.description` from CSV to "Omini".
2. Updates `$.description` from static config to "Updated Description".
3. Removes `$.connectorAttributes.formPath`.
4. Removes the first element of `$.features`.
5. Saves the result to `output.json`.

## How It Works

1. **Load Data**:
   - Reads the input JSON, CSV, mapping, and static config files.
2. **CSV Updates**:
   - Matches JSON objects by "ID" with CSV rows.
   - Updates fields using the mapping, validating types against existing values or inferring for new paths.
3. **Static Config Updates**:
   - Processes each entry in the static config:
     - **update**: Adds/updates the path with the given value, checking types.
     - **remove**: Deletes the key or array element at the specified path.
4. **Save Output**:
   - Writes the updated JSON to the output file with pretty-printing.

## Limitations

- **Simple Matching**:
  Only matches by "ID" in CSV and "id" in JSON. Multi-field matching isn’t supported without code changes.
- **Type Inference**:
  New fields from CSV default to strings if no existing value exists, which may not always be desired.
- **Static Config Overwrites**:
  `update` operations overwrite values; merging (e.g., appending to lists) isn’t supported.
- **Removal Constraints**:
  `remove` works only for direct keys or list indices; complex JSONPath filters (e.g., `$.features[?(@ == "value")]`) aren’t supported.
- **No Rollback**:
  Partial failures leave the JSON in an inconsistent state without automatic rollback.
- **Performance**:
  May be slow for very large JSON or CSV files due to JSONPath parsing overhead.
- **Error Handling**:
  Non-critical errors (e.g., type mismatches) are logged and skipped, potentially missing updates silently.
- **CSV Header Validation**:
  Doesn’t enforce that all mapped columns exist in the CSV header.

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install dependencies**:
   ```bash
   pip install jsonpath-ng
   ```

## Contributing

Feel free to submit issues or pull requests for bug fixes, feature enhancements (e.g., merge support, multi-field matching), or performance improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

````
(.venv) pavankalyandosa@MacBookAir ISC_Multiplex % javac Sample.java
(.venv) pavankalyandosa@MacBookAir ISC_Multiplex % java Sample.java
```markdown
# JSON Updater Script

This Python script updates JSON files using data from a CSV file and a static configuration JSON file. It supports type validation, automatic path creation, and two operations for static config updates: **update** (add/update) and **remove** (delete keys). The script is ideal for managing structured JSON data with external updates while preserving type consistency.

## Features

- **CSV Updates**: Updates JSON fields based on CSV data, matching by an "ID" field, with type validation against existing values.
- **Static Config Updates**: Applies changes from a static JSON config, supporting:
  - **update**: Adds or updates fields with type checking.
  - **remove**: Deletes specified keys or array elements.
- **Execution Flow**: Applies CSV updates first, followed by static config updates.
- **Type Safety**: Ensures data types match existing JSON values before updating.
- **Path Creation**: Automatically creates missing paths for new fields.
- **Logging**: Detailed logs for debugging and tracking changes.

## Requirements

- Python 3.6+
- Required package: [jsonpath_ng](https://pypi.org/project/jsonpath-ng/) (`pip install jsonpath-ng`)

## Usage

### Command-Line Arguments

```bash
python script.py -j <input.json> -c <updates.csv> -m <mapping.json> -s <static_config.json> [-o <output.json>]
````

- **-j, --json-file**: Input JSON file (required).
- **-c, --csv-file**: CSV file with updates (required).
- **-m, --mapping-file**: JSON file mapping CSV columns to JSONPaths (required).
- **-s, --static-file**: Static config JSON file with operations (required).
- **-o, --output-file**: Output JSON file (optional, defaults to input file).

## File Formats

### Input JSON (`input.json`)

A single JSON object or a list of objects. Example:

```json
{
  "id": "5961b4af88c94ab285d07a36323f5548",
  "description": "Visual Graphics",
  "connectorAttributes": {
    "formPath": null
  },
  "features": ["NO_RANDOM_ACCESS", "DIRECT_PERMISSIONS"]
}
```

### CSV File (`updates.csv`)

Contains update data with an **"ID"** column for matching. Example:

```
ID,DESCRIPTION,OWNER_TYPE
5961b4af88c94ab285d07a36323f5548,Omini,IDENTITY
```

### Mapping File (`mapping.json`)

Maps CSV columns to JSONPaths. Example:

```json
{
  "DESCRIPTION": "$.description",
  "OWNER_TYPE": "$.owner.type"
}
```

### Static Config File (`static_config.json`)

A list of operations. Example:

```json
[
  {
    "path": "$.description",
    "operation": "update",
    "value": "Updated Description"
  },
  { "path": "$.connectorAttributes.formPath", "operation": "remove" },
  { "path": "$.features[0]", "operation": "remove" }
]
```

## Example Command

```bash
python script.py -j input.json -c updates.csv -m mapping.json -s static_config.json -o output.json
```

### Output

The script:

1. Updates `$.description` from CSV to "Omini".
2. Updates `$.description` from static config to "Updated Description".
3. Removes `$.connectorAttributes.formPath`.
4. Removes the first element of `$.features`.
5. Saves the result to `output.json`.

## How It Works

1. **Load Data**:
   - Reads the input JSON, CSV, mapping, and static config files.
2. **CSV Updates**:
   - Matches JSON objects by "ID" with CSV rows.
   - Updates fields using the mapping, validating types against existing values or inferring for new paths.
3. **Static Config Updates**:
   - Processes each entry in the static config:
     - **update**: Adds/updates the path with the given value, checking types.
     - **remove**: Deletes the key or array element at the specified path.
4. **Save Output**:
   - Writes the updated JSON to the output file with pretty-printing.

## Limitations

- **Simple Matching**:
  Only matches by "ID" in CSV and "id" in JSON. Multi-field matching isn’t supported without code changes.
- **Type Inference**:
  New fields from CSV default to strings if no existing value exists, which may not always be desired.
- **Static Config Overwrites**:
  `update` operations overwrite values; merging (e.g., appending to lists) isn’t supported.
- **Removal Constraints**:
  `remove` works only for direct keys or list indices; complex JSONPath filters (e.g., `$.features[?(@ == "value")]`) aren’t supported.
- **No Rollback**:
  Partial failures leave the JSON in an inconsistent state without automatic rollback.
- **Performance**:
  May be slow for very large JSON or CSV files due to JSONPath parsing overhead.
- **Error Handling**:
  Non-critical errors (e.g., type mismatches) are logged and skipped, potentially missing updates silently.
- **CSV Header Validation**:
  Doesn’t enforce that all mapped columns exist in the CSV header.

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install dependencies**:
   ```bash
   pip install jsonpath-ng
   ```

## Contributing

Feel free to submit issues or pull requests for bug fixes, feature enhancements (e.g., merge support, multi-field matching), or performance improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
