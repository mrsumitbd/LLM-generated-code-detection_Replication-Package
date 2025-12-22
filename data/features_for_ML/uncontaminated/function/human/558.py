from typing import Any, ClassVar, Dict, Optional
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
        # override the default output from pydantic by calling `to_dict()` of profile
        if self.profile:
            _dict['profile'] = self.profile.to_dict()
        # override the default output from pydantic by calling `to_dict()` of email
        if self.email:
            _dict['email'] = self.email.to_dict()
        # override the default output from pydantic by calling `to_dict()` of phone
        if self.phone:
            _dict['phone'] = self.phone.to_dict()
        # override the default output from pydantic by calling `to_dict()` of password
        if self.password:
            _dict['password'] = self.password.to_dict()
        # set to None if username (nullable) is None
        # and model_fields_set contains the field
        if self.username is None and "username" in self.model_fields_set:
            _dict['username'] = None

        return _dict