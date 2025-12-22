from typing import Optional, Callable

def start_tunnel_for_api(port: int = 5000, url_callback: Optional[Callable[[str], None]] = None, 
                        error_callback: Optional[Callable[[str], None]] = None) -> bool:
    """
    Convenience function to start tunnel for API server
    
    Args:
        port: API server port
        url_callback: Callback function for when tunnel URL is available
        error_callback: Callback function for tunnel errors
        
    Returns:
        bool: True if tunnel startup was initiated successfully
    """
    manager = get_tunnel_manager()
    manager.set_callbacks(url_callback, error_callback)
    return manager.start_tunnel(port)