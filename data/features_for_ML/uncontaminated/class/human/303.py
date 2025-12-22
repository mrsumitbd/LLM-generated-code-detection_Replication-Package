
class UserSearchRefinement:
    """Schema for refining user search parameters."""
    add_filters: str = ""
    remove_filters: str = ""
    change_limit: int = 0
    include_deactivated: bool = False