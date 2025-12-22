def helper(sub):
        for subtask, deps in dependencies.items():
            if sub in deps:
                result_set.add(subtask)
                helper(subtask)