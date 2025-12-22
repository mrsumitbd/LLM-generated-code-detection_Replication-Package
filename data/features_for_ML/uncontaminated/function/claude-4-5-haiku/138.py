import os
import sys
from anthropic import Anthropic

class Boot:
    def __init__(self, name: str):
        self.name = name
    
    def __repr__(self):
        return f"Boot({self.name})"

def _detect_boot() -> Boot:
    """Detect the boot environment using Claude AI through multi-turn conversation."""
    client = Anthropic()
    conversation_history = []
    
    # System prompt for boot detection
    system_prompt = """You are an expert system administrator who can detect the boot environment of a system.
    
    Based on the information provided about the system, you should identify what boot system is being used.
    Common boot systems include:
    - BIOS (Basic Input/Output System)
    - UEFI (Unified Extensible Firmware Interface)
    - EFI (Extensible Firmware Interface)
    - OpenFirmware
    - U-Boot
    - GRUB
    - LILO
    - systemd-boot
    - rEFInd
    
    When you have enough information to make a determination, respond with ONLY the boot system name in the format:
    BOOT_DETECTED: [boot_system_name]
    
    Otherwise, ask clarifying questions about the system."""
    
    # Gather initial system information
    initial_info = f"""Please help me detect the boot environment. Here's what I can tell you about the system:
    - OS: {sys.platform}
    - Python version: {sys.version}
    - System: {os.name}"""
    
    if sys.platform == "linux":
        # Try to detect UEFI vs BIOS on Linux
        if os.path.exists("/sys/firmware/efi"):
            initial_info += "\n- /sys/firmware/efi exists (indicates UEFI)"
        else:
            initial_info += "\n- /sys/firmware/efi does not exist (indicates BIOS)"
        
        # Check for common bootloaders
        if os.path.exists("/boot/grub"):
            initial_info += "\n- GRUB bootloader found"
        if os.path.exists("/boot/efi"):
            initial_info += "\n- EFI boot partition found"
    
    elif sys.platform == "darwin":
        initial_info += "\n- This is macOS, which uses EFI/UEFI boot"
    
    elif sys.platform == "win32":
        initial_info += "\n- This is Windows"
        # Windows typically uses UEFI on modern systems
        if os.path.exists("C:\\Windows\\Boot\\EFI"):
            initial_info += "\n- EFI boot files found"
    
    # Start the conversation
    conversation_history.append({
        "role": "user",
        "content": initial_info
    })
    
    # First turn - get initial assessment
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        system=system_prompt,
        messages=conversation_history
    )
    
    assistant_message = response.content[0].text
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })
    
    # Check if boot was detected
    if "BOOT_DETECTED:" in assistant_message:
        boot_name = assistant_message.split("BOOT_DETECTED:")[1].strip().split("\n")[0].strip()
        return Boot(boot_name)
    
    # If not detected, provide more information based on what Claude asks
    if sys.platform == "linux":
        additional_info = """Here's more information:
        - I can check /proc/cmdline for boot parameters
        - I can check /etc/fstab for mount information
        - I can check for systemd-boot in /boot/loader
        - I can check for LILO in /etc/lilo.conf"""
    elif sys.platform == "darwin":
        additional_info = "macOS uses EFI firmware for booting."
    elif sys.platform == "win32":
        additional_info = "Windows uses UEFI on modern systems, BIOS on older systems."
    else:
        additional_info = "Unable to determine additional boot information for this platform."
    
    conversation_history.append({
        "role": "user",
        "content": additional_info
    })
    
    # Second turn - get refined assessment
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        system=system_prompt,
        messages=conversation_history
    )
    
    assistant_message = response.content[0].text
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })
    
    # Check if boot was detected
    if "BOOT_DETECTED:" in assistant_message:
        boot_name = assistant_message.split("BOOT_DETECTED:")[1].strip().split("\n")[0].strip()
        return Boot(boot_name)
    
    # Final turn - ask Claude to make a determination
    conversation_history.append({
        "role": "user",
        "content": "Based on all the information provided, what is the most likely boot system? Please respond with BOOT_DETECTED: [system_name]"
    })
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        system=system_prompt,
        messages=conversation_history
    )
    
    assistant_message = response.content[0].text
    
    # Extract boot name
    if "BOOT_DETECTED:" in assistant_message:
        boot_name = assistant_message.split("BOOT_DETECTED:")[1].strip().split("\n")[0].strip()
    else:
        # Fallback based on platform
        if sys.platform == "linux":
            boot_name = "UEFI" if os.path.exists("/sys/firmware/efi") else "BIOS"
        elif sys.platform == "darwin":
            boot_name = "EFI"
        elif sys.platform == "win32":
            boot_name = "UEFI"
        else:
            boot_name = "Unknown"
    
    return Boot(boot_name)


if __name__ == "__main__":
    boot = _detect_boot()
    print(f"Detected boot system: {boot}")