def row_to_person(row_dict: Mapping[str, Any]) -> PersonDict:
    return {
        "name": row_dict.get("name", ""),
        "age": row_dict.get("age", 0),
        "email": row_dict.get("email", ""),
        "phone": row_dict.get("phone", ""),
        "address": row_dict.get("address", "")
    }