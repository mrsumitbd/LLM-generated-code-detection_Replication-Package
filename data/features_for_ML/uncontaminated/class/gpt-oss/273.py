from __future__ import annotations
from typing import Type

class NodeProperties:
    def __init__(self, feature: 'Feature', feature_group_class: Type['AbstractFeatureGroup']) -> None:
        self.feature = feature
        self.feature_group_class = feature_group_class

    def return_self(self) -> NodeProperties:
        return self