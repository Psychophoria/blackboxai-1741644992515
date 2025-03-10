"""
Transcript Content Manager for Storm911
Contains all script pages and content
"""

TRANSCRIPT_PAGES = {
    0: {
        "title": "START Screen",
        "content": """Welcome to the Storm911 21 Second Pitch

This script is designed to help you effectively communicate with potential clients about our roofing inspection services.

Remember:
- Stay confident and professional
- Listen actively to the customer
- Address objections promptly
- Focus on scheduling the appointment

Click 'NEXT' to begin the pitch."""
    },
    
    1: {
        "title": "THE HOOK - 8.25 SECONDS",
        "content": """Hi, my name is [Your Name] with NIRC. We're the National Insurance Restoration Contractors.

We're in your neighborhood today because we've been helping a lot of your neighbors with their roofs due to all the storm damage in your area.

We're offering FREE roof inspections to help homeowners like yourself identify any storm damage that may have occurred.

[Pause for response]""",
        "key_points": [
            "Introduce yourself and company",
            "Mention local presence",
            "Emphasize FREE service",
            "Reference storm damage"
        ]
    },
    
    2: {
        "title": "INTRODUCTION AND APPOINTMENT SETTING",
        "content": """We're working with [Insurance Company Name] and other insurance companies to help homeowners identify storm damage and file insurance claims if needed.

We'd like to schedule a FREE inspection of your roof. It only takes about 30 minutes, and we can do it while you're at work or home.

Would morning or afternoon work better for you?

[Wait for response and be ready to handle objections]""",
        "key_points": [
            "Mention insurance companies",
            "Emphasize convenience",
            "Short time commitment",
            "Flexible scheduling"
        ]
    },
    
    3: {
        "title": "THE INSPECTION PROCESS",
        "content": """Great! Let me explain what we'll do during the inspection.

Our certified inspector will:
1. Thoroughly examine your roof
2. Document any damage with photos
3. Check for signs of water intrusion
4. Assess the overall condition
5. Provide a detailed report

This is completely FREE and there's no obligation.""",
        "key_points": [
            "Explain process steps",
            "Mention certification",
            "Documentation provided",
            "No obligation"
        ]
    },
    
    4: {
        "title": "THE INSPECTION PROCESS CONTINUED",
        "content": """If we find storm damage, we'll:
1. Show you exactly what we found
2. Take detailed photos
3. Help you understand your options
4. Assist with insurance claims if needed

If we don't find any damage, you'll have peace of mind knowing your roof is in good condition.

Does that sound reasonable?""",
        "key_points": [
            "Explain findings process",
            "Insurance assistance",
            "Win-win situation",
            "Seek agreement"
        ]
    },
    
    5: {
        "title": "HOME STORY QUESTION",
        "content": """Before we schedule the inspection, could you tell me how long you've lived in your home?

[Wait for response]

And have you noticed any issues with your roof, like missing shingles or water spots on the ceiling?

[Listen carefully to their response and show empathy if they mention problems]""",
        "key_points": [
            "Build rapport",
            "Show interest",
            "Identify concerns",
            "Active listening"
        ]
    },
    
    6: {
        "title": "INSPECTION PROCESS CONTINUED",
        "content": """Thank you for sharing that. It's important to catch any issues early before they become major problems.

Our inspection will give you a complete picture of your roof's condition. We'll check:
- All slopes and valleys
- Flashing and vents
- Gutters and downspouts
- Attic ventilation
- Signs of water intrusion""",
        "key_points": [
            "Comprehensive inspection",
            "Professional expertise",
            "Preventive approach",
            "Detailed checklist"
        ]
    },
    
    7: {
        "title": "ROOFING TYPE QUESTION",
        "content": """What type of roofing material do you currently have?
□ Asphalt Shingles
□ Metal
□ Tile
□ Wood Shake
□ Other

[Note their response and adjust inspection details accordingly]""",
        "key_points": [
            "Identify roof type",
            "Show expertise",
            "Customize approach",
            "Build credibility"
        ]
    },
    
    8: {
        "title": "INSPECTION PROCESS CONTINUED",
        "content": """Perfect. We have extensive experience with [their roof type] roofs.

During the inspection, we'll pay special attention to:
[Customize based on roof type]

We'll also check for any manufacturer defects or installation issues that might be covered under warranty.""",
        "key_points": [
            "Show specific expertise",
            "Mention warranties",
            "Build confidence",
            "Demonstrate value"
        ]
    },
    
    9: {
        "title": "CONTINUED INSPECTION QUESTIONS",
        "content": """Just a few more questions to help us prepare for the inspection:

1. How many stories is your home?
2. Are there any known leaks or previous repairs?
3. Have you filed any insurance claims for roof damage before?

[Document their responses]""",
        "key_points": [
            "Gather information",
            "Show thoroughness",
            "Demonstrate professionalism",
            "Build rapport"
        ]
    },
    
    10: {
        "title": "QUESTION: A LOT OF YOUR NEIGHBORS",
        "content": """As I mentioned, we've been helping many of your neighbors with storm damage inspections.

In fact, we've found significant damage on several homes in your area that qualified for insurance coverage.

Would you like to know if your roof has similar damage?

[Wait for response]""",
        "key_points": [
            "Social proof",
            "Create urgency",
            "Insurance mention",
            "Encourage action"
        ]
    },
    
    11: {
        "title": "INSPECTION PROCESS CONTINUED",
        "content": """Great! Let me explain what happens after we find damage:

1. We document everything thoroughly
2. We review the findings with you
3. We explain your options clearly
4. We help with insurance if needed
5. We provide written documentation

There's never any pressure or obligation.""",
        "key_points": [
            "Clear process",
            "No pressure",
            "Professional support",
            "Documentation"
        ]
    },
    
    12: {
        "title": "IF THEY FIND NO DAMAGES",
        "content": """If we don't find any damage, we'll:

1. Give you a clean bill of health
2. Provide preventive maintenance tips
3. Document the inspection
4. Give you our professional opinion

Either way, you'll know exactly what condition your roof is in.""",
        "key_points": [
            "Win-win situation",
            "Professional service",
            "Added value",
            "Peace of mind"
        ]
    },
    
    13: {
        "title": "NIRC REPORT",
        "content": """After the inspection, you'll receive our detailed NIRC report, which includes:

- Photos of your roof
- Detailed findings
- Professional recommendations
- Documentation for insurance
- Maintenance suggestions

This report is yours to keep, whether you need repairs or not.""",
        "key_points": [
            "Professional documentation",
            "Valuable information",
            "Insurance ready",
            "No obligation"
        ]
    },
    
    14: {
        "title": "CONFIRM EMAIL",
        "content": """To make sure you receive your inspection report promptly, could you confirm your email address?

[Record email address]

We'll send you:
1. Appointment confirmation
2. Inspector's contact information
3. What to expect
4. Inspection report (after completion)""",
        "key_points": [
            "Get contact info",
            "Professional follow-up",
            "Clear communication",
            "Set expectations"
        ]
    },
    
    15: {
        "title": "ROOF LEAK AND HOMEOWNER CONFIRMATION",
        "content": """Just to confirm:
1. Have you noticed any leaks or water spots?
2. Are you the homeowner or decision-maker?
3. Do you have homeowner's insurance?

[Document responses and address any concerns]""",
        "key_points": [
            "Verify authority",
            "Insurance status",
            "Current issues",
            "Decision maker"
        ]
    },
    
    16: {
        "title": "CLOSING THE APPOINTMENT – NAME CONFIRMATION",
        "content": """Great! Let me confirm your name for our records.

Could you spell your first and last name for me?

[Record name carefully]

And is this the name on the homeowner's insurance policy?""",
        "key_points": [
            "Accurate records",
            "Professional approach",
            "Insurance verification",
            "Detail oriented"
        ]
    },
    
    17: {
        "title": "CLOSING THE APPOINTMENT – ADDRESS CONFIRMATION",
        "content": """Now, let me verify your address:

Street Address: [Record]
City: [Record]
State: [Record]
ZIP Code: [Record]

Is this where the inspection will take place?""",
        "key_points": [
            "Verify location",
            "Accurate records",
            "Clear communication",
            "Confirm details"
        ]
    },
    
    18: {
        "title": "CLOSING THE APPOINTMENT – CONTRACT & OWNER",
        "content": """Just to confirm:
1. You are the homeowner/decision-maker
2. You don't currently have a contract with another roofing company
3. You understand this is a FREE, no-obligation inspection

Is that all correct?""",
        "key_points": [
            "Final verification",
            "Clear understanding",
            "No obligations",
            "Authority confirmation"
        ]
    },
    
    19: {
        "title": "CLOSING THE APPOINTMENT – NO OTHER CONTRACT",
        "content": """And just to verify:
You don't have any current contracts or agreements with other roofing companies, correct?

This helps us avoid any conflicts and ensures we can provide you with the best possible service.""",
        "key_points": [
            "Avoid conflicts",
            "Professional service",
            "Clear understanding",
            "Legal compliance"
        ]
    },
    
    20: {
        "title": "CLOSING THE APPOINTMENT – SCHEDULE CONFIRMATION",
        "content": """Let me confirm your appointment details:

Date: [Record]
Time: [Record]
Address: [Record]
Phone: [Record]
Email: [Record]

Does this all look correct?""",
        "key_points": [
            "Verify details",
            "Clear communication",
            "Professional approach",
            "Confirm schedule"
        ]
    },
    
    21: {
        "title": "FINAL CLOSING AND REFERRALS",
        "content": """Excellent! You're all set for [Day] at [Time].

One last thing - if you know anyone else who might benefit from a FREE roof inspection, please feel free to refer them to us.

We appreciate referrals and treat all our customers with the same professional service.""",
        "key_points": [
            "Confirm appointment",
            "Ask for referrals",
            "Professional service",
            "Appreciation"
        ]
    },
    
    22: {
        "title": "ASK FOR THE SALE DO NOT WIMP OUT",
        "content": """Great! We look forward to meeting with you and helping you protect your home.

Before we wrap up, do you have any other questions for me?

Thank you for your time, and we'll see you [Appointment Date and Time].

[End call professionally]""",
        "key_points": [
            "Professional closing",
            "Address questions",
            "Confirm details",
            "Show appreciation"
        ]
    }
}
