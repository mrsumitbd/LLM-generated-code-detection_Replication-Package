from __future__ import annotations

from typing import List, Any
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# Default model type
DEFAULT_MODEL_TYPE = "randomforest"

# Try to import the expected types; fall back to simple placeholders if unavailable
try:
    from forecasting.base import ForecastingBaseModel
except Exception:  # pragma: no cover
    class ForecastingBaseModel:
        """Fallback base model class."""
        pass

try:
    from data.adaptor import IntermediatePropertyAdaptor
except Exception:  # pragma: no cover
    class IntermediatePropertyAdaptor:
        """Fallback adaptor with minimal interface."""
        def __init__(self, features: List[float], target: float):
            self.features = features
            self.target = target

        def to_dict(self) -> dict:
            return {"features": self.features, "target": self.target}


class ModelTrainer:
    """
    Orchestrates data preprocessing, training, and returning
    a fitted model.

    Parameters
    ----------
    model_type: str, default = "randomforest"
        The type of model to train. Options include "linear" and "randomforest".
    """

    def __init__(self, model_type: str = DEFAULT_MODEL_TYPE):
        if model_type not in {"linear", "randomforest"}:
            raise ValueError(
                f"Unsupported model_type '{model_type}'. "
                "Supported types are 'linear' and 'randomforest'."
            )
        self.model_type = model_type

    def _extract_features_and_target(
        self, raw_stats: List[List[IntermediatePropertyAdaptor]]
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Convert raw adaptor lists into feature matrix X and target vector y.
        """
        X_list: List[List[float]] = []
        y_list: List[float] = []

        for adaptor_list in raw_stats:
            for adaptor in adaptor_list:
                # Prefer to_dict if available
                if hasattr(adaptor, "to_dict"):
                    data = adaptor.to_dict()
                    features = data.get("features", [])
                    target = data.get("target")
                else:
                    # Fallback to attributes
                    features = getattr(adaptor, "features", [])
                    target = getattr(adaptor, "target", None)

                if target is None:
                    raise ValueError(
                        f"Adaptor {adaptor!r} does not provide a target value."
                    )
                X_list.append(features)
                y_list.append(target)

        X = np.array(X_list, dtype=float)
        y = np.array(y_list, dtype=float)
        return X, y

    def train(
        self, raw_stats: List[List[IntermediatePropertyAdaptor]]
    ) -> ForecastingBaseModel:
        """
        Train the selected model on the provided raw statistics.

        Parameters
        ----------
        raw_stats : list[list[IntermediatePropertyAdaptor]]
            Nested list of adaptors containing feature and target data.

        Returns
        -------
        ForecastingBaseModel
            The fitted model instance.
        """
        X, y = self._extract_features_and_target(raw_stats)

        if self.model_type == "linear":
            model: ForecastingBaseModel = LinearRegression()
        else:  # randomforest
            model = RandomForestRegressor(random_state=42)

        model.fit(X, y)
        return model