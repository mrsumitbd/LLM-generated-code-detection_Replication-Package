import json
import os
from typing import Any, Dict, List

# Path to the simulated Object Registry (JSON file)
_REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "object_registry.json")


def _load_registry() -> Dict[str, Any]:
    """Load the registry from disk, creating an empty one if necessary."""
    if not os.path.exists(_REGISTRY_PATH):
        return {}
    try:
        with open(_REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # If the file is corrupted or unreadable, start fresh
        return {}


def _save_registry(registry: Dict[str, Any]) -> None:
    """Persist the registry to disk."""
    with open(_REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)


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
    try:
        # Build the report payload
        report = {
            "dataset_name": dataset_name,
            "overview": overview,
            "feature_engineering_opportunities": feature_engineering_opportunities,
            "data_quality_challenges": data_quality_challenges,
            "data_preprocessing_requirements": data_preprocessing_requirements,
            "feature_importance": feature_importance,
            "insights": insights,
            "recommendations": recommendations,
        }

        # Load existing registry
        registry = _load_registry()

        # Use dataset_name as the key; overwrite if already present
        registry[dataset_name] = report

        # Persist back to disk
        _save_registry(registry)

        return f"EDA report for '{dataset_name}' registered successfully."
    except Exception as exc:
        return f"Failed to register EDA report for '{dataset_name}': {exc}"