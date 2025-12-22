import anthropic


class UserSearchRefinement:
    """Schema for refining user search parameters."""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"

    def refine_search(self, original_query: str, search_results: list[dict]) -> dict:
        """
        Refine user search parameters based on initial query and results.
        
        Args:
            original_query: The original search query from the user
            search_results: List of search results with metadata
            
        Returns:
            Dictionary containing refined search parameters
        """
        
        # Create a prompt to analyze and refine the search
        results_summary = "\n".join([
            f"- {result.get('title', 'No title')}: {result.get('description', 'No description')}"
            for result in search_results[:5]
        ])
        
        prompt = f"""Analyze the following user search query and initial results, then suggest refinements to improve the search:

Original Query: {original_query}

Initial Results:
{results_summary}

Please provide refined search parameters in the following JSON format:
{{
    "refined_query": "improved search query",
    "suggested_filters": ["filter1", "filter2"],
    "search_intent": "description of what the user likely wants",
    "alternative_queries": ["alternative1", "alternative2"]
}}"""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Parse the response
        response_text = message.content[0].text
        
        # Extract JSON from the response
        import json
        import re
        
        # Find JSON in the response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            try:
                refinement_data = json.loads(json_match.group())
                return refinement_data
            except json.JSONDecodeError:
                pass
        
        # Fallback if JSON parsing fails
        return {
            "refined_query": original_query,
            "suggested_filters": [],
            "search_intent": "User search query",
            "alternative_queries": []
        }

    def get_search_suggestions(self, partial_query: str) -> list[str]:
        """
        Get search suggestions based on a partial query.
        
        Args:
            partial_query: Partial search query from the user
            
        Returns:
            List of suggested complete queries
        """
        
        prompt = f"""Based on the partial search query "{partial_query}", suggest 5 complete search queries that the user might be looking for. Return only the suggestions as a JSON array of strings."""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=512,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text
        
        # Extract JSON array from response
        import json
        import re
        
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if json_match:
            try:
                suggestions = json.loads(json_match.group())
                return suggestions if isinstance(suggestions, list) else []
            except json.JSONDecodeError:
                pass
        
        return [partial_query]

    def categorize_search(self, query: str) -> dict:
        """
        Categorize a search query into relevant categories.
        
        Args:
            query: The search query to categorize
            
        Returns:
            Dictionary with category information
        """
        
        prompt = f"""Categorize the following search query into relevant categories and provide metadata:

Query: {query}

Return a JSON object with:
{{
    "primary_category": "main category",
    "secondary_categories": ["category1", "category2"],
    "keywords": ["keyword1", "keyword2"],
    "search_type": "informational|navigational|transactional|local"
}}"""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=512,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text
        
        # Extract JSON from response
        import json
        import re
        
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            try:
                category_data = json.loads(json_match.group())
                return category_data
            except json.JSONDecodeError:
                pass
        
        # Fallback
        return {
            "primary_category": "general",
            "secondary_categories": [],
            "keywords": query.split(),
            "search_type": "informational"
        }


if __name__ == "__main__":
    # Example usage
    refinement = UserSearchRefinement()
    
    # Test refine_search
    original_query = "best restaurants"
    sample_results = [
        {"title": "Top 10 Restaurants in NYC", "description": "A guide to the best dining spots"},
        {"title": "Restaurant Reviews", "description": "User reviews and ratings"},
        {"title": "Fine Dining Guide", "description": "Luxury restaurant recommendations"}
    ]
    
    refined = refinement.refine_search(original_query, sample_results)
    print("Refined Search:", refined)
    
    # Test get_search_suggestions
    suggestions = refinement.get_search_suggestions("best rest")
    print("Suggestions:", suggestions)
    
    # Test categorize_search
    categories = refinement.categorize_search("how to make pasta")
    print("Categories:", categories)