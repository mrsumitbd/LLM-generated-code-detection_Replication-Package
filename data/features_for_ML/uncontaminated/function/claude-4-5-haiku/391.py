def compare(args: argparse.Namespace) -> int:
    import os
    import json
    
    file1 = args.file1
    file2 = args.file2
    
    if not os.path.exists(file1):
        print(f"Error: File '{file1}' not found")
        return 1
    
    if not os.path.exists(file2):
        print(f"Error: File '{file2}' not found")
        return 1
    
    try:
        with open(file1, 'r') as f:
            content1 = f.read()
        
        with open(file2, 'r') as f:
            content2 = f.read()
        
        if content1 == content2:
            print(f"Files are identical")
            return 0
        else:
            print(f"Files are different")
            return 1
    
    except Exception as e:
        print(f"Error reading files: {e}")
        return 1