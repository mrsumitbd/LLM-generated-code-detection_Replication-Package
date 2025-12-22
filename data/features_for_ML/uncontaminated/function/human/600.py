from tree_sitter import Node as TSNode

def _get_name_node(ts_node: TSNode) -> TSNode | None:
        if ts_node.type == "enum_declaration":
            return ts_node.child_by_field_name("name")
        return None