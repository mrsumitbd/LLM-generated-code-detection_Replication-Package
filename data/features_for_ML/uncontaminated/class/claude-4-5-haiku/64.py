class DbPostgresql:
    def __init__(self):
        self.process = None
        self.data_dir = None

    def clean_files(self):
        import shutil
        import os
        if self.data_dir and os.path.exists(self.data_dir):
            shutil.rmtree(self.data_dir)

    def start(self):
        import subprocess
        import tempfile
        import os
        import time
        
        self.data_dir = tempfile.mkdtemp()
        
        try:
            subprocess.run(['initdb', '-D', self.data_dir], 
                         check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.clean_files()
            raise
        
        try:
            self.process = subprocess.Popen(
                ['postgres', '-D', self.data_dir, '-F'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(1)
        except FileNotFoundError:
            self.clean_files()
            raise

    def stop(self):
        import subprocess
        import time
        
        if self.process:
            try:
                subprocess.run(['pg_ctl', 'stop', '-D', self.data_dir],
                             timeout=5, capture_output=True)
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
            
            self.process = None
        
        self.clean_files()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()