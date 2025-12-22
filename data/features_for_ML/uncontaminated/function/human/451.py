import sqlparse

def process_statement(statement, column_names=[]):
    if isinstance(statement, sqlparse.sql.IdentifierList):
        for identifier in statement.get_identifiers():
            process_identifier(identifier)
    elif isinstance(statement, sqlparse.sql.Identifier):
        process_identifier(statement, column_names)
    elif isinstance(statement, sqlparse.sql.TokenList):
        for item in statement.tokens:
            process_statement(item)