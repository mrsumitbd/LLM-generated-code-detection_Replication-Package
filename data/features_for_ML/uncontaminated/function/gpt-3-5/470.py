def insert_after_line(change, lines, filepath):
    for i in range(len(lines)):
        if change['insert_after_line'] in lines[i]:
            lines.insert(i+1, change['content'])
            break