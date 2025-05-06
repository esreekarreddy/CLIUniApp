"""Common theme settings for consistent UI across all windows"""

import tkinter as tk
from tkinter import ttk

# Color scheme
COLORS = {
    "primary": "#3a7ca5",       # Header blue
    "primary_dark": "#2c6284",  # Darker blue for buttons/highlights
    "background": "#f5f5f5",    # Light gray background
    "text": "#333333",          # Dark gray text
    "text_light": "#ffffff",    # White text
    "success": "#d4edda",       # Light green (HD)
    "info": "#d1ecf1",          # Light blue (D)
    "warning": "#fff3cd",       # Light yellow (C)
    "neutral": "#e2e3e5",       # Light gray (P)
    "danger": "#f8d7da",        # Light red (Z)
    "button": "#4a8db7",        # Button color
    "button_hover": "#3a7ca5",  # Button hover
}

# Font configurations
FONTS = {
    "header": ("Helvetica", 14, "bold"),
    "subheader": ("Helvetica", 12, "bold"),
    "body": ("Helvetica", 11),
    "small": ("Helvetica", 10),
}

def setup_theme():
    """Apply the application theme to the current ttk styles"""
    style = ttk.Style()
    
    # Try to use a modern theme as base
    try:
        style.theme_use('clam')
    except tk.TclError:
        # Some systems might not have clam
        pass
    
    # Configure ttk elements with our colors
    style.configure("TButton", 
                   background=COLORS["button"],
                   foreground=COLORS["text_light"],
                   padding=(10, 5),
                   font=FONTS["body"])
    
    style.map("TButton",
             background=[('active', COLORS["button_hover"])])
    
    style.configure("TLabel", 
                   background=COLORS["background"],
                   foreground=COLORS["text"],
                   font=FONTS["body"])
    
    style.configure("TEntry", 
                   fieldbackground="white",
                   font=FONTS["body"])
    
    style.configure("TFrame", 
                   background=COLORS["background"])
    
    # Treeview styling
    style.configure("Treeview", 
                   font=FONTS["body"],
                   rowheight=25,
                   background="white", 
                   fieldbackground="white")
    
    style.configure("Treeview.Heading", 
                   font=FONTS["subheader"],
                   background=COLORS["primary"],
                   foreground=COLORS["text_light"])
    
    # For headers
    style.configure("Header.TFrame", 
                   background=COLORS["primary"])
    
    style.configure("Header.TLabel", 
                   background=COLORS["primary"],
                   foreground=COLORS["text_light"],
                   font=FONTS["header"])

def apply_theme_to_window(window):
    """Apply basic theme elements to a window"""
    window.configure(background=COLORS["background"])
    setup_theme()

def create_header(parent, title_text):
    """Create a standardized header with the given title"""
    header_frame = tk.Frame(parent, bg=COLORS["primary"], pady=10)
    header_frame.pack(fill=tk.X)
    
    tk.Label(header_frame, 
             text=title_text,
             font=FONTS["header"], 
             fg=COLORS["text_light"], 
             bg=COLORS["primary"]).pack(pady=5)
    
    return header_frame
