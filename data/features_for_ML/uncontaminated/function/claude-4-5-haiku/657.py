def display_splash_screen(args: argparse.Namespace) -> None:
    """
    Display a colorful splash screen showing MiniRAG server configuration

    Args:
        args: Parsed command line arguments
    """
    import sys
    
    # ANSI color codes
    BOLD = '\033[1m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    
    # Clear screen
    print('\033[2J\033[H', end='')
    
    # Splash screen
    splash = f"""
{BOLD}{CYAN}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    {MAGENTA}✨ MiniRAG Server ✨{CYAN}                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{RESET}
{BOLD}{GREEN}Configuration:{RESET}
  {YELLOW}Host:{RESET}              {WHITE}{args.host}{RESET}
  {YELLOW}Port:{RESET}              {WHITE}{args.port}{RESET}
  {YELLOW}Workers:{RESET}           {WHITE}{getattr(args, 'workers', 1)}{RESET}
  {YELLOW}Log Level:{RESET}         {WHITE}{getattr(args, 'log_level', 'INFO')}{RESET}
  {YELLOW}Reload:{RESET}            {WHITE}{getattr(args, 'reload', False)}{RESET}

{BOLD}{CYAN}Starting MiniRAG server...{RESET}
"""
    
    print(splash)
    sys.stdout.flush()