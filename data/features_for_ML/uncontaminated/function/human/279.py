def _is_true(valid) -> bool:
            if isinstance(valid, str):
                return valid and valid.lower() in {"1", "true"}

            return True if valid else False