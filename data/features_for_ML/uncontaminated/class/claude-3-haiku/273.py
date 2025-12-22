from typing import Type
from feature import Feature
from abstract_feature_group import AbstractFeatureGroup

class NodeProperties:

    def __init__(self, feature: Feature, feature_group_class: Type[AbstractFeatureGroup]) -> None:
        self.feature = feature
        self.feature_group_class = feature_group_class

    def return_self(self) -> NodeProperties:
        return self