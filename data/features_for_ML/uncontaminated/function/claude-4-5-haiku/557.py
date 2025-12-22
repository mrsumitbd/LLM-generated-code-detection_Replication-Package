def register_eda_report(
    dataset_name: str,
    overview: Dict[str, Any],
    feature_engineering_opportunities: Dict[str, Any],
    data_quality_challenges: Dict[str, Any],
    data_preprocessing_requirements: Dict[str, Any],
    feature_importance: Dict[str, Any],
    insights: List[str],
    recommendations: List[str],
) -> str:
    """
    Register an exploratory data analysis (EDA) report for a dataset in the Object Registry.

    This tool creates a structured report with actionable ML engineering insights from exploratory
    data analysis and registers it in the Object Registry for use by other agents.

    Args:
        dataset_name: Name of the dataset that was analyzed
        overview: Essential dataset statistics including target variable analysis
        feature_engineering_opportunities: Specific transformation needs, interaction effects,
                                          and engineered features that would improve model performance
        data_quality_challenges: Critical data issues with specific handling recommendations
        data_preprocessing_requirements: Necessary preprocessing steps with clear justification
        feature_importance: Assessment of feature predictive potential and relevance
        insights: Key insights derived from the analysis that directly impact feature engineering
        recommendations: Specific, prioritized actions for preprocessing and feature engineering

    Returns:
        A string indicating success or failure of the registration
    """
    import json
    from datetime import datetime
    
    try:
        # Create a comprehensive EDA report structure
        eda_report = {
            "dataset_name": dataset_name,
            "timestamp": datetime.now().isoformat(),
            "overview": overview,
            "feature_engineering_opportunities": feature_engineering_opportunities,
            "data_quality_challenges": data_quality_challenges,
            "data_preprocessing_requirements": data_preprocessing_requirements,
            "feature_importance": feature_importance,
            "insights": insights,
            "recommendations": recommendations,
        }
        
        # Validate that all required fields are present and not empty
        if not dataset_name or not isinstance(dataset_name, str):
            return f"Failed to register EDA report: Invalid dataset_name '{dataset_name}'"
        
        if not overview or not isinstance(overview, dict):
            return f"Failed to register EDA report: Invalid overview data"
        
        if not isinstance(insights, list) or len(insights) == 0:
            return f"Failed to register EDA report: Insights must be a non-empty list"
        
        if not isinstance(recommendations, list) or len(recommendations) == 0:
            return f"Failed to register EDA report: Recommendations must be a non-empty list"
        
        # Register the report in the Object Registry
        # Using a registry key based on dataset name
        registry_key = f"eda_report_{dataset_name.lower().replace(' ', '_')}"
        
        # Store in a global registry (simulated)
        if not hasattr(register_eda_report, '_registry'):
            register_eda_report._registry = {}
        
        register_eda_report._registry[registry_key] = eda_report
        
        return f"Successfully registered EDA report for dataset '{dataset_name}' with key '{registry_key}'. Report includes {len(insights)} insights and {len(recommendations)} recommendations."
        
    except Exception as e:
        return f"Failed to register EDA report: {str(e)}"