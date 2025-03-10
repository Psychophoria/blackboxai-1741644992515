"""
UI Panels for Storm911
Contains panel creation and management functionality
"""

import customtkinter as ctk
from typing import Dict, Any

class UIPanels:
    def __init__(self, root: ctk.CTk, managers: Dict[str, Any], handlers: Dict[str, Any]):
        """Initialize UI Panels"""
        self.root = root
        self.managers = managers
        self.handlers = handlers
    
    def create_caller_info_panel(self, parent: ctk.CTkFrame) -> None:
        """Create caller information panel"""
        # Create panel
        caller_frame = ctk.CTkFrame(parent)
        caller_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Panel title
        ctk.CTkLabel(
            caller_frame,
            text="CALLER DATA & INFO",
            font=("Arial", 16, "bold")
        ).pack(fill="x", padx=5, pady=5)
        
        # Phone search section
        self._create_phone_search_section(caller_frame)
        
        # Customer info section
        self._create_customer_info_section(caller_frame)
        
        # Roofing info section
        self._create_roofing_info_section(caller_frame)
        
        # Insurance/Appointment section
        self._create_insurance_appointment_section(caller_frame)
        
        # Progress bar
        self._create_progress_bar(caller_frame)
        
        return caller_frame
    
    def create_transcript_panel(self, parent: ctk.CTkFrame) -> None:
        """Create transcript panel"""
        # Create panel
        transcript_frame = ctk.CTkFrame(parent)
        transcript_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Panel title
        ctk.CTkLabel(
            transcript_frame,
            text="TRANSCRIPT",
            font=("Arial", 16, "bold")
        ).pack(fill="x", padx=5, pady=5)
        
        # Navigation buttons
        self._create_transcript_navigation(transcript_frame)
        
        # Content area
        self._create_transcript_content(transcript_frame)
        
        # Progress bar
        self._create_transcript_progress(transcript_frame)
        
        return transcript_frame
    
    def create_objections_panel(self, parent: ctk.CTkFrame) -> None:
        """Create objections panel"""
        # Create panel
        objections_frame = ctk.CTkFrame(parent)
        objections_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Panel title
        ctk.CTkLabel(
            objections_frame,
            text="OBJECTIONS",
            font=("Arial", 16, "bold")
        ).pack(fill="x", padx=5, pady=5)
        
        # Group 1 objections
        self._create_group1_objections(objections_frame)
        
        # Group 2 objections
        self._create_group2_objections(objections_frame)
        
        return objections_frame
    
    def _create_phone_search_section(self, parent: ctk.CTkFrame) -> None:
        """Create phone search section"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", padx=5, pady=5)
        
        # Phone entry
        phone_var = tk.StringVar()
        phone_entry = ctk.CTkEntry(
            frame,
            textvariable=phone_var,
            placeholder_text="Enter phone number"
        )
        phone_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Search button
        search_button = ctk.CTkButton(
            frame,
            text="Search",
            command=lambda: self._handle_phone_search(phone_var.get())
        )
        search_button.pack(side="right", padx=5)
    
    def _create_customer_info_section(self, parent: ctk.CTkFrame) -> None:
        """Create customer information section"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", padx=5, pady=5)
        
        # Section title
        ctk.CTkLabel(
            frame,
            text="Customer Information",
            font=("Arial", 14, "bold")
        ).pack(fill="x", padx=5, pady=5)
        
        # Customer info fields
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
            field_frame = ctk.CTkFrame(frame)
            field_frame.pack(fill="x", padx=5, pady=2)
            
            ctk.CTkLabel(
                field_frame,
                text=label_text
            ).pack(side="left", padx=5)
            
            var = tk.StringVar()
            entry = ctk.CTkEntry(field_frame, textvariable=var)
            entry.pack(side="right", fill="x", expand=True, padx=5)
            
            # Store reference
            setattr(self, f"{field_name}_var", var)
    
    def _create_roofing_info_section(self, parent: ctk.CTkFrame) -> None:
        """Create roofing information section"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", padx=5, pady=5)
        
        # Section title
        ctk.CTkLabel(
            frame,
            text="Roofing Information",
            font=("Arial", 14, "bold")
        ).pack(fill="x", padx=5, pady=5)
        
        # Roofing info fields
        fields = [
            ("Stories:", "stories", ["1", "1.5", "2", "2.5", "3+"]),
            ("Roof Age:", "roof_age", ["0-5", "6-10", "11-15", "16-20", "20+"]),
            ("Roof Type:", "roof_type", ["Asphalt", "Metal", "Tile", "Wood", "Other"])
        ]
        
        for label_text, field_name, options in fields:
            field_frame = ctk.CTkFrame(frame)
            field_frame.pack(fill="x", padx=5, pady=2)
            
            ctk.CTkLabel(
                field_frame,
                text=label_text
            ).pack(side="left", padx=5)
            
            var = tk.StringVar()
            dropdown = ctk.CTkOptionMenu(
                field_frame,
                variable=var,
                values=options
            )
            dropdown.pack(side="right", fill="x", expand=True, padx=5)
            
            # Store reference
            setattr(self, f"{field_name}_var", var)
    
    def _create_insurance_appointment_section(self, parent: ctk.CTkFrame) -> None:
        """Create insurance and appointment section"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", padx=5, pady=5)
        
        # Section title
        ctk.CTkLabel(
            frame,
            text="Insurance & Appointment",
            font=("Arial", 14, "bold")
        ).pack(fill="x", padx=5, pady=5)
        
        # Insurance info
        insurance_frame = ctk.CTkFrame(frame)
        insurance_frame.pack(fill="x", padx=5, pady=2)
        
        self.has_insurance_var = tk.BooleanVar()
        ctk.CTkCheckBox(
            insurance_frame,
            text="Has Insurance",
            variable=self.has_insurance_var
        ).pack(side="left", padx=5)
        
        self.insurance_company_var = tk.StringVar()
        ctk.CTkEntry(
            insurance_frame,
            textvariable=self.insurance_company_var,
            placeholder_text="Insurance Company"
        ).pack(side="right", fill="x", expand=True, padx=5)
        
        # Appointment info
        appointment_frame = ctk.CTkFrame(frame)
        appointment_frame.pack(fill="x", padx=5, pady=2)
        
        self.appointment_date_var = tk.StringVar()
        ctk.CTkEntry(
            appointment_frame,
            textvariable=self.appointment_date_var,
            placeholder_text="Date"
        ).pack(side="left", fill="x", expand=True, padx=5)
        
        self.appointment_time_var = tk.StringVar()
        ctk.CTkOptionMenu(
            appointment_frame,
            variable=self.appointment_time_var,
            values=["9:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00"]
        ).pack(side="right", padx=5)
    
    def _create_progress_bar(self, parent: ctk.CTkFrame) -> None:
        """Create progress bar"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", padx=5, pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(frame)
        self.progress_bar.pack(fill="x", padx=5, pady=5)
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(
            frame,
            text="0% Complete"
        )
        self.progress_label.pack(pady=2)
    
    def _handle_phone_search(self, phone: str) -> None:
        """Handle phone number search"""
        try:
            # Validate phone number
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
                # Populate fields with result
                self._populate_fields(result)
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
        # Customer info
        self.first_name_var.set(data.get('first_name', ''))
        self.last_name_var.set(data.get('last_name', ''))
        self.address_var.set(data.get('address', ''))
        self.city_var.set(data.get('city', ''))
        self.state_var.set(data.get('state', ''))
        self.zip_var.set(data.get('zip', ''))
        self.email_var.set(data.get('email', ''))
        
        # Roofing info
        self.stories_var.set(data.get('stories', ''))
        self.roof_age_var.set(data.get('roof_age', ''))
        self.roof_type_var.set(data.get('roof_type', ''))
        
        # Insurance info
        self.has_insurance_var.set(data.get('has_insurance', False))
        self.insurance_company_var.set(data.get('insurance_company', ''))
        
        # Appointment info
        self.appointment_date_var.set(data.get('appointment_date', ''))
        self.appointment_time_var.set(data.get('appointment_time', ''))
