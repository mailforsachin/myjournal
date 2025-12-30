import json
from pathlib import Path

RULES_PATH = Path(__file__).parent / "rules.json"

with open(RULES_PATH, "r", encoding="utf-8") as f:
    RULES = json.load(f)


def _match_keywords(description: str, keywords: list[str]) -> bool:
    d = description.lower()
    return any(k.lower() in d for k in keywords)


def categorize(description: str, amount: float):
    """
    Returns:
      (txn_type, auto_category)
    """

    desc = description.lower()

    # ---- CREDIT CARD PAYMENTS ----
    ccp = RULES.get("credit_card_payments", {})
    if _match_keywords(desc, ccp.get("keywords", [])):
        return ccp["type"], ccp["category"]

    # ---- BUSINESS INCOME ----
    for _, rule in RULES.get("business_income", {}).items():
        if _match_keywords(desc, rule.get("keywords", [])):
            return rule["type"], rule["category"]

    # ---- BUSINESS EXPENSES ----
    for _, rule in RULES.get("business_expenses", {}).items():
        if _match_keywords(desc, rule.get("keywords", [])):
            return rule["type"], rule["category"]

    # ---- PERSONAL EXPENSES ----
    for _, rule in RULES.get("personal_expenses", {}).items():
        if _match_keywords(desc, rule.get("keywords", [])):
            return rule["type"], rule["category"]

    # ---- INVESTMENTS ----
    for _, rule in RULES.get("investments", {}).items():
        if _match_keywords(desc, rule.get("keywords", [])):
            return rule["type"], rule["category"]

    # ---- TRANSFERS ----
    for _, rule in RULES.get("transfers", {}).items():
        if _match_keywords(desc, rule.get("keywords", [])):
            return rule["type"], rule["category"]

    # ---- LOANS ----
    for _, rule in RULES.get("loans", {}).items():
        if _match_keywords(desc, rule.get("keywords", [])):
            return rule["type"], rule["category"]

    # ---- FALLBACK ----
    if amount < 0:
        return "Expense", RULES["classification_defaults"]["uncategorized"]
    else:
        return "Income", RULES["classification_defaults"]["uncategorized"]
