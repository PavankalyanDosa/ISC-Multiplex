#!/usr/bin/env python3

import json
import csv
import argparse
import logging
import sys
from jsonpath_ng import parse
from typing import Any

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# I/O Helper Functions
def load_json(json_file_path: str) -> Any:
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load JSON from '{json_file_path}': {e}")
        raise

def save_json(data: Any, json_file_path: str) -> None:
    try:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        logging.info(f"Successfully saved updated JSON to '{json_file_path}'")
    except Exception as e:
        logging.error(f"Failed to save JSON to '{json_file_path}': {e}")
        raise

def load_csv(csv_file_path: str) -> list:
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)
    except Exception as e:
        logging.error(f"Failed to load CSV from '{csv_file_path}': {e}")
        raise

# Enhanced JSONPath Handling
def get_value_by_path(obj: Any, path: str) -> Any:
    """Get value from JSON object using JSONPath, return None if not found"""
    try:
        expr = parse(path)
        matches = expr.find(obj)
        return matches[0].value if matches else None
    except Exception:
        return None

def set_value_by_path(obj: Any, path: str, value: Any) -> None:
    """Set value in JSON object using JSONPath, creating structure if needed"""
    expr = parse(path)
    expr.update_or_create(obj, value)

def remove_value_by_path(obj: Any, path: str) -> None:
    """Remove a key from JSON object using JSONPath"""
    try:
        expr = parse(path)
        matches = expr.find(obj)
        if matches:
            match = matches[0]
            # Get the parent context and the final key/index
            parent = match.context.value if match.context else obj
            final_key = match.path.fields[-1] if hasattr(match.path, 'fields') else match.path.index
            if isinstance(parent, dict) and isinstance(final_key, str):
                del parent[final_key]
                logging.debug(f"Removed key at {path}")
            elif isinstance(parent, list) and isinstance(final_key, int):
                del parent[final_key]
                logging.debug(f"Removed index at {path}")
            else:
                logging.warning(f"Cannot remove {path}: invalid parent type or key")
        else:
            logging.debug(f"Path {path} not found for removal")
    except Exception as e:
        logging.warning(f"Failed to remove {path}: {e}")

def get_type_from_value(value: Any) -> type:
    """Get Python type from a value"""
    if value is None:
        return type(None)
    return type(value)

def cast_value(value: str, target_type: type) -> Any:
    """Cast string value to target type"""
    try:
        if target_type == str:
            return value
        elif target_type == int:
            return int(value)
        elif target_type == float:
            return float(value)
        elif target_type == bool:
            return value.lower() in ('true', '1', 'yes')
        elif target_type == list:
            return json.loads(value) if value else []
        elif target_type == dict:
            return json.loads(value) if value else {}
        return value
    except Exception as e:
        logging.warning(f"Failed to cast '{value}' to {target_type.__name__}: {e}")
        return value

# CSV Updates with Type Validation
def update_from_csv(json_obj: dict, csv_row: dict, mapping: dict) -> None:
    """Update JSON object from CSV with type validation"""
    for csv_key, json_path in mapping.items():
        if csv_key not in csv_row or csv_key == "ID":
            continue
            
        new_value = csv_row[csv_key]
        current_value = get_value_by_path(json_obj, json_path)
        
        if current_value is not None:
            target_type = get_type_from_value(current_value)
            try:
                casted_value = cast_value(new_value, target_type)
                if isinstance(current_value, (list, dict)) and not isinstance(casted_value, type(current_value)):
                    logging.warning(f"Type mismatch at {json_path}: expected {type(current_value)}, got {type(casted_value)}")
                    continue
                set_value_by_path(json_obj, json_path, casted_value)
                logging.debug(f"Updated {json_path} with {casted_value} (type: {target_type.__name__})")
            except Exception as e:
                logging.warning(f"Failed to update {json_path}: {e}")
        else:
            inferred_value = cast_value(new_value, str)
            set_value_by_path(json_obj, json_path, inferred_value)
            logging.debug(f"Created {json_path} with {inferred_value}")

# Static Config Updates with Operations
def update_from_static_config(json_obj: dict, static_config: list) -> None:
    """Update JSON object from static config with update/remove operations"""
    for entry in static_config:
        path = entry.get("path")
        operation = entry.get("operation")
        value = entry.get("value") if "value" in entry else None
        
        if not path or not operation:
            logging.warning(f"Skipping invalid static config entry: {entry}")
            continue

        if operation not in ["update", "remove"]:
            logging.warning(f"Invalid operation '{operation}' in static config for {path}")
            continue

        if operation == "update":
            if "value" not in entry:
                logging.warning(f"Missing 'value' for update operation at {path}")
                continue
                
            current_value = get_value_by_path(json_obj, path)
            if current_value is not None:
                current_type = get_type_from_value(current_value)
                new_type = get_type_from_value(value)
                if current_type != new_type:
                    logging.warning(f"Type mismatch at {path}: expected {current_type.__name__}, got {new_type.__name__}")
                    continue
                set_value_by_path(json_obj, path, value)
                logging.debug(f"Updated existing {path} with {value}")
            else:
                set_value_by_path(json_obj, path, value)
                logging.debug(f"Created {path} with {value}")
                
        elif operation == "remove":
            remove_value_by_path(json_obj, path)

# Main Execution
def main():
    parser = argparse.ArgumentParser(description="JSON updater with CSV and enhanced static config")
    parser.add_argument("-j", "--json-file", required=True, help="Input JSON file")
    parser.add_argument("-c", "--csv-file", required=True, help="CSV file with updates")
    parser.add_argument("-m", "--mapping-file", required=True, help="JSON mapping file")
    parser.add_argument("-s", "--static-file", required=True, help="Static config JSON file")
    parser.add_argument("-o", "--output-file", help="Output JSON file (defaults to input)")
    parser.add_argument("-l","--log-level", default="INFO", help="Logging level (DEBUG, INFO, etc.).")

    args = parser.parse_args()
    logging.getLogger().setLevel(args.log_level.upper())

    output_file = args.output_file if args.output_file else args.json_file

    # Load data
    json_data = load_json(args.json_file)
    csv_data = load_csv(args.csv_file)
    mapping = load_json(args.mapping_file)
    static_config = load_json(args.static_file)

    # Process single object or list
    if isinstance(json_data, dict):
        # 1. Update from CSV first
        for row in csv_data:
            if row.get("ID") == json_data.get("id"):
                update_from_csv(json_data, row, mapping)
                break
        else:
            logging.warning("No matching CSV row found for JSON object")

        # 2. Update from static config
        update_from_static_config(json_data, static_config)

    elif isinstance(json_data, list):
        # 1. Update from CSV first
        for row in csv_data:
            for obj in json_data:
                if row.get("ID") == obj.get("id"):
                    update_from_csv(obj, row, mapping)

        # 2. Update from static config
        for obj in json_data:
            update_from_static_config(obj, static_config)
    else:
        logging.error("JSON must be a dict or list of dicts")
        sys.exit(1)

    # Save result
    save_json(json_data, output_file)

if __name__ == "__main__":
    main()