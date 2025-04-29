import tkinter as tk
from tkinter import messagebox
from typing import Union  # Add this import

def error(message: str, title: str = "Error") -> None:
    """Display an error message box."""
    messagebox.showerror(title, message)


def info(message: str, title: str = "Information") -> None:
    """Display an information message box."""
    messagebox.showinfo(title, message)


def centre(win: Union[tk.Toplevel, tk.Tk], w=420, h=260) -> None:
    """Centre a window on screen with given width and height."""
    # Get the screen width and height
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # Calculate x and y positions for the Tk window
    x = (screen_width // 2) - (w // 2)
    y = (screen_height // 2) - (h // 2)

    # Set the dimensions and position
    win.geometry(f'{w}x{h}+{x}+{y}')