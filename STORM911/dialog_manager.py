"""
Dialog Manager for Storm911
Handles application dialogs, popups, and notifications
"""

import tkinter as tk
from typing import Optional, Callable, Any, Dict
import customtkinter as ctk
from theme_manager import ThemeManager

class DialogManager:
    def __init__(self, root: ctk.CTk, theme_manager: ThemeManager):
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
            self.theme_manager,
            title,
            message,
            level
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
            self.theme_manager,
            title,
            message,
            callback
        )
        dialog.show()
    
    def show_input(
        self,
        title: str,
        message: str,
        callback: Callable[[str], None],
        default: str = "",
        input_type: str = "text"
    ) -> None:
        """Show input dialog"""
        dialog = InputDialog(
            self.root,
            self.theme_manager,
            title,
            message,
            callback,
            default,
            input_type
        )
        dialog.show()
    
    def show_form(
        self,
        title: str,
        fields: Dict[str, Dict],
        callback: Callable[[Dict], None]
    ) -> None:
        """Show form dialog"""
        dialog = FormDialog(
            self.root,
            self.theme_manager,
            title,
            fields,
            callback
        )
        dialog.show()
    
    def show_progress(
        self,
        title: str,
        message: str,
        callback: Optional[Callable] = None
    ) -> 'ProgressDialog':
        """Show progress dialog"""
        dialog = ProgressDialog(
            self.root,
            self.theme_manager,
            title,
            message,
            callback
        )
        dialog.show()
        return dialog
    
    def show_notification(
        self,
        message: str,
        duration: int = 3000,
        level: str = "info"
    ) -> None:
        """Show notification popup"""
        notification = NotificationPopup(
            self.root,
            self.theme_manager,
            message,
            duration,
            level
        )
        notification.show()
    
    def close_all(self) -> None:
        """Close all active dialogs"""
        for dialog in list(self.active_dialogs.values()):
            dialog.close()

class BaseDialog:
    """Base class for dialogs"""
    def __init__(
        self,
        root: ctk.CTk,
        theme_manager: ThemeManager,
        title: str
    ):
        self.root = root
        self.theme_manager = theme_manager
        self.title = title
        self.dialog = None
    
    def create_dialog(self) -> None:
        """Create dialog window"""
        self.dialog = ctk.CTkToplevel(self.root)
        self.dialog.title(self.title)
        self.dialog.transient(self.root)
        self.dialog.grab_set()
        
        # Center dialog
        self.center_dialog()
    
    def center_dialog(self) -> None:
        """Center dialog on screen"""
        if self.dialog:
            self.dialog.update_idletasks()
            width = self.dialog.winfo_width()
            height = self.dialog.winfo_height()
            x = (self.root.winfo_width() // 2) - (width // 2)
            y = (self.root.winfo_height() // 2) - (height // 2)
            self.dialog.geometry(f"+{x}+{y}")
    
    def show(self) -> None:
        """Show dialog"""
        self.create_dialog()
    
    def close(self) -> None:
        """Close dialog"""
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None

class MessageDialog(BaseDialog):
    """Dialog for displaying messages"""
    def __init__(
        self,
        root: ctk.CTk,
        theme_manager: ThemeManager,
        title: str,
        message: str,
        level: str = "info"
    ):
        super().__init__(root, theme_manager, title)
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
            command=self.close
        )
        button.pack(pady=10)
        
        # Style based on level
        colors = self.theme_manager.get_color_scheme()
        if self.level == "error":
            self.dialog.configure(fg_color=colors["danger"])
        elif self.level == "warning":
            self.dialog.configure(fg_color=colors["warning"])
        elif self.level == "success":
            self.dialog.configure(fg_color=colors["success"])

class ConfirmationDialog(BaseDialog):
    """Dialog for confirmations"""
    def __init__(
        self,
        root: ctk.CTk,
        theme_manager: ThemeManager,
        title: str,
        message: str,
        callback: Callable[[bool], None]
    ):
        super().__init__(root, theme_manager, title)
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
            command=lambda: self.handle_response(True)
        )
        yes_button.pack(side="left", padx=5)
        
        # No button
        no_button = ctk.CTkButton(
            button_frame,
            text="No",
            command=lambda: self.handle_response(False)
        )
        no_button.pack(side="left", padx=5)
    
    def handle_response(self, response: bool) -> None:
        """Handle user response"""
        self.close()
        if self.callback:
            self.callback(response)

class InputDialog(BaseDialog):
    """Dialog for user input"""
    def __init__(
        self,
        root: ctk.CTk,
        theme_manager: ThemeManager,
        title: str,
        message: str,
        callback: Callable[[str], None],
        default: str = "",
        input_type: str = "text"
    ):
        super().__init__(root, theme_manager, title)
        self.message = message
        self.callback = callback
        self.default = default
        self.input_type = input_type
    
    def show(self) -> None:
        """Show input dialog"""
        super().show()
        
        # Message label
        label = ctk.CTkLabel(
            self.dialog,
            text=self.message,
            wraplength=300
        )
        label.pack(padx=20, pady=10)
        
        # Input field
        self.input_var = tk.StringVar(value=self.default)
        input_field = ctk.CTkEntry(
            self.dialog,
            textvariable=self.input_var,
            show="*" if self.input_type == "password" else ""
        )
        input_field.pack(padx=20, pady=10, fill="x")
        
        # Button frame
        button_frame = ctk.CTkFrame(self.dialog)
        button_frame.pack(pady=10)
        
        # OK button
        ok_button = ctk.CTkButton(
            button_frame,
            text="OK",
            command=self.handle_ok
        )
        ok_button.pack(side="left", padx=5)
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.close
        )
        cancel_button.pack(side="left", padx=5)
        
        # Focus input field
        input_field.focus()
    
    def handle_ok(self) -> None:
        """Handle OK button click"""
        value = self.input_var.get()
        self.close()
        if self.callback:
            self.callback(value)

class FormDialog(BaseDialog):
    """Dialog for form input"""
    def __init__(
        self,
        root: ctk.CTk,
        theme_manager: ThemeManager,
        title: str,
        fields: Dict[str, Dict],
        callback: Callable[[Dict], None]
    ):
        super().__init__(root, theme_manager, title)
        self.fields = fields
        self.callback = callback
        self.field_vars = {}
    
    def show(self) -> None:
        """Show form dialog"""
        super().show()
        
        # Create form fields
        for field_id, field_config in self.fields.items():
            # Field frame
            field_frame = ctk.CTkFrame(self.dialog)
            field_frame.pack(fill="x", padx=20, pady=5)
            
            # Label
            label = ctk.CTkLabel(
                field_frame,
                text=field_config.get("label", field_id)
            )
            label.pack(side="left")
            
            # Input field
            field_type = field_config.get("type", "text")
            if field_type == "checkbox":
                self.field_vars[field_id] = tk.BooleanVar(
                    value=field_config.get("default", False)
                )
                field = ctk.CTkCheckBox(
                    field_frame,
                    text="",
                    variable=self.field_vars[field_id]
                )
            else:
                self.field_vars[field_id] = tk.StringVar(
                    value=field_config.get("default", "")
                )
                field = ctk.CTkEntry(
                    field_frame,
                    textvariable=self.field_vars[field_id],
                    show="*" if field_type == "password" else ""
                )
            field.pack(side="right", padx=5)
        
        # Button frame
        button_frame = ctk.CTkFrame(self.dialog)
        button_frame.pack(pady=10)
        
        # OK button
        ok_button = ctk.CTkButton(
            button_frame,
            text="OK",
            command=self.handle_ok
        )
        ok_button.pack(side="left", padx=5)
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.close
        )
        cancel_button.pack(side="left", padx=5)
    
    def handle_ok(self) -> None:
        """Handle OK button click"""
        values = {
            field_id: var.get()
            for field_id, var in self.field_vars.items()
        }
        self.close()
        if self.callback:
            self.callback(values)

class ProgressDialog(BaseDialog):
    """Dialog for showing progress"""
    def __init__(
        self,
        root: ctk.CTk,
        theme_manager: ThemeManager,
        title: str,
        message: str,
        callback: Optional[Callable] = None
    ):
        super().__init__(root, theme_manager, title)
        self.message = message
        self.callback = callback
    
    def show(self) -> None:
        """Show progress dialog"""
        super().show()
        
        # Message label
        self.message_label = ctk.CTkLabel(
            self.dialog,
            text=self.message,
            wraplength=300
        )
        self.message_label.pack(padx=20, pady=10)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.dialog)
        self.progress_bar.pack(padx=20, pady=10, fill="x")
        self.progress_bar.set(0)
        
        if self.callback:
            self.callback(self)
    
    def update_progress(
        self,
        value: float,
        message: Optional[str] = None
    ) -> None:
        """Update progress value and message"""
        self.progress_bar.set(value)
        if message:
            self.message_label.configure(text=message)
        self.dialog.update()

class NotificationPopup(BaseDialog):
    """Popup for notifications"""
    def __init__(
        self,
        root: ctk.CTk,
        theme_manager: ThemeManager,
        message: str,
        duration: int = 3000,
        level: str = "info"
    ):
        super().__init__(root, theme_manager, "")
        self.message = message
        self.duration = duration
        self.level = level
    
    def show(self) -> None:
        """Show notification popup"""
        super().show()
        
        # Configure window
        self.dialog.overrideredirect(True)
        self.dialog.attributes("-topmost", True)
        
        # Message label
        label = ctk.CTkLabel(
            self.dialog,
            text=self.message,
            wraplength=300
        )
        label.pack(padx=20, pady=10)
        
        # Style based on level
        colors = self.theme_manager.get_color_scheme()
        if self.level == "error":
            self.dialog.configure(fg_color=colors["danger"])
        elif self.level == "warning":
            self.dialog.configure(fg_color=colors["warning"])
        elif self.level == "success":
            self.dialog.configure(fg_color=colors["success"])
        
        # Position at bottom right
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - width - 20
        y = screen_height - height - 40
        self.dialog.geometry(f"+{x}+{y}")
        
        # Schedule auto-close
        self.root.after(self.duration, self.close)
