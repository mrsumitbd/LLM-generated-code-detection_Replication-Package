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
    try:
        from pyngrok import ngrok
        
        # Start ngrok tunnel
        public_url = ngrok.connect(port, "http")
        
        # Extract the URL string
        tunnel_url = public_url.public_url if hasattr(public_url, 'public_url') else str(public_url)
        
        # Call the URL callback if provided
        if url_callback:
            url_callback(tunnel_url)
        
        return True
    except Exception as e:
        # Call the error callback if provided
        if error_callback:
            error_callback(str(e))
        return False