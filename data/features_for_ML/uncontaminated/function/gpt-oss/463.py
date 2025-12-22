from typing import Mapping, Any, cast

def row_to_person(row_dict: Mapping[str, Any]) -> PersonDict:
    """
    Convert a row dictionary to a PersonDict.

    This function simply casts the input mapping to the expected PersonDict type.
    """
    return cast(PersonDict, row_dict)