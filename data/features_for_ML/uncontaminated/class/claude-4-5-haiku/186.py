import os
import time
import threading
from anthropic import Anthropic

class CPUMonitor:
    """Non-blocking CPU monitoring with cgroup awareness."""

    def __init__(self, max_cpu_per_core: float):
        self.max_cpu_per_core = max_cpu_per_core
        self.last_cpu_time = None
        self.last_wall_time = None
        self.cpu_usage = 0.0
        self.lock = threading.Lock()
        self.update_thread = threading.Thread(target=self._update_cpu_usage, daemon=True)
        self.update_thread.start()

    def _get_cpu_time(self) -> float:
        """Get CPU time from /proc/self/stat or cgroup."""
        try:
            # Try cgroup v2 first
            if os.path.exists('/sys/fs/cgroup/cpu.stat'):
                with open('/sys/fs/cgroup/cpu.stat', 'r') as f:
                    for line in f:
                        if line.startswith('usage_usec'):
                            return float(line.split()[1]) / 1_000_000
            
            # Try cgroup v1
            if os.path.exists('/sys/fs/cgroup/cpuacct/cpuacct.usage'):
                with open('/sys/fs/cgroup/cpuacct/cpuacct.usage', 'r') as f:
                    return float(f.read().strip()) / 1_000_000_000
            
            # Fallback to /proc/self/stat
            with open('/proc/self/stat', 'r') as f:
                fields = f.read().split()
                utime = int(fields[13])
                stime = int(fields[14])
                return (utime + stime) / 100.0
        except (FileNotFoundError, ValueError, IndexError):
            return 0.0

    def _update_cpu_usage(self):
        """Background thread to update CPU usage."""
        while True:
            current_cpu_time = self._get_cpu_time()
            current_wall_time = time.time()
            
            with self.lock:
                if self.last_cpu_time is not None and self.last_wall_time is not None:
                    cpu_delta = current_cpu_time - self.last_cpu_time
                    wall_delta = current_wall_time - self.last_wall_time
                    
                    if wall_delta > 0:
                        # Get number of CPU cores
                        try:
                            num_cores = os.cpu_count() or 1
                        except:
                            num_cores = 1
                        
                        # Calculate CPU usage as percentage per core
                        self.cpu_usage = (cpu_delta / wall_delta) / num_cores * 100
                
                self.last_cpu_time = current_cpu_time
                self.last_wall_time = current_wall_time
            
            time.sleep(0.1)

    def get_cpu_nowait(self) -> float:
        """Get current CPU usage percentage per core without blocking."""
        with self.lock:
            return self.cpu_usage

    def should_throttle(self) -> bool:
        """Check if CPU usage exceeds the threshold."""
        return self.get_cpu_nowait() > self.max_cpu_per_core


def main():
    """Main function to demonstrate CPU monitoring with Claude API."""
    # Initialize CPU monitor with 80% threshold per core
    cpu_monitor = CPUMonitor(max_cpu_per_core=80.0)
    
    # Initialize Anthropic client
    client = Anthropic()
    conversation_history = []
    
    print("CPU Monitor with Claude API")
    print("=" * 50)
    print(f"CPU threshold: {cpu_monitor.max_cpu_per_core}% per core")
    print("Type 'quit' to exit, 'status' to check CPU, or ask Claude anything")
    print("=" * 50)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("Exiting...")
            break
        
        if user_input.lower() == 'status':
            cpu_usage = cpu_monitor.get_cpu_nowait()
            should_throttle = cpu_monitor.should_throttle()
            print(f"\nCPU Status:")
            print(f"  Current usage: {cpu_usage:.2f}% per core")
            print(f"  Should throttle: {should_throttle}")
            continue
        
        if not user_input:
            continue
        
        # Check CPU before making API call
        if cpu_monitor.should_throttle():
            print(f"\nSystem: CPU usage is high ({cpu_monitor.get_cpu_nowait():.2f}%). Throttling API calls.")
            continue
        
        # Add user message to conversation history
        conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Make API call with conversation history
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system="You are a helpful assistant. Keep responses concise and friendly.",
            messages=conversation_history
        )
        
        # Extract assistant response
        assistant_message = response.content[0].text
        
        # Add assistant response to conversation history
        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        print(f"\nClaude: {assistant_message}")
        
        # Print CPU status
        cpu_usage = cpu_monitor.get_cpu_nowait()
        print(f"[CPU: {cpu_usage:.2f}%]")


if __name__ == "__main__":
    main()