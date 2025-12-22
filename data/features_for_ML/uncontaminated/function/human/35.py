from .translation.translator import Translator
from .translation.variables import GraphVariables
import ibis

def _log_debug_end(translator: Translator, variables: GraphVariables) -> None:
    variables = translator._variables
    output_vars = {
        name: type(variables.peek_variable(name)) for name in translator.outputs
    }
    log.debug(
        f"\tOutput: {output_vars} TOTAL: {variables.nested_len()}/{len(variables)}"
    )

    if LOG_DATA:
        print("\tOutput Data", flush=True)
        print(
            _projection_results(translator.mutated_table, variables).execute(),
            flush=True,
        )
        print("", flush=True)
    if LOG_SQL:
        print("\tSQL Expressions", flush=True)
        print(
            ibis.duckdb.connect().compile(
                (_projection_results(translator.mutated_table, variables))
            ),
            flush=True,
        )