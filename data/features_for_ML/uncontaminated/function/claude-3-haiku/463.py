from typing import Mapping, Any
from dataclasses import dataclass

@dataclass
class PersonDict:
    name: str
    age: int
    email: str

def row_to_person(row_dict: Mapping[str, Any]) -> PersonDict:
    return PersonDict(
        name=row_dict['name'],
        age=row_dict['age'],
        email=row_dict['email']
    )