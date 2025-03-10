"""
Menu Manager for Storm911
Handles application menu bar and toolbar functionality
"""

import tkinter as tk
import customtkinter as ctk
from typing import Dict, Any
import logging

class MenuManager:
    def __init__(self, root: ctk.CTk, managers: Dict[str, Any], handlers: Dict[str, Any]):
        """Initialize Menu Manager"""
        self.root = root
        self.managers = managers
        self.handlers = handlers
        
        # Create menu bar
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # Create toolbar
        self.toolbar = None
        
        # Initialize menus
        self._create_file_menu()
        self._create_edit_menu()
        self._create_view_menu()
        self._create_tools_menu()
        self._create_help_menu()
    
    def _create_file_menu(self) -> None:
        """Create File menu"""
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        
        file_menu.add_command(
            label="New Call",
            command=self._new_call,
            accelerator="Ctrl+N"
        )
        file_menu.add_command(
            label="End Call",
            command=self._end_call,
            accelerator="Ctrl+E"
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Export PDF",
            command=self._export_pdf,
            accelerator="Ctrl+P"
        )
        file_menu.add_command(
            label="Send Email",
            command=self._send_email,
            accelerator="Ctrl+M"
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Exit",
            command=self._exit_app,
            accelerator="Ctrl+Q"
        )
    
    def _create_edit_menu(self) -> None:
        """Create Edit menu"""
        edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=edit_menu)
        
        edit_menu.add_command(
            label="Clear Form",
            command=self._clear_form,
            accelerator="Ctrl+R"
        )
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Copy",
            command=lambda: self.root.focus_get().event_generate("<<Copy>>"),
            accelerator="Ctrl+C"
        )
        edit_menu.add_command(
            label="Cut",
            command=lambda: self.root.focus_get().event_generate("<<Cut>>"),
            accelerator="Ctrl+X"
        )
        edit_menu.add_command(
            label="Paste",
            command=lambda: self.root.focus_get().event_generate("<<Paste>>"),
            accelerator="Ctrl+V"
        )
    
    def _create_view_menu(self) -> None:
        """Create View menu"""
        view_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="View", menu=view_menu)
        
        # Theme submenu
        theme_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Theme", menu=theme_menu)
        
        theme_menu.add_radiobutton(
            label="Light",
            command=lambda: self._change_theme("light")
        )
        theme_menu.add_radiobutton(
            label="Dark",
            command=lambda: self._change_theme("dark")
        )
        
        # Font size submenu
        font_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Font Size", menu=font_menu)
        
        font_menu.add_radiobutton(
            label="Small",
            command=lambda: self._change_font_size("small")
        )
        font_menu.add_radiobutton(
            label="Normal",
            command=lambda: self._change_font_size("normal")
        )
        font_menu.add_radiobutton(
            label="Large",
            command=lambda: self._change_font_size("large")
        )
        
        view_menu.add_separator()
        view_menu.add_checkbutton(
            label="Show Toolbar",
            command=self._toggle_toolbar
        )
        view_menu.add_checkbutton(
            label="Show Status Bar",
            command=self._toggle_status_bar
        )
    
    def _create_tools_menu(self) -> None:
        """Create Tools menu"""
        tools_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Tools", menu=tools_menu)
        
        tools_menu.add_command(
            label="Settings",
            command=self._show_settings
        )
        tools_menu.add_command(
            label="Clear Logs",
            command=self._clear_logs
        )
        tools_menu.add_separator()
        tools_menu.add_command(
            label="Test Email",
            command=self._test_email
        )
        tools_menu.add_command(
            label="Test API",
            command=self._test_api
        )
    
    def _create_help_menu(self) -> None:
        """Create Help menu"""
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=help_menu)
        
        help_menu.add_command(
            label="View Help",
            command=self._show_help,
            accelerator="F1"
        )
        help_menu.add_command(
            label="Keyboard Shortcuts",
            command=self._show_shortcuts
        )
        help_menu.add_separator()
        help_menu.add_command(
            label="About",
            command=self._show_about
        )
    
    def create_toolbar(self, parent: ctk.CTkFrame) -> None:
        """Create toolbar"""
        self.toolbar = ctk.CTkFrame(parent)
        self.toolbar.pack(fill="x", padx=5, pady=2)
        
        # New Call button
        new_call_btn = ctk.CTkButton(
            self.toolbar,
            text="New Call",
            command=self._new_call,
            width=80
        )
        new_call_btn.pack(side="left", padx=2)
        
        # End Call button
        end_call_btn = ctk.CTkButton(
            self.toolbar,
            text="End Call",
            command=self._end_call,
            width=80
        )
        end_call_btn.pack(side="left", padx=2)
        
        # Separator
        ctk.CTkFrame(
            self.toolbar,
            width=2,
            height=25
        ).pack(side="left", padx=5, pady=2)
        
        # Export PDF button
        export_btn = ctk.CTkButton(
            self.toolbar,
            text="Export PDF",
            command=self._export_pdf,
            width=80
        )
        export_btn.pack(side="left", padx=2)
        
        # Send Email button
        email_btn = ctk.CTkButton(
            self.toolbar,
            text="Send Email",
            command=self._send_email,
            width=80
        )
        email_btn.pack(side="left", padx=2)
    
    def _new_call(self) -> None:
        """Handle new call"""
        try:
            # Check if current call needs to be saved
            if self.managers['state'].get_current_call():
                self.managers['dialog'].show_confirmation(
                    "New Call",
                    "Current call not saved. Continue?",
                    self._confirm_new_call
                )
            else:
                self._confirm_new_call(True)
            
        except Exception as e:
            logging.error(f"Error starting new call: {str(e)}")
            self.managers['dialog'].show_message(
                "Error",
                "Failed to start new call",
                "error"
            )
    
    def _confirm_new_call(self, confirmed: bool) -> None:
        """Handle new call confirmation"""
        if confirmed:
            try:
                # Clear current call
                self.managers['state'].clear_current_call()
                
                # Reset UI
                self.root.event_generate("<<ResetUI>>")
                
            except Exception as e:
                logging.error(f"Error confirming new call: {str(e)}")
    
    def _end_call(self) -> None:
        """Handle end call"""
        try:
            if self.managers['state'].get_current_call():
                self.managers['dialog'].show_confirmation(
                    "End Call",
                    "Are you sure you want to end this call?",
                    self._confirm_end_call
                )
            
        except Exception as e:
            logging.error(f"Error ending call: {str(e)}")
            self.managers['dialog'].show_message(
                "Error",
                "Failed to end call",
                "error"
            )
    
    def _confirm_end_call(self, confirmed: bool) -> None:
        """Handle end call confirmation"""
        if confirmed:
            try:
                # Show disposition dialog
                self.root.event_generate("<<ShowDisposition>>")
                
            except Exception as e:
                logging.error(f"Error confirming end call: {str(e)}")
    
    def _export_pdf(self) -> None:
        """Handle PDF export"""
        try:
            self.root.event_generate("<<ExportPDF>>")
            
        except Exception as e:
            logging.error(f"Error exporting PDF: {str(e)}")
            self.managers['dialog'].show_message(
                "Error",
                "Failed to export PDF",
                "error"
            )
    
    def _send_email(self) -> None:
        """Handle email send"""
        try:
            self.root.event_generate("<<SendEmail>>")
            
        except Exception as e:
            logging.error(f"Error sending email: {str(e)}")
            self.managers['dialog'].show_message(
                "Error",
                "Failed to send email",
                "error"
            )
    
    def _exit_app(self) -> None:
        """Handle application exit"""
        try:
            self.root.event_generate("<<Exit>>")
            
        except Exception as e:
            logging.error(f"Error exiting application: {str(e)}")
            self.root.destroy()
    
    def _clear_form(self) -> None:
        """Handle form clear"""
        try:
            self.root.event_generate("<<ClearForm>>")
            
        except Exception as e:
            logging.error(f"Error clearing form: {str(e)}")
    
    def _change_theme(self, theme: str) -> None:
        """Handle theme change"""
        try:
            self.managers['theme'].apply_theme(theme)
            
        except Exception as e:
            logging.error(f"Error changing theme: {str(e)}")
    
    def _change_font_size(self, size: str) -> None:
        """Handle font size change"""
        try:
            self.managers['theme'].set_font_size(size)
            
        except Exception as e:
            logging.error(f"Error changing font size: {str(e)}")
    
    def _toggle_toolbar(self) -> None:
        """Handle toolbar toggle"""
        if self.toolbar:
            if self.toolbar.winfo_viewable():
                self.toolbar.pack_forget()
            else:
                self.toolbar.pack(fill="x", padx=5, pady=2)
    
    def _toggle_status_bar(self) -> None:
        """Handle status bar toggle"""
        self.root.event_generate("<<ToggleStatusBar>>")
    
    def _show_settings(self) -> None:
        """Show settings dialog"""
        try:
            self.root.event_generate("<<ShowSettings>>")
            
        except Exception as e:
            logging.error(f"Error showing settings: {str(e)}")
    
    def _clear_logs(self) -> None:
        """Handle log clear"""
        try:
            self.managers['event'].clear_logs()
            self.managers['dialog'].show_message(
                "Success",
                "Logs cleared successfully",
                "success"
            )
            
        except Exception as e:
            logging.error(f"Error clearing logs: {str(e)}")
            self.managers['dialog'].show_message(
                "Error",
                "Failed to clear logs",
                "error"
            )
    
    def _test_email(self) -> None:
        """Handle email test"""
        try:
            self.handlers['email'].send_test_email(
                self.managers['settings'].get_setting(
                    'email',
                    'test_recipient'
                )
            )
            self.managers['dialog'].show_message(
                "Success",
                "Test email sent successfully",
                "success"
            )
            
        except Exception as e:
            logging.error(f"Error testing email: {str(e)}")
            self.managers['dialog'].show_message(
                "Error",
                "Failed to send test email",
                "error"
            )
    
    def _test_api(self) -> None:
        """Handle API test"""
        try:
            success, message = self.handlers['api'].validate_credentials()
            
            if success:
                self.managers['dialog'].show_message(
                    "Success",
                    "API connection successful",
                    "success"
                )
            else:
                self.managers['dialog'].show_message(
                    "Error",
                    message,
                    "error"
                )
            
        except Exception as e:
            logging.error(f"Error testing API: {str(e)}")
            self.managers['dialog'].show_message(
                "Error",
                "Failed to test API connection",
                "error"
            )
    
    def _show_help(self) -> None:
        """Show help dialog"""
        try:
            self.root.event_generate("<<ShowHelp>>")
            
        except Exception as e:
            logging.error(f"Error showing help: {str(e)}")
    
    def _show_shortcuts(self) -> None:
        """Show keyboard shortcuts"""
        try:
            self.managers['hotkey'].show_help_dialog()
            
        except Exception as e:
            logging.error(f"Error showing shortcuts: {str(e)}")
    
    def _show_about(self) -> None:
        """Show about dialog"""
        try:
            self.root.event_generate("<<ShowAbout>>")
            
        except Exception as e:
            logging.error(f"Error showing about dialog: {str(e)}")
