"""
Entry-point so you can simply run  `python -m GUIUniApp`
"""
import os
import sys
import tkinter as tk

# Ensure parent directory is in path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Use relative import when running as a module
from login_win import LoginWindow

def main():
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    # When running this file directly, not as a module
    from login_win import LoginWindow
    main()
