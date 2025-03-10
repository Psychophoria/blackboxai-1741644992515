"""
Application Initializer for Storm911
Handles application startup, initialization, and dependency management
"""

import os
import logging
from typing import Optional, Dict, Any
import customtkinter as ctk

from config import APP_NAME, APP_VERSION, WINDOW_SIZE
from theme_manager import ThemeManager
from state_manager import StateManager
from settings_manager import SettingsManager
from event_logger import EventLogger
from hotkey_manager import HotkeyManager
from dialog_manager import DialogManager
from api_handler import APIHandler
from pdf_handler import PDFHandler
from email_handler import EmailHandler
from disposition_handler import DispositionHandler
from menu_manager import MenuManager

class AppInitializer:
    def __init__(self):
        """Initialize application components"""
        self.root: Optional[ctk.CTk] = None
        self.managers: Dict[str, Any] = {}
        self.handlers: Dict[str, Any] = {}
        
        # Set up logging first
        self._setup_logging()
        
        logging.info(f"Initializing {APP_NAME} v{APP_VERSION}")
    
    def _setup_logging(self) -> None:
        """Set up application logging"""
        try:
            # Ensure logs directory exists
            os.makedirs('logs', exist_ok=True)
            
            # Configure logging
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler('logs/storm911.log'),
                    logging.StreamHandler()
                ]
            )
        except Exception as e:
            print(f"Error setting up logging: {str(e)}")
            raise
    
    def initialize_app(self) -> ctk.CTk:
        """Initialize the application"""
        try:
            # Create main window
            self.root = ctk.CTk()
            self.root.title(f"{APP_NAME} v{APP_VERSION}")
            self.root.geometry(WINDOW_SIZE)
            
            # Initialize managers
            self._initialize_managers()
            
            # Initialize handlers
            self._initialize_handlers()
            
            # Set up application theme
            self._setup_theme()
            
            # Load settings
            self._load_settings()
            
            # Set up event bindings
            self._setup_event_bindings()
            
            # Initialize UI components
            self._initialize_ui()
            
            logging.info("Application initialization completed successfully")
            return self.root
            
        except Exception as e:
            logging.error(f"Error initializing application: {str(e)}")
            raise
    
    def _initialize_managers(self) -> None:
        """Initialize application managers"""
        try:
            # Create managers
            self.managers['theme'] = ThemeManager()
            self.managers['state'] = StateManager()
            self.managers['settings'] = SettingsManager()
            self.managers['event'] = EventLogger()
            self.managers['hotkey'] = HotkeyManager(self.root)
            self.managers['dialog'] = DialogManager(
                self.root,
                self.managers['theme']
            )
            self.managers['menu'] = MenuManager(
                self.root,
                self.managers,
                self.handlers
            )
            
            logging.info("Application managers initialized successfully")
            
        except Exception as e:
            logging.error(f"Error initializing managers: {str(e)}")
            raise
    
    def _initialize_handlers(self) -> None:
        """Initialize application handlers"""
        try:
            # Create handlers
            self.handlers['api'] = APIHandler()
            self.handlers['pdf'] = PDFHandler()
            self.handlers['email'] = EmailHandler()
            self.handlers['disposition'] = DispositionHandler(
                self.handlers['pdf'],
                self.handlers['email'],
                self.handlers['api']
            )
            
            logging.info("Application handlers initialized successfully")
            
        except Exception as e:
            logging.error(f"Error initializing handlers: {str(e)}")
            raise
    
    def _setup_theme(self) -> None:
        """Set up application theme"""
        try:
            # Get theme settings
            theme = self.managers['settings'].get_setting('appearance', 'theme')
            
            # Apply theme
            self.managers['theme'].apply_theme(theme)
            
            logging.info(f"Applied theme: {theme}")
            
        except Exception as e:
            logging.error(f"Error setting up theme: {str(e)}")
            raise
    
    def _load_settings(self) -> None:
        """Load application settings"""
        try:
            # Apply settings
            self.managers['settings'].apply_settings()
            
            # Configure window size
            window_size = self.managers['settings'].get_setting(
                'appearance',
                'window_size'
            )
            if window_size:
                self.root.geometry(window_size)
            
            logging.info("Settings loaded successfully")
            
        except Exception as e:
            logging.error(f"Error loading settings: {str(e)}")
            raise
    
    def _setup_event_bindings(self) -> None:
        """Set up application event bindings"""
        try:
            # Window close handler
            self.root.protocol(
                "WM_DELETE_WINDOW",
                self._handle_window_close
            )
            
            # Set up hotkeys
            self._setup_hotkeys()
            
            logging.info("Event bindings set up successfully")
            
        except Exception as e:
            logging.error(f"Error setting up event bindings: {str(e)}")
            raise
    
    def _setup_hotkeys(self) -> None:
        """Set up application hotkeys"""
        try:
            # Only set up if enabled in settings
            if self.managers['settings'].get_setting('behavior', 'enable_hotkeys'):
                self.managers['hotkey'].setup_default_bindings({
                    # Add default hotkey callbacks here
                })
            
            logging.info("Hotkeys set up successfully")
            
        except Exception as e:
            logging.error(f"Error setting up hotkeys: {str(e)}")
            raise
    
    def _initialize_ui(self) -> None:
        """Initialize UI components"""
        try:
            # Create main container
            main_container = ctk.CTkFrame(self.root)
            main_container.pack(fill="both", expand=True)
            
            # Store reference
            self.root.main_container = main_container
            
            # Create menu
            self.managers['menu'].create_toolbar(main_container)
            
            logging.info("UI components initialized successfully")
            
        except Exception as e:
            logging.error(f"Error initializing UI: {str(e)}")
            raise
    
    def _handle_window_close(self) -> None:
        """Handle window close event"""
        try:
            # Check if confirmation is required
            if self.managers['settings'].get_setting('behavior', 'confirm_exit'):
                self.managers['dialog'].show_confirmation(
                    "Exit Application",
                    "Are you sure you want to exit?",
                    self._confirm_exit
                )
            else:
                self._confirm_exit(True)
            
        except Exception as e:
            logging.error(f"Error handling window close: {str(e)}")
            self._confirm_exit(True)
    
    def _confirm_exit(self, confirmed: bool) -> None:
        """Handle exit confirmation response"""
        if confirmed:
            try:
                # Save application state
                self.managers['state'].save_state()
                
                # Save settings
                self.managers['settings'].save_settings()
                
                # Close all dialogs
                self.managers['dialog'].close_all()
                
                # Destroy root window
                self.root.destroy()
                
                logging.info("Application shut down successfully")
                
            except Exception as e:
                logging.error(f"Error during shutdown: {str(e)}")
                self.root.destroy()
