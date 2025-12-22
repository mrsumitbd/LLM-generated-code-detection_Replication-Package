from nat.profiler.forecasting.models import ForecastingBaseModel
from nat.profiler.forecasting.config import DEFAULT_MODEL_TYPE
from nat.profiler.intermediate_property_adapter import IntermediatePropertyAdaptor

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
        self._model = create_model(self.model_type)

    def train(self, raw_stats: list[list[IntermediatePropertyAdaptor]]) -> ForecastingBaseModel:
        """
        Train the model using the `raw_stats` training data.

        Parameters
        ----------
        raw_stats: list[list[IntermediatePropertyAdaptor]]
            Stats collected by the profiler.

        Returns
        -------
        ForecastingBaseModel
            A fitted model.
        """

        self._model.fit(raw_stats)

        return self._model