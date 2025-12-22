from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set

def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of query
        if self.query:
            _dict['query'] = self.query.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in queries (list)
        _items = []
        if self.queries:
            for _item_queries in self.queries:
                if _item_queries:
                    _items.append(_item_queries.to_dict())
            _dict['queries'] = _items
        return _dict