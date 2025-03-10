"""
Objection Response Manager for Storm911
Contains all objection responses and handling strategies
"""

GROUP1_OBJECTIONS = {
    "I Don't Have Time": {
        "response": """I completely understand you're busy. That's why we make this process as convenient as possible:

• The inspection only takes 30 minutes
• We can do it while you're at work
• We just need your permission to inspect
• No need to be present
• Flexible scheduling available

When would be a better time for you - morning or afternoon?""",
        "key_points": [
            "Acknowledge their time concern",
            "Emphasize convenience",
            "Flexible scheduling",
            "No presence required"
        ]
    },
    
    "I Am Not Interested": {
        "response": """I understand your hesitation. Many of your neighbors felt the same way until they learned:

• Our inspection is completely FREE
• Could save thousands in roof repairs
• No obligation whatsoever
• Helps prevent future problems
• Works with your insurance

Would you at least like to know if your roof has any damage?""",
        "key_points": [
            "Acknowledge concern",
            "Emphasize FREE service",
            "Mention cost savings",
            "No obligation"
        ]
    },
    
    "Already Had Inspection": {
        "response": """That's great that you're being proactive! May I ask:

• When was your last inspection?
• Who performed it?
• Did they provide detailed documentation?
• Did they check for storm damage?

Given the recent storms and that damage isn't always visible from the ground, would you be open to a FREE second opinion?""",
        "key_points": [
            "Acknowledge proactive approach",
            "Question previous inspection",
            "Offer second opinion",
            "Emphasize FREE service"
        ]
    },
    
    "No Damage": {
        "response": """I understand you don't see any damage, but consider this:

• Storm damage isn't always visible from the ground
• Our trained inspectors spot issues most people miss
• Early detection prevents costly repairs
• FREE inspection gives peace of mind
• No obligation if no damage found

Since it's FREE, wouldn't it be worth 30 minutes for peace of mind?""",
        "key_points": [
            "Acknowledge their perspective",
            "Expert inspection value",
            "Hidden damage possibility",
            "Peace of mind"
        ]
    },
    
    "Insurance Claim Denied": {
        "response": """I'm sorry to hear that. Often, claims are denied because:

• Damage wasn't properly documented
• Inspection wasn't thorough enough
• Wrong type of damage reported
• Incorrect documentation

We specialize in insurance claims and can:
• Provide detailed inspection
• Document everything properly
• Help with appeal process
• Work directly with insurance

When was your claim denied? We might be able to help you appeal.""",
        "key_points": [
            "Show empathy",
            "Explain common denial reasons",
            "Offer specialized help",
            "Mention appeal possibility"
        ]
    },
    
    "Selling Home": {
        "response": """This is actually perfect timing! A recent roof inspection:

• Can be a great selling point
• Gives buyers peace of mind
• Identifies issues before buyer's inspection
• Provides professional documentation
• Could increase home value

When are you planning to list the house?""",
        "key_points": [
            "Turn objection into opportunity",
            "Selling advantages",
            "Professional documentation",
            "Added value"
        ]
    },
    
    "Metal Roof": {
        "response": """Metal roofs are great, but they're not immune to damage:

• Hail can cause dents that compromise integrity
• Storm damage can affect seams and fasteners
• Wind can loosen panels
• Our inspectors are specially trained for metal roofs
• FREE inspection provides peace of mind

Would you like us to take a look?""",
        "key_points": [
            "Acknowledge roof quality",
            "Explain specific risks",
            "Demonstrate expertise",
            "Offer FREE inspection"
        ]
    },
    
    "Call Back Later": {
        "response": """I understand you'd like me to call back, but:

• We're only in your area for a limited time
• Our schedule fills up quickly
• FREE inspections are time-sensitive
• Weather damage can worsen over time

Instead of calling back, why don't we schedule a time that works better for you? Would morning or afternoon be better?""",
        "key_points": [
            "Create urgency",
            "Limited availability",
            "Flexible scheduling",
            "Immediate action"
        ]
    },
    
    "Don't Want To Decide Now": {
        "response": """I understand you want to think about it. Consider this:

• Storm damage can worsen over time
• The inspection is completely FREE
• No obligation to proceed
• You have nothing to lose
• Could save thousands in repairs

Since it's FREE, can we schedule a time that works for you?""",
        "key_points": [
            "Acknowledge hesitation",
            "Emphasize no risk",
            "Create urgency",
            "Offer value"
        ]
    },
    
    "No Insurance": {
        "response": """Even without insurance, it's important to know your roof's condition:

• FREE inspection gives you valuable information
• Early detection prevents costly repairs
• Documentation helps with future coverage
• We can suggest affordable solutions
• No obligation or pressure

Would you like us to take a look?""",
        "key_points": [
            "Focus on value",
            "Preventive benefits",
            "Future planning",
            "No pressure"
        ]
    },
    
    "Not The Homeowner": {
        "response": """I understand. This FREE inspection could really help the homeowner:

• Identifies potential problems early
• Prevents costly repairs
• Works with their insurance
• Professional documentation
• No obligation

Could you help me get in touch with the homeowner? When would be the best time to reach them?""",
        "key_points": [
            "Acknowledge situation",
            "Explain benefits",
            "Request referral",
            "Professional approach"
        ]
    }
}

GROUP2_OBJECTIONS = {
    "Spam Call": {
        "response": """I assure you this isn't a spam call:

• We're a legitimate roofing company
• Licensed and insured
• Local presence
• Verifiable credentials
• Check our online reviews

We're offering FREE inspections to help homeowners identify storm damage. Would you like to learn more?""",
        "key_points": [
            "Establish legitimacy",
            "Provide verification",
            "Local presence",
            "Professional service"
        ]
    },
    
    "How Got Number": {
        "response": """We work with legitimate lead sources:

• Focus on storm-affected areas
• Help homeowners prevent damage
• Fully compliant with regulations
• Remove numbers upon request
• Professional service only

Would you like to hear more about our FREE inspection service?""",
        "key_points": [
            "Professional explanation",
            "Legal compliance",
            "Customer focus",
            "Respect privacy"
        ]
    },
    
    "Who is NIRC": {
        "response": """NIRC (National Insurance Restoration Contractors):

• Network of certified contractors
• Specialize in insurance restoration
• Years of experience
• Thousands of satisfied customers
• Industry leading standards

Would you like to learn more about our services?""",
        "key_points": [
            "Company credentials",
            "Experience",
            "Specialization",
            "Professional network"
        ]
    },
    
    "Why Can't Call Back": {
        "response": """We're currently in your area offering FREE inspections:

• Limited time availability
• Schedule fills quickly
• Weather damage can worsen
• Flexible appointment times
• Convenient scheduling

Rather than calling back, why don't we find a time that works better for you? Would morning or afternoon be more convenient?""",
        "key_points": [
            "Create urgency",
            "Limited availability",
            "Flexible scheduling",
            "Immediate action"
        ]
    },
    
    "Bad Experience": {
        "response": """I'm sorry to hear about your bad experience. We're different:

• Fully licensed and insured
• Excellent reviews
• Professional standards
• Customer satisfaction guarantee
• No pressure approach

Would you give us a chance to show you how a professional roofing company should operate?""",
        "key_points": [
            "Show empathy",
            "Differentiate service",
            "Professional standards",
            "Customer focus"
        ]
    },
    
    "Nothing Is Free": {
        "response": """I understand your skepticism. Our inspection is genuinely FREE because:

• We believe in helping homeowners
• No obligation whatsoever
• We work with insurance companies
• Professional documentation provided
• Builds trust in our community

Would you like to learn more?""",
        "key_points": [
            "Address skepticism",
            "Explain business model",
            "No obligation",
            "Community focus"
        ]
    },
    
    "Which Neighbor": {
        "response": """Due to privacy concerns, we can't disclose specific names, but:

• We've helped several homes on your street
• Can provide references after inspection
• Many satisfied customers
• Growing local presence
• Professional service

Would you like to schedule a time for us to take a look at your roof?""",
        "key_points": [
            "Respect privacy",
            "Local presence",
            "Professional approach",
            "Reference availability"
        ]
    },
    
    "Has Contractor": {
        "response": """It's great that you have a contractor you trust. However:

• Our FREE inspection provides second opinion
• We specialize in storm damage
• Work directly with insurance
• No obligation
• Professional documentation

Would you be interested in our assessment?""",
        "key_points": [
            "Acknowledge relationship",
            "Offer additional value",
            "Specialization",
            "No obligation"
        ]
    },
    
    "Thirty Second": {
        "response": """I know your time is valuable. Quick overview:

• FREE roof inspection
• 30-minute process
• Insurance claim assistance
• No obligation
• Professional service

Can we schedule a time that works for you?""",
        "key_points": [
            "Respect time",
            "Key benefits",
            "Quick process",
            "Clear value"
        ]
    }
}

def get_objection_response(group: int, objection: str) -> dict:
    """Get response for specific objection"""
    if group == 1:
        return GROUP1_OBJECTIONS.get(objection, {
            "response": "Response not available.",
            "key_points": []
        })
    elif group == 2:
        return GROUP2_OBJECTIONS.get(objection, {
            "response": "Response not available.",
            "key_points": []
        })
    else:
        return {
            "response": "Invalid objection group.",
            "key_points": []
        }

def get_all_objections(group: int) -> list:
    """Get list of all objections for a group"""
    if group == 1:
        return list(GROUP1_OBJECTIONS.keys())
    elif group == 2:
        return list(GROUP2_OBJECTIONS.keys())
    else:
        return []

def get_objection_groups() -> dict:
    """Get all objection groups"""
    return {
        1: "Common Sales Objections",
        2: "Technical and Trust Objections"
    }
