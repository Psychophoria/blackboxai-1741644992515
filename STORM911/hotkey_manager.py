"""
Hotkey Manager for Storm911
Handles keyboard shortcuts and hotkey bindings
"""

import logging
from typing import Dict, Callable, Optional
import tkinter as tk
import customtkinter as ctk

class HotkeyManager:
    def __init__(self, root: ctk.CTk):
        """Initialize Hotkey Manager"""
        self.root = root
        self.bindings: Dict[str, Dict] = {}
        self.active = True
        
        # Default hotkey configurations
        self.default_hotkeys = {
            # Navigation
            "<Control-n>": {
                "description": "Next page",
                "category": "navigation",
                "enabled": True
            },
            "<Control-p>": {
                "description": "Previous page",
                "category": "navigation",
                "enabled": True
            },
            
            # Call Control
            "<Control-s>": {
                "description": "Start new call",
                "category": "call_control",
                "enabled": True
            },
            "<Control-e>": {
                "description": "End call",
                "category": "call_control",
                "enabled": True
            },
            "<Control-h>": {
                "description": "Hold call",
                "category": "call_control",
                "enabled": True
            },
            
            # Data Entry
            "<Control-f>": {
                "description": "Search phone number",
                "category": "data_entry",
                "enabled": True
            },
            "<Control-r>": {
                "description": "Reset form",
                "category": "data_entry",
                "enabled": True
            },
            
            # Objection Handling
            "<Alt-1>": {
                "description": "Show Group 1 objections",
                "category": "objections",
                "enabled": True
            },
            "<Alt-2>": {
                "description": "Show Group 2 objections",
                "category": "objections",
                "enabled": True
            },
            
            # Application Control
            "<Control-q>": {
                "description": "Quit application",
                "category": "application",
                "enabled": True
            },
            "<F1>": {
                "description": "Show help",
                "category": "application",
                "enabled": True
            },
            "<Control-l>": {
                "description": "Clear logs",
                "category": "application",
                "enabled": True
            },
            
            # Quick Actions
            "<F5>": {
                "description": "Refresh data",
                "category": "quick_actions",
                "enabled": True
            },
            "<Control-d>": {
                "description": "Export to PDF",
                "category": "quick_actions",
                "enabled": True
            },
            "<Control-m>": {
                "description": "Send email",
                "category": "quick_actions",
                "enabled": True
            }
        }
    
    def bind_hotkey(
        self,
        key: str,
        callback: Callable,
        description: str = "",
        category: str = "custom",
        enabled: bool = True
    ) -> None:
        """Bind a hotkey to a callback function"""
        try:
            if enabled:
                self.root.bind(key, lambda e: self._handle_hotkey(key, callback))
            
            self.bindings[key] = {
                "callback": callback,
                "description": description,
                "category": category,
                "enabled": enabled
            }
            
            logging.info(f"Hotkey bound: {key} - {description}")
            
        except Exception as e:
            logging.error(f"Error binding hotkey {key}: {str(e)}")
    
    def unbind_hotkey(self, key: str) -> None:
        """Unbind a hotkey"""
        try:
            self.root.unbind(key)
            if key in self.bindings:
                del self.bindings[key]
            logging.info(f"Hotkey unbound: {key}")
            
        except Exception as e:
            logging.error(f"Error unbinding hotkey {key}: {str(e)}")
    
    def enable_hotkey(self, key: str) -> None:
        """Enable a specific hotkey"""
        if key in self.bindings:
            binding = self.bindings[key]
            self.bind_hotkey(
                key,
                binding["callback"],
                binding["description"],
                binding["category"],
                True
            )
    
    def disable_hotkey(self, key: str) -> None:
        """Disable a specific hotkey"""
        if key in self.bindings:
            self.bindings[key]["enabled"] = False
            self.root.unbind(key)
    
    def enable_category(self, category: str) -> None:
        """Enable all hotkeys in a category"""
        for key, binding in self.bindings.items():
            if binding["category"] == category:
                self.enable_hotkey(key)
    
    def disable_category(self, category: str) -> None:
        """Disable all hotkeys in a category"""
        for key, binding in self.bindings.items():
            if binding["category"] == category:
                self.disable_hotkey(key)
    
    def enable_all(self) -> None:
        """Enable all hotkeys"""
        self.active = True
        for key, binding in self.bindings.items():
            self.enable_hotkey(key)
    
    def disable_all(self) -> None:
        """Disable all hotkeys"""
        self.active = False
        for key in self.bindings:
            self.disable_hotkey(key)
    
    def _handle_hotkey(self, key: str, callback: Callable) -> None:
        """Handle hotkey press"""
        if self.active and self.bindings[key]["enabled"]:
            try:
                callback()
            except Exception as e:
                logging.error(f"Error executing hotkey {key} callback: {str(e)}")
    
    def get_hotkey_info(self, key: str) -> Optional[Dict]:
        """Get information about a specific hotkey"""
        return self.bindings.get(key)
    
    def get_all_hotkeys(self) -> Dict:
        """Get all registered hotkeys and their information"""
        return self.bindings
    
    def get_category_hotkeys(self, category: str) -> Dict:
        """Get all hotkeys in a specific category"""
        return {
            key: binding
            for key, binding in self.bindings.items()
            if binding["category"] == category
        }
    
    def setup_default_bindings(self, callbacks: Dict[str, Callable]) -> None:
        """Set up default hotkey bindings"""
        for key, config in self.default_hotkeys.items():
            if key in callbacks:
                self.bind_hotkey(
                    key,
                    callbacks[key],
                    config["description"],
                    config["category"],
                    config["enabled"]
                )
    
    def generate_help_text(self) -> str:
        """Generate help text for all hotkeys"""
        help_text = "Keyboard Shortcuts:\n\n"
        
        # Group by category
        categories = {}
        for key, binding in self.bindings.items():
            category = binding["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append((key, binding))
        
        # Generate text by category
        for category in sorted(categories.keys()):
            help_text += f"{category.upper()}:\n"
            for key, binding in sorted(categories[category]):
                status = "Enabled" if binding["enabled"] else "Disabled"
                help_text += f"  {key}: {binding['description']} ({status})\n"
            help_text += "\n"
        
        return help_text
    
    def show_help_dialog(self) -> None:
        """Show help dialog with hotkey information"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Keyboard Shortcuts")
        dialog.geometry("600x400")
        
        # Make dialog modal
        dialog.grab_set()
        
        # Add help text
        text = ctk.CTkTextbox(dialog, wrap="word")
        text.pack(fill="both", expand=True, padx=10, pady=10)
        text.insert("1.0", self.generate_help_text())
        text.configure(state="disabled")
        
        # Close button
        close_button = ctk.CTkButton(
            dialog,
            text="Close",
            command=dialog.destroy
        )
        close_button.pack(pady=10)
