"""
Dialog Manager for Storm911
Handles application dialogs, popups, and notifications
"""

import tkinter as tk
from typing import Optional, Callable, Any, Dict
import customtkinter as ctk
import logging

class DialogManager:
    def __init__(self, root: ctk.CTk, theme_manager: Any):
        """Initialize Dialog Manager"""
        self.root = root
        self.theme_manager = theme_manager
        
        # Track active dialogs
        self.active_dialogs = {}
    
    def show_message(
        self,
        title: str,
        message: str,
        level: str = "info"
    ) -> None:
        """Show message dialog"""
        dialog = MessageDialog(
            self.root,
            title,
            message,
            level,
            self.theme_manager
        )
        dialog.show()
    
    def show_confirmation(
        self,
        title: str,
        message: str,
        callback: Callable[[bool], None]
    ) -> None:
        """Show confirmation dialog"""
        dialog = ConfirmationDialog(
            self.root,
            title,
            message,
            callback,
            self.theme_manager
        )
        dialog.show()
    
    def close_all(self) -> None:
        """Close all active dialogs"""
        for dialog in list(self.active_dialogs.values()):
            dialog.destroy()
        self.active_dialogs.clear()

class BaseDialog:
    """Base class for dialogs"""
    def __init__(
        self,
        root: ctk.CTk,
        title: str,
        theme_manager: Any
    ):
        self.root = root
        self.title = title
        self.theme_manager = theme_manager
        self.dialog = None
    
    def show(self) -> None:
        """Show dialog"""
        self.dialog = ctk.CTkToplevel(self.root)
        self.dialog.title(self.title)
        self.dialog.transient(self.root)
        self.dialog.grab_set()
        
        # Center dialog
        self.center_dialog()
        
        # Apply theme
        colors = self.theme_manager.get_color_scheme()
        self.dialog.configure(fg_color=colors["background"])
    
    def center_dialog(self) -> None:
        """Center dialog on screen"""
        if self.dialog:
            self.dialog.update_idletasks()
            width = self.dialog.winfo_width()
            height = self.dialog.winfo_height()
            x = (self.root.winfo_width() // 2) - (width // 2)
            y = (self.root.winfo_height() // 2) - (height // 2)
            self.dialog.geometry(f"+{x}+{y}")
    
    def destroy(self) -> None:
        """Destroy dialog"""
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None

class MessageDialog(BaseDialog):
    """Dialog for displaying messages"""
    def __init__(
        self,
        root: ctk.CTk,
        title: str,
        message: str,
        level: str,
        theme_manager: Any
    ):
        super().__init__(root, title, theme_manager)
        self.message = message
        self.level = level
    
    def show(self) -> None:
        """Show message dialog"""
        super().show()
        
        # Message label
        label = ctk.CTkLabel(
            self.dialog,
            text=self.message,
            wraplength=300
        )
        label.pack(padx=20, pady=20)
        
        # OK button
        button = ctk.CTkButton(
            self.dialog,
            text="OK",
            command=self.destroy
        )
        button.pack(pady=10)
        
        # Apply theme
        colors = self.theme_manager.get_color_scheme()
        if self.level == "error":
            button.configure(fg_color=colors["danger"])
        elif self.level == "warning":
            button.configure(fg_color=colors["warning"])
        elif self.level == "success":
            button.configure(fg_color=colors["success"])
        else:
            button.configure(fg_color=colors["primary"])

class ConfirmationDialog(BaseDialog):
    """Dialog for confirmations"""
    def __init__(
        self,
        root: ctk.CTk,
        title: str,
        message: str,
        callback: Callable[[bool], None],
        theme_manager: Any
    ):
        super().__init__(root, title, theme_manager)
        self.message = message
        self.callback = callback
    
    def show(self) -> None:
        """Show confirmation dialog"""
        super().show()
        
        # Message label
        label = ctk.CTkLabel(
            self.dialog,
            text=self.message,
            wraplength=300
        )
        label.pack(padx=20, pady=20)
        
        # Button frame
        button_frame = ctk.CTkFrame(self.dialog)
        button_frame.pack(pady=10)
        
        # Yes button
        yes_button = ctk.CTkButton(
            button_frame,
            text="Yes",
            command=lambda: self._handle_response(True)
        )
        yes_button.pack(side="left", padx=5)
        
        # No button
        no_button = ctk.CTkButton(
            button_frame,
            text="No",
            command=lambda: self._handle_response(False)
        )
        no_button.pack(side="left", padx=5)
        
        # Apply theme
        colors = self.theme_manager.get_color_scheme()
        yes_button.configure(fg_color=colors["success"])
        no_button.configure(fg_color=colors["danger"])
    
    def _handle_response(self, response: bool) -> None:
        """Handle user response"""
        self.destroy()
        if self.callback:
            self.callback(response)
