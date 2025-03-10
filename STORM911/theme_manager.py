"""
Theme Manager for Storm911
Handles application themes, styles, and visual customization
"""

import json
import os
from typing import Dict, Any
import customtkinter as ctk

class ThemeManager:
    def __init__(self):
        """Initialize Theme Manager"""
        # Default color schemes
        self.color_schemes = {
            "dark": {
                "primary": "#007bff",
                "secondary": "#6c757d",
                "success": "#28a745",
                "danger": "#dc3545",
                "warning": "#ffc107",
                "info": "#17a2b8",
                "light": "#f8f9fa",
                "dark": "#343a40",
                "background": "#2b2b2b",
                "foreground": "#ffffff",
                "border": "#404040",
                "hover": "#0056b3",
                "active": "#004085",
                "disabled": "#6c757d"
            },
            "light": {
                "primary": "#0056b3",
                "secondary": "#6c757d",
                "success": "#28a745",
                "danger": "#dc3545",
                "warning": "#ffc107",
                "info": "#17a2b8",
                "light": "#f8f9fa",
                "dark": "#343a40",
                "background": "#ffffff",
                "foreground": "#000000",
                "border": "#dee2e6",
                "hover": "#007bff",
                "active": "#0056b3",
                "disabled": "#6c757d"
            }
        }

        # Font configurations
        self.font_configs = {
            "small": {
                "size": 10,
                "title_size": 18,
                "header_size": 14,
                "button_size": 10
            },
            "normal": {
                "size": 12,
                "title_size": 24,
                "header_size": 16,
                "button_size": 12
            },
            "large": {
                "size": 14,
                "title_size": 28,
                "header_size": 18,
                "button_size": 14
            }
        }

        # Widget styles
        self.widget_styles = {
            "button": {
                "corner_radius": 6,
                "border_width": 0,
                "padding": 10
            },
            "entry": {
                "corner_radius": 6,
                "border_width": 1,
                "padding": 10
            },
            "frame": {
                "corner_radius": 10,
                "border_width": 1,
                "padding": 10
            }
        }

        # Initialize with default theme
        self.current_theme = "dark"
        self.current_font_size = "normal"
        self.apply_theme(self.current_theme)

    def apply_theme(self, theme_name: str) -> None:
        """Apply selected theme to application"""
        if theme_name in self.color_schemes:
            self.current_theme = theme_name
            colors = self.color_schemes[theme_name]

            # Set CustomTkinter appearance mode
            ctk.set_appearance_mode("dark" if theme_name == "dark" else "light")

            # Set CustomTkinter color theme
            ctk.set_default_color_theme("blue")  # Base theme

    def set_font_size(self, size: str) -> None:
        """Set application font size"""
        if size in self.font_configs:
            self.current_font_size = size

    def get_font_config(self) -> Dict:
        """Get current font configuration"""
        return self.font_configs[self.current_font_size]

    def get_color_scheme(self) -> Dict:
        """Get current color scheme"""
        return self.color_schemes[self.current_theme]

    def get_widget_style(self, widget_type: str) -> Dict:
        """Get style configuration for specific widget type"""
        return self.widget_styles.get(widget_type, {})

    def style_button(self, button: ctk.CTkButton, style: str = "default") -> None:
        """Apply specific style to button"""
        colors = self.get_color_scheme()
        font_config = self.get_font_config()
        button_style = self.get_widget_style("button")

        style_config = {
            "corner_radius": button_style["corner_radius"],
            "border_width": button_style["border_width"],
            "font": ("Arial", font_config["button_size"])
        }

        if style == "primary":
            style_config.update({
                "fg_color": colors["primary"],
                "hover_color": colors["hover"],
                "text_color": colors["light"]
            })
        elif style == "secondary":
            style_config.update({
                "fg_color": colors["secondary"],
                "hover_color": colors["dark"],
                "text_color": colors["light"]
            })
        elif style == "danger":
            style_config.update({
                "fg_color": colors["danger"],
                "hover_color": "#c82333",
                "text_color": colors["light"]
            })
        elif style == "success":
            style_config.update({
                "fg_color": colors["success"],
                "hover_color": "#218838",
                "text_color": colors["light"]
            })

        button.configure(**style_config)

    def style_entry(self, entry: ctk.CTkEntry) -> None:
        """Apply style to entry widget"""
        colors = self.get_color_scheme()
        font_config = self.get_font_config()
        entry_style = self.get_widget_style("entry")

        entry.configure(
            fg_color=colors["background"],
            border_color=colors["border"],
            text_color=colors["foreground"],
            corner_radius=entry_style["corner_radius"],
            border_width=entry_style["border_width"],
            font=("Arial", font_config["size"])
        )

    def style_frame(self, frame: ctk.CTkFrame) -> None:
        """Apply style to frame widget"""
        colors = self.get_color_scheme()
        frame_style = self.get_widget_style("frame")

        frame.configure(
            fg_color=colors["background"],
            border_color=colors["border"],
            corner_radius=frame_style["corner_radius"],
            border_width=frame_style["border_width"]
        )

    def get_text_style(self, style_type: str = "normal") -> Dict:
        """Get text style configuration"""
        colors = self.get_color_scheme()
        font_config = self.get_font_config()

        styles = {
            "title": {
                "font": ("Arial", font_config["title_size"], "bold"),
                "fg": colors["foreground"]
            },
            "header": {
                "font": ("Arial", font_config["header_size"], "bold"),
                "fg": colors["foreground"]
            },
            "normal": {
                "font": ("Arial", font_config["size"]),
                "fg": colors["foreground"]
            },
            "small": {
                "font": ("Arial", font_config["size"] - 2),
                "fg": colors["foreground"]
            }
        }

        return styles.get(style_type, styles["normal"])

    def create_custom_theme(self, name: str, colors: Dict) -> None:
        """Create new custom theme"""
        self.color_schemes[name] = colors

    def export_theme(self, name: str, filepath: str) -> bool:
        """Export theme configuration to file"""
        if name in self.color_schemes:
            try:
                with open(filepath, 'w') as f:
                    json.dump(self.color_schemes[name], f, indent=2)
                return True
            except Exception:
                return False
        return False

    def import_theme(self, filepath: str) -> bool:
        """Import theme configuration from file"""
        try:
            with open(filepath, 'r') as f:
                theme_data = json.load(f)
                name = os.path.splitext(os.path.basename(filepath))[0]
                self.create_custom_theme(name, theme_data)
                return True
        except Exception:
            return False
