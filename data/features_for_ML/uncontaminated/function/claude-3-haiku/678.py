import os
import tempfile

def rules_dir_writable() -> bool:
    """
    Checks if Prometheus rules directory is writable
    """
    try:
        with tempfile.TemporaryDirectory(dir='/etc/prometheus/rules') as temp_dir:
            with open(os.path.join(temp_dir, 'test.txt'), 'w') as f:
                f.write('test')
        return True
    except (OSError, IOError):
        return False