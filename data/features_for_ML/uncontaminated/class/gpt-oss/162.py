import json
import os
from pathlib import Path
from typing import Dict, List, Any


class JsonUtil:
    @staticmethod
    def write_data(data: Dict[str, Any], data_path: str | Path) -> None:
        """Write a dictionary to a JSON file."""
        path = Path(data_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def read_data(data_path: str | Path) -> Dict[str, Any]:
        """Read a JSON file and return its contents as a dictionary."""
        path = Path(data_path)
        if not path.is_file():
            raise FileNotFoundError(f"JSON file not found: {path}")
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def read_all_data(data_path_dir: str | Path) -> List[Dict[str, Any]]:
        """Read all JSON files in a directory and return a list of dictionaries."""
        dir_path = Path(data_path_dir)
        if not dir_path.is_dir():
            raise NotADirectoryError(f"Directory not found: {dir_path}")
        data_list: List[Dict[str, Any]] = []
        for json_file in dir_path.glob("*.json"):
            try:
                data_list.append(JsonUtil.read_data(json_file))
            except Exception:
                # Skip files that cannot be parsed as JSON
                continue
        return data_list

    @staticmethod
    def create_tmp_json(data_dict: Dict[str, Any], json_path: str | Path) -> None:
        """Create a temporary JSON file from a dictionary."""
        JsonUtil.write_data(data_dict, json_path)

    @staticmethod
    def rewrite_template_json(
        jsonpath: str | Path,
        extend_args: Dict[str, List[Any]] | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Rewrite a JSON template file.

        Parameters
        ----------
        jsonpath : str | Path
            Path to the JSON file to be rewritten.
        extend_args : dict[str, list], optional
            For each key, the list of values to extend the existing list.
            If the key does not exist, it will be created with the list.
        **kwargs : Any
            Additional key/value pairs to set or override in the JSON.
        """
        path = Path(jsonpath)
        if not path.is_file():
            raise FileNotFoundError(f"Template JSON not found: {path}")

        # Load existing data
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        # Extend lists if requested
        if extend_args:
            for key, values in extend_args.items():
                if key in data and isinstance(data[key], list):
                    data[key].extend(values)
                else:
                    data[key] = list(values)

        # Update with kwargs
        for key, value in kwargs.items():
            data[key] = value

        # Write back
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)