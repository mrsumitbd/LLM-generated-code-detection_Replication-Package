import json
from typing import Dict, Any, List
from object_registry import register_object

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
    eda_report = {
        "dataset_name": dataset_name,
        "overview": overview,
        "feature_engineering_opportunities": feature_engineering_opportunities,
        "data_quality_challenges": data_quality_challenges,
        "data_preprocessing_requirements": data_preprocessing_requirements,
        "feature_importance": feature_importance,
        "insights": insights,
        "recommendations": recommendations
    }

    try:
        register_object(f"eda_report_{dataset_name}", json.dumps(eda_report))
        return "EDA report registered successfully"
    except Exception as e:
        return f"Failed to register EDA report: {str(e)}"