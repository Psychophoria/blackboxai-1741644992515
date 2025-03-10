"""
Caller Information Panel for Storm911
Handles caller data entry and display
"""

import tkinter as tk
import customtkinter as ctk
from typing import Dict, Any
import logging

class CallerInfoPanel:
    def __init__(self, root: ctk.CTk, managers: Dict[str, Any], handlers: Dict[str, Any]):
        """Initialize Caller Info Panel"""
        self.root = root
        self.managers = managers
        self.handlers = handlers
        
        # Initialize variables
        self.variables = {}
        
        # Initialize UI elements
        self.frame = None
        self.search_frame = None
        self.customer_frame = None
        self.roofing_frame = None
        self.insurance_frame = None
        self.progress_frame = None
    
    def create_panel(self, parent: ctk.CTkFrame) -> ctk.CTkFrame:
        """Create caller information panel"""
        # Create main frame
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Panel title
        ctk.CTkLabel(
            self.frame,
            text="CALLER DATA & INFO",
            font=("Arial", 16, "bold")
        ).pack(fill="x", padx=5, pady=5)
        
        # Create sections
        self._create_search_section()
        self._create_customer_section()
        self._create_roofing_section()
        self._create_insurance_section()
        self._create_progress_section()
        
        return self.frame
    
    def _create_search_section(self) -> None:
        """Create phone search section"""
        self.search_frame = ctk.CTkFrame(self.frame)
        self.search_frame.pack(fill="x", padx=5, pady=5)
        
        # Phone entry
        self.variables['phone'] = tk.StringVar()
        phone_entry = ctk.CTkEntry(
            self.search_frame,
            textvariable=self.variables['phone'],
            placeholder_text="Enter phone number"
        )
        phone_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Search button
        search_button = ctk.CTkButton(
            self.search_frame,
            text="Search",
            command=self._handle_search
        )
        search_button.pack(side="right", padx=5)
    
    def _create_customer_section(self) -> None:
        """Create customer information section"""
        self.customer_frame = ctk.CTkFrame(self.frame)
        self.customer_frame.pack(fill="x", padx=5, pady=5)
        
        # Section title
        ctk.CTkLabel(
            self.customer_frame,
            text="Customer Information",
            font=("Arial", 14, "bold")
        ).pack(fill="x", padx=5, pady=5)
        
        # Customer fields
        fields = [
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Address:", "address"),
            ("City:", "city"),
            ("State:", "state"),
            ("ZIP:", "zip"),
            ("Email:", "email")
        ]
        
        for label_text, field_name in fields:
            self._create_field(self.customer_frame, label_text, field_name)
    
    def _create_roofing_section(self) -> None:
        """Create roofing information section"""
        self.roofing_frame = ctk.CTkFrame(self.frame)
        self.roofing_frame.pack(fill="x", padx=5, pady=5)
        
        # Section title
        ctk.CTkLabel(
            self.roofing_frame,
            text="Roofing Information",
            font=("Arial", 14, "bold")
        ).pack(fill="x", padx=5, pady=5)
        
        # Roofing fields
        self._create_dropdown(
            self.roofing_frame,
            "Stories:",
            "stories",
            ["1", "1.5", "2", "2.5", "3+"]
        )
        
        self._create_dropdown(
            self.roofing_frame,
            "Roof Age:",
            "roof_age",
            ["0-5", "6-10", "11-15", "16-20", "20+"]
        )
        
        self._create_dropdown(
            self.roofing_frame,
            "Roof Type:",
            "roof_type",
            ["Asphalt", "Metal", "Tile", "Wood", "Other"]
        )
    
    def _create_insurance_section(self) -> None:
        """Create insurance information section"""
        self.insurance_frame = ctk.CTkFrame(self.frame)
        self.insurance_frame.pack(fill="x", padx=5, pady=5)
        
        # Section title
        ctk.CTkLabel(
            self.insurance_frame,
            text="Insurance & Appointment",
            font=("Arial", 14, "bold")
        ).pack(fill="x", padx=5, pady=5)
        
        # Insurance checkbox and company
        insurance_row = ctk.CTkFrame(self.insurance_frame)
        insurance_row.pack(fill="x", padx=5, pady=2)
        
        self.variables['has_insurance'] = tk.BooleanVar()
        ctk.CTkCheckBox(
            insurance_row,
            text="Has Insurance",
            variable=self.variables['has_insurance']
        ).pack(side="left", padx=5)
        
        self.variables['insurance_company'] = tk.StringVar()
        ctk.CTkEntry(
            insurance_row,
            textvariable=self.variables['insurance_company'],
            placeholder_text="Insurance Company"
        ).pack(side="right", fill="x", expand=True, padx=5)
        
        # Appointment date and time
        appointment_row = ctk.CTkFrame(self.insurance_frame)
        appointment_row.pack(fill="x", padx=5, pady=2)
        
        self.variables['appointment_date'] = tk.StringVar()
        ctk.CTkEntry(
            appointment_row,
            textvariable=self.variables['appointment_date'],
            placeholder_text="Date (MM/DD/YYYY)"
        ).pack(side="left", fill="x", expand=True, padx=5)
        
        self.variables['appointment_time'] = tk.StringVar()
        ctk.CTkOptionMenu(
            appointment_row,
            variable=self.variables['appointment_time'],
            values=["9:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00"]
        ).pack(side="right", padx=5)
    
    def _create_progress_section(self) -> None:
        """Create progress section"""
        self.progress_frame = ctk.CTkFrame(self.frame)
        self.progress_frame.pack(fill="x", padx=5, pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(fill="x", padx=5, pady=5)
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="0% Complete"
        )
        self.progress_label.pack(pady=2)
    
    def _create_field(
        self,
        parent: ctk.CTkFrame,
        label_text: str,
        field_name: str
    ) -> None:
        """Create labeled field"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", padx=5, pady=2)
        
        ctk.CTkLabel(
            frame,
            text=label_text
        ).pack(side="left", padx=5)
        
        self.variables[field_name] = tk.StringVar()
        ctk.CTkEntry(
            frame,
            textvariable=self.variables[field_name]
        ).pack(side="right", fill="x", expand=True, padx=5)
    
    def _create_dropdown(
        self,
        parent: ctk.CTkFrame,
        label_text: str,
        field_name: str,
        options: list
    ) -> None:
        """Create labeled dropdown"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", padx=5, pady=2)
        
        ctk.CTkLabel(
            frame,
            text=label_text
        ).pack(side="left", padx=5)
        
        self.variables[field_name] = tk.StringVar()
        ctk.CTkOptionMenu(
            frame,
            variable=self.variables[field_name],
            values=options
        ).pack(side="right", fill="x", expand=True, padx=5)
    
    def _handle_search(self) -> None:
        """Handle phone search"""
        try:
            phone = self.variables['phone'].get()
            
            if not phone:
                self.managers['dialog'].show_message(
                    "Error",
                    "Please enter a phone number",
                    "error"
                )
                return
            
            # Search for lead
            success, result = self.handlers['api'].search_lead(phone)
            
            if success:
                self._populate_fields(result)
                self.update_progress()
            else:
                self.managers['dialog'].show_message(
                    "Error",
                    result,
                    "error"
                )
            
        except Exception as e:
            logging.error(f"Error searching phone number: {str(e)}")
            self.managers['dialog'].show_message(
                "Error",
                "Failed to search phone number",
                "error"
            )
    
    def _populate_fields(self, data: Dict) -> None:
        """Populate form fields with data"""
        for field, value in data.items():
            if field in self.variables:
                self.variables[field].set(value)
    
    def get_field_values(self) -> Dict:
        """Get all field values"""
        return {
            field: var.get()
            for field, var in self.variables.items()
        }
    
    def clear_fields(self) -> None:
        """Clear all fields"""
        for var in self.variables.values():
            if isinstance(var, tk.BooleanVar):
                var.set(False)
            else:
                var.set("")
        
        self.update_progress()
    
    def update_progress(self) -> None:
        """Update progress bar"""
        # Count filled fields
        filled = sum(
            1 for var in self.variables.values()
            if var.get()
        )
        
        # Calculate progress
        progress = filled / len(self.variables)
        
        # Update progress bar and label
        self.progress_bar.set(progress)
        self.progress_label.configure(
            text=f"{int(progress * 100)}% Complete"
        )
    
    def validate_fields(self) -> bool:
        """Validate required fields"""
        required_fields = [
            'first_name',
            'last_name',
            'address',
            'city',
            'state',
            'zip',
            'phone'
        ]
        
        missing = [
            field for field in required_fields
            if not self.variables[field].get()
        ]
        
        if missing:
            self.managers['dialog'].show_message(
                "Error",
                f"Please fill in required fields: {', '.join(missing)}",
                "error"
            )
            return False
        
        return True
