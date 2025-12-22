import os
from tkinter import ttk, filedialog, messagebox, simpledialog, Scrollbar

def load_section(section_number):
    if not loaded_file_data:
        messagebox.showerror("Error", "Please open a file first")
        return

    current_section_var.set(section_number)
    section_info = SECTIONS[section_number]
    section_data = loaded_file_data[section_info['start']:section_info['end'] + 1]

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
        # Section 1 starts at 0xA01AA2, each section offset is 632 (0x278) bytes apart (290 in the new update)
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
    if name_bytes is None:
        messagebox.showerror("Error", "Failed to locate character name. Please ensure the file is valid.")
        return

    # Do something with section_data and name_bytes...
    print(f"Loaded section {section_number} with name: {name_bytes}")
    

    
    

    offset1 = find_hex_offset(section_data, name_bytes.hex())
    if offset1 is None:
        name_bytes =locate_name1(file_path_var.get(), offset)
        offset1 = find_hex_offset(section_data, name_bytes.hex())
        if offset1 is None:
            name_bytes =locate_name2(file_path_var.get(), offset)
            offset1 = find_hex_offset(section_data, name_bytes.hex())
    
    find_steam_id(section_data)
        
    if offset1 is not None:
        # Display Souls value
        souls_offset = offset1 + 52
        sig_offset= offset1 - 64
        current_sig= find_value_at_offset(section_data, sig_offset)
        current_sig_var.set(current_sig if current_sig is not None else "N/A")
        current_souls = find_value_at_offset(section_data, souls_offset)
        current_souls_var.set(current_souls if current_souls is not None else "N/A")

        # Display character name
        for distance in possible_name_distances_for_name_tap:
            name_offset = offset1
            current_name = find_character_name(section_data, name_offset)
            if current_name and current_name != "N/A":
                current_name_var.set(current_name)
                break
        else:
            current_name_var.set("N/A")

    else:
        current_souls_var.set("N/A")
        current_name_var.set("N/A")
        current_sig_var.set("N/A")