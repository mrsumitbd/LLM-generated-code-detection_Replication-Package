class JensenCommandDiscovery:
    """
    Jensen Protocol Command Discovery Tool
    
    This class systematically tests Jensen protocol commands to determine
    what the HiDock H1E device actually supports beyond the documented commands.
    """

    def __init__(self, jensen_device: HiDockJensen):
        self.device = jensen_device
        self.safe_mode = True
        self.tested_commands = {}
        self.discovered_commands = []

    def set_safe_mode(self, enabled: bool):
        self.safe_mode = enabled

    def test_single_command(self, command_id: int, test_payload: bytes = b"") -> CommandResult:
        try:
            if self.safe_mode and command_id > 100:
                return CommandResult(
                    command_id=command_id,
                    supported=False,
                    response=None,
                    error="Command ID exceeds safe mode limit",
                    payload_used=test_payload
                )
            
            response = self.device.send_command(command_id, test_payload)
            
            result = CommandResult(
                command_id=command_id,
                supported=True,
                response=response,
                error=None,
                payload_used=test_payload
            )
            
            self.tested_commands[command_id] = result
            return result
            
        except Exception as e:
            result = CommandResult(
                command_id=command_id,
                supported=False,
                response=None,
                error=str(e),
                payload_used=test_payload
            )
            self.tested_commands[command_id] = result
            return result

    def discover_commands_in_range(self, start_cmd: int, end_cmd: int) -> List[CommandResult]:
        results = []
        for cmd_id in range(start_cmd, end_cmd + 1):
            result = self.test_single_command(cmd_id)
            results.append(result)
        return results

    def test_missing_commands(self) -> List[CommandResult]:
        known_commands = [0x01, 0x02, 0x03, 0x04, 0x05, 0x10, 0x11, 0x20, 0x21]
        results = []
        
        for cmd_id in known_commands:
            if cmd_id not in self.tested_commands:
                result = self.test_single_command(cmd_id)
                results.append(result)
        
        return results

    def validate_known_commands(self) -> List[CommandResult]:
        known_commands = {
            0x01: b"\x00",
            0x02: b"\x00",
            0x03: b"\x00",
            0x04: b"\x00",
            0x05: b"\x00",
        }
        
        results = []
        for cmd_id, payload in known_commands.items():
            result = self.test_single_command(cmd_id, payload)
            results.append(result)
        
        return results

    def comprehensive_discovery(self, max_command_id: int = 50) -> DiscoverySession:
        session = DiscoverySession(
            start_time=datetime.now(),
            safe_mode=self.safe_mode,
            max_command_id=max_command_id
        )
        
        # Test known commands
        known_results = self.validate_known_commands()
        session.results.extend(known_results)
        
        # Test missing commands
        missing_results = self.test_missing_commands()
        session.results.extend(missing_results)
        
        # Discover commands in range
        discovery_results = self.discover_commands_in_range(0, max_command_id)
        session.results.extend(discovery_results)
        
        # Remove duplicates
        seen = set()
        unique_results = []
        for result in session.results:
            if result.command_id not in seen:
                seen.add(result.command_id)
                unique_results.append(result)
        
        session.results = unique_results
        session.end_time = datetime.now()
        session.total_commands_tested = len(unique_results)
        session.supported_commands = [r for r in unique_results if r.supported]
        
        return session

    def save_discovery_results(self, session: DiscoverySession, filename: str = None):
        if filename is None:
            filename = f"jensen_discovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = {
            "start_time": session.start_time.isoformat(),
            "end_time": session.end_time.isoformat() if session.end_time else None,
            "safe_mode": session.safe_mode,
            "max_command_id": session.max_command_id,
            "total_commands_tested": session.total_commands_tested,
            "supported_commands_count": len(session.supported_commands),
            "results": [
                {
                    "command_id": r.command_id,
                    "supported": r.supported,
                    "response": r.response.hex() if r.response else None,
                    "error": r.error,
                    "payload_used": r.payload_used.hex() if r.payload_used else None
                }
                for r in session.results
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def print_discovery_summary(self, session: DiscoverySession):
        print("\n" + "="*60)
        print("JENSEN COMMAND DISCOVERY SUMMARY")
        print("="*60)
        print(f"Start Time: {session.start_time}")
        print(f"End Time: {session.end_time}")
        print(f"Safe Mode: {session.safe_mode}")
        print(f"Max Command ID Tested: {session.max_command_id}")
        print(f"Total Commands Tested: {session.total_commands_tested}")
        print(f"Supported Commands: {len(session.supported_commands)}")
        print(f"Unsupported Commands: {session.total_commands_tested - len(session.supported_commands)}")
        print("\nSupported Commands:")
        for result in sorted(session.supported_commands, key=lambda x: x.command_id):
            print(f"  0x{result.command_id:02X}: {result.response.hex() if result.response else 'No response'}")
        print("="*60 + "\n")