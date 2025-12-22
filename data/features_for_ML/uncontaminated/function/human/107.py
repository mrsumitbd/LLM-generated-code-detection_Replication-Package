import os
from tkinter import ttk, filedialog, messagebox, simpledialog, Scrollbar

def find_and_replace_pattern_with_aow_and_update_counters():
    global loaded_file_data
    try:
        # Get file path
        file_path = file_path_var.get()
        section_number = current_section_var.get()
        if not file_path or section_number == 0:
            messagebox.showerror("Error", "No file selected or section not chosen. Please load a file and select a section.")
            return

        # Get section information
        section_info = SECTIONS[section_number]
        
        # Convert loaded_file_data to bytearray if it's not already
        if isinstance(loaded_file_data, bytes):
            loaded_file_data = bytearray(loaded_file_data)
        
        # Get current section data from loaded_file_data
        section_data = loaded_file_data[section_info['start']:section_info['end']+1]
        file_name = os.path.basename(file_path_var.get()).lower()
    
        # Determine offset based on file name
        if file_name == "memory.dat":
            base_offset = 0xA019DE
            if 1 <= section_number <= 10:
                offset = base_offset + (section_number - 1) * 0x290
            else:
                messagebox.showerror("Error", f"Invalid section number: {section_number}")
                return
        elif file_name == "memory.sl2":
            # Section 1 starts at 0xA01AA2, each section offset is 632 (0x278) bytes apart
            base_offset = 0xA01AA2
            if 1 <= section_number <= 10:
                offset = base_offset + (section_number - 1) * 0x290
            else:
                messagebox.showerror("Error", f"Invalid section number: {section_number}")
                return
        else:
            messagebox.showerror("Error", f"Unknown file type: {file_name}")
            return
        print(file_name)
        # Now call locate_name with the correct offset
        name_bytes = locate_name(file_path_var.get(), offset)

        # Locate Fixed Pattern 1
        fixed_pattern_offset = find_hex_offset(section_data, name_bytes.hex())
        print(fixed_pattern_offset)
        
        if fixed_pattern_offset is None:
            fixed_pattern_offset=0xffff
            messagebox.showerror("Error", "Due to character name not being found, unrelated items could be shown.")
            
        fixed_pattern_offset_start = fixed_pattern_offset
        search_start_position = fixed_pattern_offset_start + len(hex_pattern1_Fixed) + 1000
        
        if search_start_position >= len(section_data):
            print("Search start position beyond section data.")
            return
            
        fixed_pattern_offset_end = find_hex_offset(section_data[search_start_position:], hex_pattern_end)
        if fixed_pattern_offset_end is not None:
            fixed_pattern_offset_end += search_start_position
        else:
            # Handle case where end pattern isn't found
            print("End pattern not found")
            return

        # Call the slot finder with corrected parameters
        empty_slot_finder_aow(file_path, section_info['start'] + 32, section_info['start'] + fixed_pattern_offset - 100)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to add or update item: {e}")