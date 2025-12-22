import asyncio
import serial
import serial.tools.list_ports
from typing import Optional
from dataclasses import dataclass

@dataclass
class Point3D:
    x: float
    y: float
    z: float

class GrblCNCAsync:

    def __init__(self, port: str, address: str = "1", limits: tuple[int, int, int, int, int, int] = (-150, 150, -200, 0, 0, 60)):
        self.port = port
        self.address = address
        self.limits = limits
        self.serial = None
        self._status = "Idle"
        self._position = Point3D(0, 0, 0)
        self._buffer = b""
        self._lock = asyncio.Lock()
        
    def _read_all(self):
        """Read all available data from serial port"""
        if self.serial and self.serial.in_waiting:
            return self.serial.read(self.serial.in_waiting)
        return b""
    
    def _parse(self, data: bytes, dtype: Optional[type] = None):
        """Parse data from GRBL response"""
        try:
            data_str = data.decode('utf-8').strip()
            
            if data_str.startswith('<') and data_str.endswith('>'):
                # Status report: <Idle|MPos:0.000,0.000,0.000|FS:0,0>
                parts = data_str[1:-1].split('|')
                self._status = parts[0]
                
                for part in parts[1:]:
                    if part.startswith('MPos:'):
                        coords = part[5:].split(',')
                        if len(coords) >= 3:
                            self._position = Point3D(
                                float(coords[0]),
                                float(coords[1]),
                                float(coords[2])
                            )
                return data_str
            
            elif data_str.startswith('[') and data_str.endswith(']'):
                # Info response
                return data_str
            
            elif data_str == 'ok' or data_str == 'error':
                return data_str
            
            if dtype:
                return dtype(data_str)
            
            return data_str
        except Exception as e:
            return None
    
    def _receive(self, data: bytes):
        """Process received data"""
        self._buffer += data
        
        while b'\n' in self._buffer:
            line, self._buffer = self._buffer.split(b'\n', 1)
            self._parse(line)
    
    @property
    def status(self) -> str:
        """Get current machine status"""
        return self._status
    
    @property
    def position(self) -> Point3D:
        """Get current machine position"""
        return self._position
    
    def get_position(self):
        """Get current position (alias for position property)"""
        return self.position
    
    @staticmethod
    def list():
        """List available serial ports"""
        ports = []
        for port_info in serial.tools.list_ports.comports():
            ports.append({
                'port': port_info.device,
                'description': port_info.description,
                'hwid': port_info.hwid
            })
        return ports