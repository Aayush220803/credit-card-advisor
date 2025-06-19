import json
import os

# Load the card data
def load_cards():
    path = os.path.join(os.path.dirname(__file__), '../data/cards.json')
    with open(path, 'r') as f:
        return json.load(f)


def score_card(card, user_input):
    score = 0

    # Income eligibility
    if user_input["income"] >= card["eligibility"]["min_income"]:
        score += 2
    else:
        return 0

    # Credit score check (optional)
    if user_input.get("credit_score", "unknown") != "unknown":
        if user_input["credit_score"] >= card["credit_score_required"]:
            score += 1
        else:
            return 0

    # Normalize user inputs
    spending = [s.strip().lower() for s in user_input["spending"]]
    preferences = [p.strip().lower() for p in user_input["preferences"]]

    # Normalize card data
    card_spending = [s.lower() for s in card["ideal_for"]]
    card_benefits = [b.lower() for b in card["preferred_benefit"]]

    # Match spending categories
    for category in spending:
        for tag in card_spending:
            if category in tag or tag in category:
                score += 2
                break

    # Match preferred benefits
    for pref in preferences:
        for benefit in card_benefits:
            if pref in benefit or benefit in pref:
                score += 2
                break

    # Prefer lower annual fee
    score -= card["annual_fee"] / 1000

    return score



def recommend_cards(user_input, top_n=3):
    cards = load_cards()
    scored_cards = []

    # Normalize input
    try:
        income = int(user_input.get("income", 0))
    except ValueError:
        income = 0

    credit_score = user_input.get("credit_score", "unknown")
    try:
        credit_score = int(credit_score) if credit_score != "unknown" else "unknown"
    except:
        credit_score = "unknown"

    spending = user_input.get("spending", [])
    if isinstance(spending, str):
        spending = [s.strip().lower() for s in spending.split(",")]

    preferences = user_input.get("preferences", [])
    if isinstance(preferences, str):
        preferences = [p.strip().lower() for p in preferences.split(",")]

    spend_amounts = user_input.get("spend_amounts", {})

    # Score cards
    for card in cards:
        score = 0

        # Income check
        if income >= card["eligibility"]["min_income"]:
            score += 2
        else:
            continue

        # Credit score check
        if credit_score != "unknown":
            if credit_score >= card["credit_score_required"]:
                score += 1
            else:
                continue

        # Spending match
        for category in spending:
            if category in card["ideal_for"]:
                score += 2

        # Preference match
        for pref in preferences:
            if pref in card["preferred_benefit"]:
                score += 2

        # Lower fee better
        score -= card["annual_fee"] / 1000

        if score > 0:
            scored_cards.append((card, score))

    scored_cards.sort(key=lambda x: x[1], reverse=True)

    recommendations = []
    for card, score in scored_cards[:top_n]:
        recommendations.append({
            "name": card["name"],
            "issuer": card["issuer"],
            "image": card["image"],
            "annual_fee": card["annual_fee"],
            "reward_rate": card["reward_rate"],
            "perks": card["perks"],
            "why_recommended": f"Matches your spending on {', '.join(spending)} and preferences like {', '.join(preferences)}.",
            "estimated_savings": estimate_rewards(card, spend_amounts),
            "apply_link": card["affiliate_url"]
        })

    return recommendations


def estimate_rewards(card, spend_amounts):
    try:
        if "cashback" in card["reward_type"].lower():
            total_spend = sum(spend_amounts.values())
            cashback_rate = 0.03
            estimated = int(total_spend * cashback_rate)
            return f"Estimated ₹{estimated} cashback/year"
        elif "travel" in card["reward_type"].lower():
            return "Earn travel points worth up to ₹5,000/year"
        else:
            return "Varies based on usage"
    except:
        return "N/A"
