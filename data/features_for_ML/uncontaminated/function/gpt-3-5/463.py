def row_to_person(row_dict: Mapping[str, Any]) -> PersonDict:
    person = {
        'name': row_dict.get('name', ''),
        'age': row_dict.get('age', 0),
        'gender': row_dict.get('gender', ''),
        'city': row_dict.get('city', ''),
    }
    return person