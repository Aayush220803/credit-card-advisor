# credit-card-advisor/backend/utils/prompt_templates.py

WELCOME_MESSAGE = """
Hi! 👋 I'm your AI-powered credit card advisor.
I'll ask you a few quick questions to understand your needs and suggest the best cards in India for you. Let's begin!
"""

QUESTION_TEMPLATES = [
    {
        "key": "income",
        "prompt": "What's your **monthly income** in ₹ (approx)?",
        "type": "number"
    },
    {
        "key": "spending",
        "prompt": "Which **categories do you spend on most**? (e.g., fuel, travel, groceries, dining)",
        "type": "multi-select",
        "options": ["fuel", "travel", "groceries", "dining", "shopping", "online"]
    },
    {
        "key": "preferences",
        "prompt": "What kind of **benefits do you prefer**? (e.g., cashback, travel points, lounge access)",
        "type": "multi-select",
        "options": ["cashback", "travel", "lounge", "amazon vouchers"]
    },
    {
        "key": "existing_cards",
        "prompt": "(Optional) Do you already have any credit cards? If yes, which ones?",
        "type": "text"
    },
    {
        "key": "credit_score",
        "prompt": "What's your approximate **credit score**? If unknown, type 'unknown'.",
        "type": "text"
    }
]

RECOMMENDATION_PROMPT = """
Based on the following user profile:
- Monthly Income: ₹{income}
- Spending Categories: {spending}
- Benefit Preferences: {preferences}
- Credit Score: {credit_score}
- Existing Cards: {existing_cards}

Select and rank the top 3 Indian credit cards from our database that match the user's needs.
For each card, include:
- Card name
- Key benefits
- Reason for recommendation
- Estimated reward/cashback

Use simple language and justify why each card is a good fit.
"""
