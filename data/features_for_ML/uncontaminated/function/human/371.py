from fenic.core._logical_plan.plans.base import LogicalPlan

def _transform_plan(node: LogicalPlan) -> None:
        # Transform expressions attached to this plan node
        for attr, val in list(vars(node).items()):
            new_val = _transform_value(val)
            if new_val is not val:
                setattr(node, attr, new_val)
        # Recurse into children
        for child in node.children():
            _transform_plan(child)