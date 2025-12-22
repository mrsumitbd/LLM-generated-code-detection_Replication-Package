import json
import time
from dataclasses import dataclass, asdict
from typing import List, Optional

# Minimal placeholder types for the purpose of this implementation
class HiDockJensen:
    """Placeholder for the actual HiDockJensen device interface."""
    def send_command(self, command_id: int, payload: bytes = b"") -> bytes:
        """Send a command to the device and return the raw response."""
        # In a real implementation this would communicate over serial or USB.
        # Here we simulate a successful response for even command IDs and
        # raise an exception for odd ones to mimic unsupported commands.
        if command_id % 2 == 0:
            return b"OK" + payload
        raise RuntimeError(f"Command {command_id} not supported")

@dataclass
class CommandResult:
    command_id: int
    success: bool
    response: Optional[bytes] = None
    error: Optional[str] = None

@dataclass
class DiscoverySession:
    results: List[CommandResult]
    timestamp: float

class JensenCommandDiscovery:
    """
    Jensen Protocol Command Discovery Tool
    
    This class systematically tests Jensen protocol commands to determine
    what the HiDock H1E device actually supports beyond the documented commands.
    """

    def __init__(self, jensen_device: HiDockJensen):
        self.device = jensen_device
        self.safe_mode = False
        self.known_commands = set()  # Populate with documented command IDs if known

    def set_safe_mode(self, enabled: bool):
        """Enable or disable safe mode for the discovery process."""
        self.safe_mode = enabled

    def test_single_command(self, command_id: int, test_payload: bytes = b"") -> CommandResult:
        """Send a single command and capture the result."""
        try:
            response = self.device.send_command(command_id, test_payload)
            return CommandResult(command_id=command_id, success=True, response=response)
        except Exception as e:
            return CommandResult(command_id=command_id, success=False, error=str(e))

    def discover_commands_in_range(self, start_cmd: int, end_cmd: int) -> List[CommandResult]:
        """Test all commands in the specified inclusive range."""
        results = []
        for cmd_id in range(start_cmd, end_cmd + 1):
            result = self.test_single_command(cmd_id)
            results.append(result)
        return results

    def test_missing_commands(self) -> List[CommandResult]:
        """Identify commands that are not documented but supported."""
        all_results = self.discover_commands_in_range(0, 255)
        missing = [r for r in all_results if r.success and r.command_id not in self.known_commands]
        return missing

    def validate_known_commands(self) -> List[CommandResult]:
        """Validate that all documented commands are supported."""
        return [self.test_single_command(cmd_id) for cmd_id in self.known_commands]

    def comprehensive_discovery(self, max_command_id: int = 50) -> DiscoverySession:
        """Run a full discovery session up to the specified maximum command ID."""
        results = self.discover_commands_in_range(0, max_command_id)
        session = DiscoverySession(results=results, timestamp=time.time())
        return session

    def save_discovery_results(self, session: DiscoverySession, filename: str = None):
        """Persist the discovery session to a JSON file."""
        if filename is None:
            filename = f"jensen_discovery_{int(session.timestamp)}.json"
        data = {
            "timestamp": session.timestamp,
            "results": [asdict(r) for r in session.results]
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def print_discovery_summary(self, session: DiscoverySession):
        """Print a concise summary of the discovery session."""
        total = len(session.results)
        successes = sum(1 for r in session.results if r.success)
        failures = total - successes
        print(f"Discovery Summary (Timestamp: {time.ctime(session.timestamp)})")
        print(f"  Total commands tested: {total}")
        print(f"  Successful responses: {successes}")
        print(f"  Failures: {failures}")
        if failures:
            print("  Failed command IDs:")
            for r in session.results:
                if not r.success:
                    print(f"    - {r.command_id}: {r.error}")