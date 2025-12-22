def redo():
    import sys
    import os

    try:
        last_command = sys.argv[1]
        os.system(last_command)
    except IndexError:
        print("No previous command to redo.")