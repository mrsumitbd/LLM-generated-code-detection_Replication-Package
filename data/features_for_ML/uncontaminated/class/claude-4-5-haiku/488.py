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
        self._validate_model_type()

    def _validate_model_type(self) -> None:
        """Validate that the model_type is supported."""
        valid_types = ["linear", "randomforest"]
        if self.model_type not in valid_types:
            raise ValueError(
                f"Invalid model_type '{self.model_type}'. "
                f"Must be one of {valid_types}"
            )

    def train(self, raw_stats: list[list[IntermediatePropertyAdaptor]]) -> ForecastingBaseModel:
        """
        Train a model on the provided raw statistics.

        Parameters
        ----------
        raw_stats : list[list[IntermediatePropertyAdaptor]]
            Raw statistics data to train on.

        Returns
        -------
        ForecastingBaseModel
            A fitted forecasting model.
        """
        # Preprocess the data
        X, y = self._preprocess_data(raw_stats)

        # Create and train the model
        if self.model_type == "linear":
            model = self._create_linear_model()
        elif self.model_type == "randomforest":
            model = self._create_randomforest_model()

        # Fit the model
        model.fit(X, y)

        return model

    def _preprocess_data(self, raw_stats: list[list[IntermediatePropertyAdaptor]]) -> tuple:
        """
        Preprocess raw statistics into features and target.

        Parameters
        ----------
        raw_stats : list[list[IntermediatePropertyAdaptor]]
            Raw statistics data.

        Returns
        -------
        tuple
            (X, y) where X is features and y is target values.
        """
        X = []
        y = []

        for sequence in raw_stats:
            for adaptor in sequence:
                features = adaptor.get_features()
                target = adaptor.get_target()
                X.append(features)
                y.append(target)

        import numpy as np
        return np.array(X), np.array(y)

    def _create_linear_model(self) -> ForecastingBaseModel:
        """Create a linear regression model."""
        from sklearn.linear_model import LinearRegression
        return LinearRegression()

    def _create_randomforest_model(self) -> ForecastingBaseModel:
        """Create a random forest model."""
        from sklearn.ensemble import RandomForestRegressor
        return RandomForestRegressor(random_state=42)