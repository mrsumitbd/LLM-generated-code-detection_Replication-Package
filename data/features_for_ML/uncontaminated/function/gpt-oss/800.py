from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ExecutionNode:
    """Simple node for representing a Spark execution plan."""
    name: str
    children: List["ExecutionNode"] = field(default_factory=list)

    def add_child(self, child: "ExecutionNode") -> None:
        self.children.append(child)

    def __repr__(self) -> str:
        return f"ExecutionNode(name={self.name!r}, children={len(self.children)})"


def build_execution_tree(explain_result: str) -> Optional[ExecutionNode]:
    """
    Build a tree structure from result of df.explain("formatted").
    Parent - child relationship is established based on indentation level.
    Returns the root node of the tree.
    """
    if not explain_result:
        return None

    lines = explain_result.splitlines()
    root: Optional[ExecutionNode] = None
    stack: List[ExecutionNode] = []

    for raw_line in lines:
        # Skip empty lines
        if not raw_line.strip():
            continue

        # Determine indentation level (2 spaces per level in Spark explain)
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        level = indent // 2

        # Node name is the line stripped of leading/trailing whitespace
        name = raw_line.strip()

        node = ExecutionNode(name=name)

        if level == 0:
            # This is the root node
            root = node
            stack = [node]
        else:
            # Ensure the stack has the parent at level-1
            if level - 1 < len(stack):
                parent = stack[level - 1]
                parent.add_child(node)
            else:
                # Malformed indentation; treat as child of last node
                if stack:
                    stack[-1].add_child(node)

            # Update stack to current level
            if level < len(stack):
                stack[level] = node
                stack = stack[: level + 1]
            else:
                stack.append(node)

    return root