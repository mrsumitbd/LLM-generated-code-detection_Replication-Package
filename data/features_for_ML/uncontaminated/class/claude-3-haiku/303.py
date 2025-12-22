class UserSearchRefinement:
    """Schema for refining user search parameters."""

    def __init__(self, search_term=None, location=None, category=None, price_range=None, rating=None, sort_by=None):
        self.search_term = search_term
        self.location = location
        self.category = category
        self.price_range = price_range
        self.rating = rating
        self.sort_by = sort_by

    def to_dict(self):
        return {
            "search_term": self.search_term,
            "location": self.location,
            "category": self.category,
            "price_range": self.price_range,
            "rating": self.rating,
            "sort_by": self.sort_by
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            search_term=data.get("search_term"),
            location=data.get("location"),
            category=data.get("category"),
            price_range=data.get("price_range"),
            rating=data.get("rating"),
            sort_by=data.get("sort_by")
        )