from typing import List
from intermediate_property_adaptor import IntermediatePropertyAdaptor
from forecasting_base_model import ForecastingBaseModel
from linear_model import LinearModel
from random_forest_model import RandomForestModel

DEFAULT_MODEL_TYPE = "randomforest"

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
        self.model_type = model_type

    def train(self, raw_stats: List[List[IntermediatePropertyAdaptor]]) -> ForecastingBaseModel:
        if self.model_type == "linear":
            model = LinearModel()
        elif self.model_type == "randomforest":
            model = RandomForestModel()
        else:
            raise ValueError(f"Invalid model type: {self.model_type}")

        model.fit(raw_stats)
        return model