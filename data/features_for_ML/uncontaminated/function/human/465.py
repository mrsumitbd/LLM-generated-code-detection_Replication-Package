def extract_required(schema, prefix=""):
        required = []
        for key, rules in schema.items():
            if isinstance(rules, dict):
                path = f"{prefix}.{key}" if prefix else key
                if rules.get('required'):
                    meta = rules.get('meta', 'No description')
                    required.append(f"- `{path}`: {meta}")
                if rules.get('type') == 'dict' and 'schema' in rules:
                    required.extend(extract_required(rules['schema'], path))
        return required