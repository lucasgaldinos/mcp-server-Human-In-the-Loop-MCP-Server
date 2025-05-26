#!/usr/bin/env python3
"""
Human-in-the-Loop MCP Server

This server provides tools for getting human input and choices through GUI dialogs.
It enables LLMs to pause and ask for human feedback, input, or decisions.
"""

import asyncio
import json
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from typing import List, Dict, Any, Optional, Literal
import sys
import os
from pydantic import Field
from typing import Annotated

from fastmcp import FastMCP, Context

# Initialize the MCP server
mcp = FastMCP("Human-in-the-Loop Server")

# Global variable to ensure GUI is initialized properly
_gui_initialized = False
_gui_lock = threading.Lock()

def ensure_gui_initialized():
    """Ensure GUI subsystem is properly initialized"""
    global _gui_initialized
    with _gui_lock:
        if not _gui_initialized:
            # Force tkinter to initialize properly on Windows
            try:
                test_root = tk.Tk()
                test_root.withdraw()
                test_root.destroy()
                _gui_initialized = True
            except Exception as e:
                print(f"Warning: GUI initialization failed: {e}")
                _gui_initialized = False
        return _gui_initialized

def create_input_dialog(title: str, prompt: str, default_value: str = "", input_type: str = "text"):
    """Create an input dialog window - runs in main thread"""
    try:
        # Create root window
        root = tk.Tk()
        root.withdraw()  # Hide main window
        root.attributes('-topmost', True)  # Bring to front
        root.lift()
        root.focus_force()
        
        # Show the dialog
        if input_type == "text":
            result = simpledialog.askstring(title, prompt, parent=root, initialvalue=default_value)
        elif input_type == "integer":
            try:
                initial = int(default_value) if default_value else 0
            except:
                initial = 0
            result = simpledialog.askinteger(title, prompt, parent=root, initialvalue=initial)
        elif input_type == "float":
            try:
                initial = float(default_value) if default_value else 0.0
            except:
                initial = 0.0
            result = simpledialog.askfloat(title, prompt, parent=root, initialvalue=initial)
        else:
            result = simpledialog.askstring(title, prompt, parent=root, initialvalue=default_value)
        
        root.destroy()
        return result
        
    except Exception as e:
        print(f"Error in input dialog: {e}")
        return None

def create_choice_dialog(title: str, prompt: str, choices: List[str], allow_multiple: bool = False):
    """Create a choice dialog window"""
    try:
        root = tk.Tk()
        root.withdraw()
        dialog = ChoiceDialog(root, title, prompt, choices, allow_multiple)
        result = dialog.result
        root.destroy()
        return result
    except Exception as e:
        print(f"Error in choice dialog: {e}")
        return None

def create_multiline_input_dialog(title: str, prompt: str, default_value: str = ""):
    """Create a multi-line text input dialog"""
    try:
        root = tk.Tk()
        root.withdraw()
        dialog = MultilineInputDialog(root, title, prompt, default_value)
        result = dialog.result
        root.destroy()
        return result
    except Exception as e:
        print(f"Error in multiline dialog: {e}")
        return None

def show_confirmation(title: str, message: str):
    """Show confirmation dialog"""
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        root.lift()
        root.focus_force()
        result = messagebox.askyesno(title, message, parent=root)
        root.destroy()
        return result
    except Exception as e:
        print(f"Error in confirmation dialog: {e}")
        return False

def show_info(title: str, message: str):
    """Show info dialog"""
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        root.lift()
        root.focus_force()
        messagebox.showinfo(title, message, parent=root)
        root.destroy()
        return True
    except Exception as e:
        print(f"Error in info dialog: {e}")
        return False

class ChoiceDialog:
    def __init__(self, parent, title, prompt, choices, allow_multiple=False):
        self.result = None
        
        # Create the dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.grab_set()
        self.dialog.resizable(True, True)
        self.dialog.attributes('-topmost', True)
        self.dialog.lift()
        self.dialog.focus_force()
        
        # Center the dialog
        self.dialog.geometry("450x350")
        self.center_window()
        
        # Create the main frame
        main_frame = ttk.Frame(self.dialog, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Add prompt label
        prompt_label = ttk.Label(main_frame, text=prompt, wraplength=400)
        prompt_label.grid(row=0, column=0, pady=(0, 15), sticky=(tk.W, tk.E))
        
        # Create choice selection widget
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=1, column=0, pady=(0, 15), sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Use Listbox for selection
        if allow_multiple:
            self.listbox = tk.Listbox(list_frame, selectmode=tk.MULTIPLE, height=10)
        else:
            self.listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE, height=10)
            
        for choice in choices:
            self.listbox.insert(tk.END, choice)
        self.listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.listbox.configure(yscrollcommand=scrollbar.set)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=(15, 0))
        
        # OK and Cancel buttons
        ttk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=self.cancel_clicked).pack(side=tk.LEFT)
        
        # Handle window close
        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel_clicked)
        
        # Focus on listbox
        self.listbox.focus_set()
        if choices:
            self.listbox.selection_set(0)  # Select first item by default
        
        # Wait for the dialog to complete
        self.dialog.wait_window()
    
    def center_window(self):
        """Center the dialog window on screen"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
    
    def ok_clicked(self):
        selection = self.listbox.curselection()
        if selection:
            selected_items = [self.listbox.get(i) for i in selection]
            self.result = selected_items if len(selected_items) > 1 else selected_items[0]
        self.dialog.destroy()
    
    def cancel_clicked(self):
        self.result = None
        self.dialog.destroy()

class MultilineInputDialog:
    def __init__(self, parent, title, prompt, default_value=""):
        self.result = None
        
        # Create the dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.grab_set()
        self.dialog.resizable(True, True)
        self.dialog.attributes('-topmost', True)
        self.dialog.lift()
        self.dialog.focus_force()
        
        # Set size and center the dialog
        self.dialog.geometry("550x450")
        self.center_window()
        
        # Create the main frame
        main_frame = ttk.Frame(self.dialog, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Add prompt label
        prompt_label = ttk.Label(main_frame, text=prompt, wraplength=500)
        prompt_label.grid(row=0, column=0, pady=(0, 15), sticky=(tk.W, tk.E))
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=1, column=0, pady=(0, 15), sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.text_widget = tk.Text(text_frame, wrap=tk.WORD, height=15, font=("Consolas", 10))
        self.text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_widget.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Set default value
        if default_value:
            self.text_widget.insert("1.0", default_value)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=(15, 0))
        
        # OK and Cancel buttons
        ttk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=self.cancel_clicked).pack(side=tk.LEFT)
        
        # Handle window close
        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel_clicked)
        
        # Focus on text widget
        self.text_widget.focus_set()
        
        # Wait for the dialog to complete
        self.dialog.wait_window()
    
    def center_window(self):
        """Center the dialog window on screen"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
    
    def ok_clicked(self):
        self.result = self.text_widget.get("1.0", tk.END).strip()
        self.dialog.destroy()
    
    def cancel_clicked(self):
        self.result = None
        self.dialog.destroy()

# MCP Tools

@mcp.tool()
async def get_user_input(
    title: Annotated[str, Field(description="Title of the input dialog window")],
    prompt: Annotated[str, Field(description="The prompt/question to show to the user")],
    default_value: Annotated[str, Field(description="Default value to pre-fill in the input field")] = "",
    input_type: Annotated[Literal["text", "integer", "float"], Field(description="Type of input expected")] = "text",
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Create an input dialog window for the user to enter text, numbers, or other data.
    
    This tool opens a GUI dialog box where the user can input information that the LLM needs.
    Perfect for getting specific details, clarifications, or data from the user.
    """
    try:
        if ctx:
            await ctx.info(f"Requesting user input: {prompt}")
        
        # Ensure GUI is initialized
        if not ensure_gui_initialized():
            return {
                "success": False,
                "error": "GUI system not available",
                "cancelled": False
            }
        
        # Create the dialog in a separate thread to avoid blocking
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(create_input_dialog, title, prompt, default_value, input_type)
            result = future.result(timeout=300)  # 5 minute timeout
        
        if result is not None:
            if ctx:
                await ctx.info(f"User provided input: {result}")
            return {
                "success": True,
                "user_input": result,
                "input_type": input_type,
                "cancelled": False
            }
        else:
            if ctx:
                await ctx.warning("User cancelled the input dialog")
            return {
                "success": False,
                "user_input": None,
                "input_type": input_type,
                "cancelled": True
            }
    
    except Exception as e:
        if ctx:
            await ctx.error(f"Error creating input dialog: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "cancelled": False
        }

@mcp.tool()
async def get_user_choice(
    title: Annotated[str, Field(description="Title of the choice dialog window")],
    prompt: Annotated[str, Field(description="The prompt/question to show to the user")],
    choices: Annotated[List[str], Field(description="List of choices to present to the user")],
    allow_multiple: Annotated[bool, Field(description="Whether user can select multiple choices")] = False,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Create a choice dialog window for the user to select from multiple options.
    
    This tool opens a GUI dialog box with a list of choices where the user can select
    one or multiple options. Perfect for getting decisions, preferences, or selections from the user.
    """
    try:
        if ctx:
            await ctx.info(f"Requesting user choice: {prompt}")
            await ctx.debug(f"Available choices: {choices}")
        
        # Ensure GUI is initialized
        if not ensure_gui_initialized():
            return {
                "success": False,
                "error": "GUI system not available",
                "cancelled": False
            }
        
        # Create the dialog in a separate thread
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(create_choice_dialog, title, prompt, choices, allow_multiple)
            result = future.result(timeout=300)  # 5 minute timeout
        
        if result is not None:
            if ctx:
                await ctx.info(f"User selected: {result}")
            return {
                "success": True,
                "selected_choice": result,
                "selected_choices": result if isinstance(result, list) else [result],
                "allow_multiple": allow_multiple,
                "cancelled": False
            }
        else:
            if ctx:
                await ctx.warning("User cancelled the choice dialog")
            return {
                "success": False,
                "selected_choice": None,
                "selected_choices": [],
                "allow_multiple": allow_multiple,
                "cancelled": True
            }
    
    except Exception as e:
        if ctx:
            await ctx.error(f"Error creating choice dialog: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "cancelled": False
        }

@mcp.tool()
async def get_multiline_input(
    title: Annotated[str, Field(description="Title of the input dialog window")],
    prompt: Annotated[str, Field(description="The prompt/question to show to the user")],
    default_value: Annotated[str, Field(description="Default text to pre-fill in the text area")] = "",
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Create a multi-line text input dialog for the user to enter longer text content.
    
    This tool opens a GUI dialog box with a large text area where the user can input
    multiple lines of text. Perfect for getting detailed descriptions, code, or long-form content.
    """
    try:
        if ctx:
            await ctx.info(f"Requesting multiline user input: {prompt}")
        
        # Ensure GUI is initialized
        if not ensure_gui_initialized():
            return {
                "success": False,
                "error": "GUI system not available",
                "cancelled": False
            }
        
        # Create the dialog in a separate thread
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(create_multiline_input_dialog, title, prompt, default_value)
            result = future.result(timeout=300)  # 5 minute timeout
        
        if result is not None:
            if ctx:
                await ctx.info(f"User provided multiline input ({len(result)} characters)")
            return {
                "success": True,
                "user_input": result,
                "character_count": len(result),
                "line_count": len(result.split('\n')),
                "cancelled": False
            }
        else:
            if ctx:
                await ctx.warning("User cancelled the multiline input dialog")
            return {
                "success": False,
                "user_input": None,
                "cancelled": True
            }
    
    except Exception as e:
        if ctx:
            await ctx.error(f"Error creating multiline input dialog: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "cancelled": False
        }

@mcp.tool()
async def show_confirmation_dialog(
    title: Annotated[str, Field(description="Title of the confirmation dialog")],
    message: Annotated[str, Field(description="The message to show to the user")],
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Show a confirmation dialog with Yes/No buttons.
    
    This tool displays a message to the user and asks for confirmation.
    Perfect for getting approval before proceeding with an action.
    """
    try:
        if ctx:
            await ctx.info(f"Requesting user confirmation: {message}")
        
        # Ensure GUI is initialized
        if not ensure_gui_initialized():
            return {
                "success": False,
                "error": "GUI system not available",
                "confirmed": False
            }
        
        # Create the dialog in a separate thread
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(show_confirmation, title, message)
            result = future.result(timeout=300)  # 5 minute timeout
        
        if ctx:
            await ctx.info(f"User confirmation result: {'Yes' if result else 'No'}")
        
        return {
            "success": True,
            "confirmed": result,
            "response": "yes" if result else "no"
        }
    
    except Exception as e:
        if ctx:
            await ctx.error(f"Error showing confirmation dialog: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "confirmed": False
        }

@mcp.tool()
async def show_info_message(
    title: Annotated[str, Field(description="Title of the information dialog")],
    message: Annotated[str, Field(description="The information message to show to the user")],
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Show an information message to the user.
    
    This tool displays an informational message dialog to notify the user about something.
    The user just needs to click OK to acknowledge the message.
    """
    try:
        if ctx:
            await ctx.info(f"Showing info message to user: {message}")
        
        # Ensure GUI is initialized
        if not ensure_gui_initialized():
            return {
                "success": False,
                "error": "GUI system not available"
            }
        
        # Create the dialog in a separate thread
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(show_info, title, message)
            result = future.result(timeout=300)  # 5 minute timeout
        
        if ctx:
            await ctx.info("Info message acknowledged by user")
        
        return {
            "success": True,
            "acknowledged": result
        }
    
    except Exception as e:
        if ctx:
            await ctx.error(f"Error showing info message: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

# Add a health check tool
@mcp.tool()
async def health_check() -> Dict[str, Any]:
    """Check if the Human-in-the-Loop server is running and GUI is available."""
    try:
        gui_available = ensure_gui_initialized()
        
        return {
            "status": "healthy" if gui_available else "degraded",
            "gui_available": gui_available,
            "server_name": "Human-in-the-Loop Server",
            "platform": sys.platform,
            "python_version": sys.version.split()[0],
            "tools_available": [
                "get_user_input",
                "get_user_choice", 
                "get_multiline_input",
                "show_confirmation_dialog",
                "show_info_message"
            ]
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "gui_available": False,
            "error": str(e),
            "platform": sys.platform
        }

# Main execution
if __name__ == "__main__":
    print("Starting Human-in-the-Loop MCP Server...")
    print("This server provides tools for LLMs to interact with humans through GUI dialogs.")
    print("")
    print("Available tools:")
    print("get_user_input - Get text/number input from user")
    print("get_user_choice - Let user choose from options")
    print("get_multiline_input - Get multi-line text from user")
    print("show_confirmation_dialog - Ask user for yes/no confirmation")
    print("show_info_message - Display information to user")
    print("health_check - Check server status")
    print("")
    
    # Test GUI availability
    if ensure_gui_initialized():
        print("GUI system initialized successfully")
    else:
        print("Warning: GUI system may not be available")
    
    print("Starting MCP server...")
    
    # Run the server
    mcp.run()