import json
from typing import IO, Any, Mapping, NotRequired, Optional, TypedDict, cast

def row_to_person(row_dict: Mapping[str, Any]) -> PersonDict:
                records = [json.loads(record) for record in row_dict["records"]]

                return PersonDict(
                    uuid=row_dict["uuid"],
                    created=row_dict["created"],
                    version=row_dict["version"],
                    records=records,
                )