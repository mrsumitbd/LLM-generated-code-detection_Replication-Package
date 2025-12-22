from typing import Dict, List, Any
from datetime import datetime
from plexe.core.object_registry import ObjectRegistry

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
    object_registry = ObjectRegistry()

    try:
        # Create structured EDA report with actionable ML focus
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

        # TODO: separate EDA reports for raw and transformed data
        # Register in registry
        object_registry.register(dict, f"eda_report_{dataset_name}", eda_report, overwrite=True)
        logger.debug(f"✅ Registered EDA report for dataset '{dataset_name}'")
        return f"Successfully registered EDA report for dataset '{dataset_name}'"

    except Exception as e:
        logger.warning(f"⚠️ Error registering EDA report: {str(e)}")
        raise RuntimeError(f"Failed to register EDA report for dataset '{dataset_name}': {str(e)}")