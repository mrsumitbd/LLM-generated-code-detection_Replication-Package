def path_to_regex(path: str) -> str:
                parts = path.strip("/").split("/")
                regex_parts = []

                for part in parts:
                    if part == "**":
                        # Match any number of tokens
                        regex_parts.append(r".*")
                    elif part == "*":
                        # Match a single token
                        regex_parts.append(r"[^/]+")
                    else:
                        # Regular token
                        regex_parts.append(part)

                # We do NOT start with a slash as only the node name could be specified
                return "^" + "/".join(regex_parts) + "$"