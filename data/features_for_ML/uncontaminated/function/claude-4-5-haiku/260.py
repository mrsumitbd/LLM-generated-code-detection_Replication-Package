def analyze_program(  # noqa C901
        self,
        df_or_prog: Union["DomainFile", "Program"],
        require_symbols: bool = True,
        force_analysis: bool = False,
        verbose_analysis: bool = False,
    ):
    """Analyze a program or domain file and extract relevant information."""
    from .program import Program
    from .domain_file import DomainFile
    
    # Convert DomainFile to Program if necessary
    if isinstance(df_or_prog, DomainFile):
        program = df_or_prog.program
    else:
        program = df_or_prog
    
    # Check if analysis is already done and not forced
    if hasattr(program, '_analyzed') and program._analyzed and not force_analysis:
        return program
    
    # Initialize analysis structures
    if not hasattr(program, 'symbols'):
        program.symbols = {}
    if not hasattr(program, 'dependencies'):
        program.dependencies = {}
    if not hasattr(program, 'metadata'):
        program.metadata = {}
    
    # Extract symbols from the program
    if hasattr(program, 'ast') and program.ast:
        self._extract_symbols(program, verbose_analysis)
    
    # Analyze dependencies
    if hasattr(program, 'symbols'):
        self._analyze_dependencies(program, verbose_analysis)
    
    # Validate symbols if required
    if require_symbols and not program.symbols:
        if verbose_analysis:
            print("Warning: No symbols found in program")
    
    # Mark as analyzed
    program._analyzed = True
    
    if verbose_analysis:
        print(f"Analysis complete. Found {len(program.symbols)} symbols")
    
    return program

def _extract_symbols(self, program, verbose: bool = False):
    """Extract symbols from program AST."""
    if not hasattr(program, 'ast'):
        return
    
    ast = program.ast
    
    # Walk through AST nodes
    for node in self._walk_ast(ast):
        symbol_info = self._extract_symbol_info(node)
        if symbol_info:
            name = symbol_info.get('name')
            if name:
                program.symbols[name] = symbol_info
                if verbose:
                    print(f"Found symbol: {name}")

def _walk_ast(self, node):
    """Walk through AST nodes recursively."""
    yield node
    if hasattr(node, 'children'):
        for child in node.children:
            yield from self._walk_ast(child)
    elif hasattr(node, '__dict__'):
        for attr_value in node.__dict__.values():
            if isinstance(attr_value, list):
                for item in attr_value:
                    if hasattr(item, '__dict__'):
                        yield from self._walk_ast(item)
            elif hasattr(attr_value, '__dict__'):
                yield from self._walk_ast(attr_value)

def _extract_symbol_info(self, node):
    """Extract symbol information from an AST node."""
    symbol_info = {}
    
    if hasattr(node, 'name'):
        symbol_info['name'] = node.name
    
    if hasattr(node, 'type'):
        symbol_info['type'] = node.type
    
    if hasattr(node, 'lineno'):
        symbol_info['lineno'] = node.lineno
    
    if hasattr(node, 'value'):
        symbol_info['value'] = node.value
    
    return symbol_info if symbol_info.get('name') else None

def _analyze_dependencies(self, program, verbose: bool = False):
    """Analyze dependencies between symbols."""
    if not hasattr(program, 'symbols'):
        return
    
    for symbol_name, symbol_info in program.symbols.items():
        program.dependencies[symbol_name] = []
        
        # Check for references to other symbols
        for other_name in program.symbols:
            if other_name != symbol_name:
                if self._has_dependency(symbol_info, other_name):
                    program.dependencies[symbol_name].append(other_name)
                    if verbose:
                        print(f"{symbol_name} depends on {other_name}")

def _has_dependency(self, symbol_info, other_name):
    """Check if a symbol has a dependency on another symbol."""
    for key, value in symbol_info.items():
        if isinstance(value, str) and other_name in value:
            return True
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str) and other_name in item:
                    return True
    return False