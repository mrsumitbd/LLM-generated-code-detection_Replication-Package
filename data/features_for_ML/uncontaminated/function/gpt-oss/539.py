import sys

def redo():
    data = sys.stdin.read().splitlines()
    if not data:
        return
    n = int(data[0])
    text = []
    undo_stack = []
    redo_stack = []
    for line in data[1:n+1]:
        if line.startswith("type"):
            _, ch = line.split()
            text.append(ch)
            undo_stack.append(("type", ch))
            redo_stack.clear()
        elif line == "undo":
            if undo_stack:
                op, ch = undo_stack.pop()
                if op == "type":
                    text.pop()
                redo_stack.append((op, ch))
        elif line == "redo":
            if redo_stack:
                op, ch = redo_stack.pop()
                if op == "type":
                    text.append(ch)
                undo_stack.append((op, ch))
    sys.stdout.write("".join(text))

if __name__ == "__main__":
    redo()