def check_and_notify():
    """Check for updates and notify user if available.

    This is the main entry point for version checking.
    """
    import subprocess
    import sys
    import json
    from packaging import version
    
    try:
        # Get current version
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", "anthropic"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return
        
        current_version = None
        for line in result.stdout.split('\n'):
            if line.startswith('Version:'):
                current_version = line.split(':', 1)[1].strip()
                break
        
        if not current_version:
            return
        
        # Get latest version from PyPI
        result = subprocess.run(
            [sys.executable, "-m", "pip", "index", "versions", "anthropic"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            # Fallback: try using pip search or direct PyPI API
            import urllib.request
            try:
                response = urllib.request.urlopen(
                    "https://pypi.org/pypi/anthropic/json",
                    timeout=5
                )
                data = json.loads(response.read().decode())
                latest_version = data['info']['version']
            except Exception:
                return
        else:
            # Parse version from pip index output
            latest_version = None
            for line in result.stdout.split('\n'):
                if 'Available versions:' in line:
                    versions = line.split(':', 1)[1].strip().split(',')
                    latest_version = versions[0].strip()
                    break
            
            if not latest_version:
                return
        
        # Compare versions
        if version.parse(latest_version) > version.parse(current_version):
            print(f"\n{'='*60}")
            print(f"A new version of anthropic is available!")
            print(f"Current version: {current_version}")
            print(f"Latest version: {latest_version}")
            print(f"To update, run: pip install --upgrade anthropic")
            print(f"{'='*60}\n")
    
    except Exception:
        # Silently fail if version check encounters any error
        pass