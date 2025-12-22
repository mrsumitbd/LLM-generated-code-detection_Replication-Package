from typing import List
from forecasting_base_model import ForecastingBaseModel
from intermediate_property_adaptor import IntermediatePropertyAdaptor

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
        # Perform data preprocessing
        preprocessed_data = self._preprocess_data(raw_stats)
        
        # Train the model based on the preprocessed data
        fitted_model = self._train_model(preprocessed_data)
        
        return fitted_model

    def _preprocess_data(self, raw_stats: List[List[IntermediatePropertyAdaptor]]) -> List[List[float]]:
        # Placeholder for data preprocessing logic
        preprocessed_data = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]  # Dummy preprocessed data
        return preprocessed_data

    def _train_model(self, preprocessed_data: List[List[float]]) -> ForecastingBaseModel:
        if self.model_type == "linear":
            model = self._train_linear_model(preprocessed_data)
        elif self.model_type == "randomforest":
            model = self._train_randomforest_model(preprocessed_data)
        else:
            raise ValueError("Invalid model type. Supported types are 'linear' and 'randomforest'.")
        
        return model

    def _train_linear_model(self, preprocessed_data: List[List[float]]) -> ForecastingBaseModel:
        # Placeholder for training linear model logic
        return ForecastingBaseModel("Linear Model")

    def _train_randomforest_model(self, preprocessed_data: List[List[float]]) -> ForecastingBaseModel:
        # Placeholder for training random forest model logic
        return ForecastingBaseModel("Random Forest Model")