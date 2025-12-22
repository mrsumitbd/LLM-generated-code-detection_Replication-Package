def _cleanup_orphan_bridges():
    """Clean up orphan bridges that are not associated with any active network."""
    import subprocess
    import json
    
    try:
        # Get list of all bridges
        result = subprocess.run(
            ['brctl', 'show'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return
        
        lines = result.stdout.strip().split('\n')[1:]  # Skip header
        bridges = set()
        
        for line in lines:
            if line.strip():
                parts = line.split()
                if parts:
                    bridges.add(parts[0])
        
        # Get active network interfaces
        result = subprocess.run(
            ['ip', 'link', 'show'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return
        
        active_interfaces = set()
        for line in result.stdout.split('\n'):
            if ':' in line and not line.startswith(' '):
                parts = line.split(':')
                if len(parts) >= 2:
                    iface = parts[1].strip()
                    active_interfaces.add(iface)
        
        # Find orphan bridges (bridges with no interfaces)
        for bridge in bridges:
            result = subprocess.run(
                ['brctl', 'show', bridge],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                # If bridge has no interfaces (only header line)
                if len(lines) <= 1:
                    try:
                        subprocess.run(
                            ['ip', 'link', 'set', bridge, 'down'],
                            timeout=10,
                            capture_output=True
                        )
                        subprocess.run(
                            ['brctl', 'delbr', bridge],
                            timeout=10,
                            capture_output=True
                        )
                    except Exception:
                        pass
    
    except Exception:
        pass