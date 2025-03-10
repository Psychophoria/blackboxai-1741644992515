"""
Storm911 - Call Center Application
Main application entry point
"""

import os
import sys
import logging
from typing import Optional
import customtkinter as ctk

from app_initializer import AppInitializer
from config import APP_NAME, APP_VERSION

class Storm911App:
    def __init__(self):
        """Initialize Storm911 application"""
        # Configure customtkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize application components
        self.initializer = AppInitializer()
        self.root: Optional[ctk.CTk] = None
        
        # Store manager and handler references
        self.managers = {}
        self.handlers = {}
    
    def setup(self) -> None:
        """Set up application"""
        try:
            # Initialize application
            self.root = self.initializer.initialize_app()
            
            # Store references to managers and handlers
            self.managers = self.initializer.managers
            self.handlers = self.initializer.handlers
            
            # Create main UI
            self.create_main_ui()
            
            # Show splash screen
            self.show_splash_screen()
            
        except Exception as e:
            logging.error(f"Error setting up application: {str(e)}")
            self.show_error_and_exit("Failed to start application")
    
    def create_main_ui(self) -> None:
        """Create main application UI"""
        try:
            # Get main container reference
            main_container = self.root.main_container
            
            # Create header
            self.create_header(main_container)
            
            # Create main panels
            self.create_caller_info_panel(main_container)
            self.create_transcript_panel(main_container)
            self.create_objections_panel(main_container)
            
            # Create status bar
            self.create_status_bar(main_container)
            
        except Exception as e:
            logging.error(f"Error creating main UI: {str(e)}")
            self.show_error_and_exit("Failed to create user interface")
    
    def create_header(self, parent: ctk.CTkFrame) -> None:
        """Create application header"""
        try:
            # Create header frame
            header_frame = ctk.CTkFrame(parent)
            header_frame.pack(fill="x", padx=5, pady=5)
            
            # Try to load logos
            try:
                # AssureCall logo
                assurecall_logo = ctk.CTkImage(
                    light_image=os.path.join("assets", "assurecall.png"),
                    dark_image=os.path.join("assets", "assurecall.png")
                )
                ctk.CTkLabel(
                    header_frame,
                    image=assurecall_logo,
                    text=""
                ).pack(side="left", padx=10)
            except:
                # Create text label if image fails to load
                ctk.CTkLabel(
                    header_frame,
                    text="AssureCall",
                    font=("Arial", 16)
                ).pack(side="left", padx=10)
            
            try:
                # Storm911 logo
                storm911_logo = ctk.CTkImage(
                    light_image=os.path.join("assets", "storm911.png"),
                    dark_image=os.path.join("assets", "storm911.png")
                )
                ctk.CTkLabel(
                    header_frame,
                    image=storm911_logo,
                    text=""
                ).pack(side="left", padx=10)
            except:
                # Create text label if image fails to load
                ctk.CTkLabel(
                    header_frame,
                    text="Storm911",
                    font=("Arial", 24, "bold")
                ).pack(side="left", padx=10)
            
        except Exception as e:
            logging.error(f"Error creating header: {str(e)}")
            raise
    
    def create_caller_info_panel(self, parent: ctk.CTkFrame) -> None:
        """Create caller information panel"""
        from caller_info_panel import CallerInfoPanel
        panel = CallerInfoPanel(self.root, self.managers, self.handlers)
        panel.create_panel(parent)
    
    def create_transcript_panel(self, parent: ctk.CTkFrame) -> None:
        """Create transcript panel"""
        from transcript_panel import TranscriptPanel
        panel = TranscriptPanel(self.root, self.managers, self.handlers)
        panel.create_panel(parent)
    
    def create_objections_panel(self, parent: ctk.CTkFrame) -> None:
        """Create objections panel"""
        from ui_panels import ObjectionsPanel
        panel = ObjectionsPanel(self.root, self.managers, self.handlers)
        panel.create_panel(parent)
    
    def create_status_bar(self, parent: ctk.CTkFrame) -> None:
        """Create status bar"""
        try:
            # Create status bar frame
            status_frame = ctk.CTkFrame(parent)
            status_frame.pack(fill="x", side="bottom", padx=5, pady=5)
            
            # Status message
            self.status_label = ctk.CTkLabel(
                status_frame,
                text="Ready",
                font=("Arial", 12)
            )
            self.status_label.pack(side="left", padx=5)
            
            # Version info
            version_label = ctk.CTkLabel(
                status_frame,
                text=f"v{APP_VERSION}",
                font=("Arial", 12)
            )
            version_label.pack(side="right", padx=5)
            
        except Exception as e:
            logging.error(f"Error creating status bar: {str(e)}")
            raise
    
    def show_splash_screen(self) -> None:
        """Show splash screen"""
        try:
            # Create splash screen window
            splash = ctk.CTkToplevel(self.root)
            splash.title("")
            splash.geometry("400x200")
            splash.overrideredirect(True)
            
            # Center splash screen
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width - 400) // 2
            y = (screen_height - 200) // 2
            splash.geometry(f"+{x}+{y}")
            
            # Add content
            ctk.CTkLabel(
                splash,
                text=APP_NAME,
                font=("Arial", 24, "bold")
            ).pack(pady=20)
            
            ctk.CTkLabel(
                splash,
                text=f"Version {APP_VERSION}",
                font=("Arial", 14)
            ).pack()
            
            # Progress bar
            progress = ctk.CTkProgressBar(splash)
            progress.pack(pady=20, padx=40, fill="x")
            progress.set(0)
            
            # Schedule splash screen close
            self.root.after(2000, lambda: self.close_splash_screen(splash))
            
        except Exception as e:
            logging.error(f"Error showing splash screen: {str(e)}")
            # Continue without splash screen
            self.root.deiconify()
    
    def close_splash_screen(self, splash: ctk.CTkToplevel) -> None:
        """Close splash screen"""
        try:
            splash.destroy()
            self.root.deiconify()
            
        except Exception as e:
            logging.error(f"Error closing splash screen: {str(e)}")
            self.root.deiconify()
    
    def show_error_and_exit(self, message: str) -> None:
        """Show error message and exit application"""
        try:
            # Log error
            logging.error(message)
            
            # Show error dialog
            if hasattr(self, 'managers') and 'dialog' in self.managers:
                self.managers['dialog'].show_message(
                    "Error",
                    message,
                    "error"
                )
            else:
                # Fallback to basic message box
                from tkinter import messagebox
                messagebox.showerror("Error", message)
            
            # Exit application
            sys.exit(1)
            
        except Exception as e:
            logging.error(f"Error showing error message: {str(e)}")
            sys.exit(1)
    
    def run(self) -> None:
        """Run the application"""
        try:
            # Set up application
            self.setup()
            
            # Start main loop
            self.root.mainloop()
            
        except Exception as e:
            logging.error(f"Error running application: {str(e)}")
            self.show_error_and_exit("Application error occurred")

def main():
    """Main entry point"""
    try:
        # Create and run application
        app = Storm911App()
        app.run()
        
    except Exception as e:
        logging.error(f"Application failed to start: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
