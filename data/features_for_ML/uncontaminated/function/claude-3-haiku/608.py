import subprocess
import threading
import time
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
    try:
        process = subprocess.Popen(['ngrok', 'http', str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        def monitor_tunnel():
            while True:
                output = process.stdout.readline().decode().strip()
                if output.startswith('Forwarding'):
                    tunnel_url = output.split('Forwarding')[1].strip().split(' ')[0]
                    if url_callback:
                        url_callback(tunnel_url)
                elif output.startswith('Error'):
                    if error_callback:
                        error_callback(output)
                time.sleep(1)
        
        threading.Thread(target=monitor_tunnel, daemon=True).start()
        return True
    except (subprocess.CalledProcessError, OSError) as e:
        if error_callback:
            error_callback(str(e))
        return False