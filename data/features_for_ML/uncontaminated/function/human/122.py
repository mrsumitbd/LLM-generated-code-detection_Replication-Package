from typing import Any

def _recurse(node: Any):
        if isinstance(node, dict):
            # Dive into $defs/definitions first (Pydantic v2 uses $defs)
            for defs_key in ("$defs", "definitions"):
                if defs_key in node and isinstance(node[defs_key], dict):
                    for _, sub in node[defs_key].items():
                        _recurse(sub)

            # Recurse common composition keys
            for k in SCHEMA_KEYS_SINGLE:
                if k in node:
                    _recurse(node[k])
            for k in SCHEMA_KEYS_ARRAY:
                if k in node and isinstance(node[k], list):
                    for sub in node[k]:
                        _recurse(sub)

            # items can be schema or list of schemas (tuple validation)
            if "items" in node:
                items = node["items"]
                if isinstance(items, list):
                    for sub in items:
                        _recurse(sub)
                else:
                    _recurse(items)
            # prefixItems (2020-12)
            if "prefixItems" in node and isinstance(node["prefixItems"], list):
                for sub in node["prefixItems"]:
                    _recurse(sub)
            # properties / patternProperties values are schemas
            if "properties" in node and isinstance(node["properties"], dict):
                for sub in node["properties"].values():
                    _recurse(sub)
            if "patternProperties" in node and isinstance(
                node["patternProperties"], dict
            ):
                for sub in node["patternProperties"].values():
                    _recurse(sub)
            # additionalProperties itself can be a schema; recurse into it if dict
            if "additionalProperties" in node and isinstance(
                node["additionalProperties"], dict
            ):
                _recurse(node["additionalProperties"])

            # Now, possibly inject at this node if it's an object schema
            if _is_object_schema(node):
                has_ap = "additionalProperties" in node
                has_uneval = "unevaluatedProperties" in node
                if (not has_ap or not only_when_missing) and not (
                    skip_when_unevaluated_present and has_uneval
                ):
                    # Don’t overwrite explicitly set AP if only_when_missing=True
                    if not (has_ap and only_when_missing):
                        node["additionalProperties"] = value
        elif isinstance(node, list):
            for sub in node:
                _recurse(sub)