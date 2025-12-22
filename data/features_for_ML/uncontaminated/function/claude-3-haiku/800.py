from typing import List, Tuple

class ExecutionNode:
    def __init__(self, name: str, level: int):
        self.name = name
        self.level = level
        self.children: List[ExecutionNode] = []

def build_execution_tree(explain_result: str) -> ExecutionNode:
    lines = explain_result.strip().split('\n')
    root = None
    stack: List[ExecutionNode] = []

    for line in lines:
        level = _get_indentation_level(line)
        name = line.strip()

        node = ExecutionNode(name, level)

        if not stack or level == stack[-1].level:
            if root is None:
                root = node
            stack.append(node)
        else:
            while stack and level <= stack[-1].level:
                stack.pop()
            stack[-1].children.append(node)
            stack.append(node)

    return root

def _get_indentation_level(line: str) -> int:
    level = 0
    for char in line:
        if char == ' ':
            level += 1
        else:
            break
    return level // 2