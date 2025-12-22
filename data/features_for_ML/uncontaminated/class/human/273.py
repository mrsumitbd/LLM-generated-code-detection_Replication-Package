from typing import Type
from mloda_core.abstract_plugins.components.feature import Feature
from mloda_core.abstract_plugins.abstract_feature_group import AbstractFeatureGroup

class NodeProperties:
    def __init__(self, feature: Feature, feature_group_class: Type[AbstractFeatureGroup]) -> None:
        self.feature = feature
        self.feature_group_class = feature_group_class
        self.name = feature.name

    def return_self(self) -> NodeProperties:
        return self