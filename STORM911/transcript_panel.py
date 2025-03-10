"""
Transcript Panel for Storm911
Handles transcript display and navigation
"""

import customtkinter as ctk
from typing import Dict, Any
from transcript_content import TRANSCRIPT_PAGES

class TranscriptPanel:
    def __init__(self, root: ctk.CTk, managers: Dict[str, Any], handlers: Dict[str, Any]):
        """Initialize Transcript Panel"""
        self.root = root
        self.managers = managers
        self.handlers = handlers
        
        # Initialize state
        self.current_page = 0
        self.total_pages = len(TRANSCRIPT_PAGES)
        
        # Create UI elements
        self.frame = None
        self.nav_frame = None
        self.content_frame = None
        self.progress_frame = None
        self.prev_button = None
        self.next_button = None
        self.page_counter = None
        self.transcript_text = None
        self.progress_bar = None
        self.progress_label = None
    
    def create_panel(self, parent: ctk.CTkFrame) -> ctk.CTkFrame:
        """Create transcript panel"""
        # Create main frame
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Panel title
        ctk.CTkLabel(
            self.frame,
            text="TRANSCRIPT",
            font=("Arial", 16, "bold")
        ).pack(fill="x", padx=5, pady=5)
        
        # Create components
        self._create_navigation()
        self._create_content()
        self._create_progress()
        
        # Show initial page
        self.show_page(0)
        
        return self.frame
    
    def _create_navigation(self) -> None:
        """Create navigation buttons"""
        self.nav_frame = ctk.CTkFrame(self.frame)
        self.nav_frame.pack(fill="x", padx=5, pady=5)
        
        # Previous button
        self.prev_button = ctk.CTkButton(
            self.nav_frame,
            text="← PREVIOUS",
            command=self.prev_page,
            state="disabled"
        )
        self.prev_button.pack(side="left", padx=5)
        
        # Page counter
        self.page_counter = ctk.CTkLabel(
            self.nav_frame,
            text=f"Page {self.current_page}/{self.total_pages-1}",
            font=("Arial", 12)
        )
        self.page_counter.pack(side="left", padx=20)
        
        # Next button
        self.next_button = ctk.CTkButton(
            self.nav_frame,
            text="NEXT →",
            command=self.next_page
        )
        self.next_button.pack(side="right", padx=5)
    
    def _create_content(self) -> None:
        """Create content area"""
        self.content_frame = ctk.CTkFrame(self.frame)
        self.content_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Transcript text widget
        self.transcript_text = ctk.CTkTextbox(
            self.content_frame,
            wrap="word",
            font=("Arial", 14)
        )
        self.transcript_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.transcript_text.configure(state="disabled")
    
    def _create_progress(self) -> None:
        """Create progress bar"""
        self.progress_frame = ctk.CTkFrame(self.frame)
        self.progress_frame.pack(fill="x", padx=5, pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(fill="x", padx=5, pady=5)
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="0% Complete",
            font=("Arial", 12)
        )
        self.progress_label.pack(pady=2)
    
    def show_page(self, page_number: int) -> None:
        """Display the specified page"""
        if page_number in TRANSCRIPT_PAGES:
            # Update current page
            self.current_page = page_number
            
            # Update page counter
            self.page_counter.configure(
                text=f"Page {page_number}/{self.total_pages-1}"
            )
            
            # Enable/disable navigation buttons
            self.prev_button.configure(
                state="normal" if page_number > 0 else "disabled"
            )
            self.next_button.configure(
                state="normal" if page_number < self.total_pages-1 else "disabled"
            )
            
            # Update content
            self.transcript_text.configure(state="normal")
            self.transcript_text.delete("1.0", "end")
            
            page_content = TRANSCRIPT_PAGES[page_number]
            content = f"{page_content['title']}\n\n{page_content['content']}"
            
            if 'key_points' in page_content:
                content += "\n\nKey Points:\n"
                for point in page_content['key_points']:
                    content += f"• {point}\n"
            
            self.transcript_text.insert("1.0", content)
            self.transcript_text.configure(state="disabled")
            
            # Update progress
            progress = page_number / (self.total_pages - 1)
            self.progress_bar.set(progress)
            self.progress_label.configure(
                text=f"{int(progress * 100)}% Complete"
            )
            
            # Log page change
            self.managers['event'].log_event(
                'user',
                'page_change',
                {'page': page_number}
            )
    
    def next_page(self) -> None:
        """Navigate to next page"""
        if self.current_page < self.total_pages - 1:
            self.show_page(self.current_page + 1)
    
    def prev_page(self) -> None:
        """Navigate to previous page"""
        if self.current_page > 0:
            self.show_page(self.current_page - 1)
    
    def reset(self) -> None:
        """Reset transcript to start"""
        self.show_page(0)
    
    def get_current_page(self) -> Dict:
        """Get current page content"""
        return TRANSCRIPT_PAGES.get(self.current_page, {})
    
    def get_progress(self) -> float:
        """Get current progress percentage"""
        return self.current_page / (self.total_pages - 1)
    
    def is_complete(self) -> bool:
        """Check if transcript is complete"""
        return self.current_page == self.total_pages - 1
    
    def handle_hotkey(self, key: str) -> None:
        """Handle hotkey press"""
        if key == "next" and self.next_button.cget("state") == "normal":
            self.next_page()
        elif key == "prev" and self.prev_button.cget("state") == "normal":
            self.prev_page()
