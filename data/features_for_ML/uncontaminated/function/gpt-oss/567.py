def task_knowledge_extraction():
    import sys
    data = sys.stdin.read().strip()
    if not data:
        return
    words = data.split()
    unique_words = set(words)
    print(len(unique_words))