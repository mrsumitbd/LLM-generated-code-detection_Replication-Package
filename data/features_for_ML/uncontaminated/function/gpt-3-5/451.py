def process_statement(statement, column_names=[]):
    result = []
    for line in statement.split('\n'):
        values = line.split(',')
        if len(column_names) > 0:
            row = {column_names[i]: values[i] for i in range(min(len(column_names), len(values)))}
        else:
            row = {f'column_{i+1}': value for i, value in enumerate(values)}
        result.append(row)
    return result