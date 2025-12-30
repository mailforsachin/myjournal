import json
import re
from typing import Dict, List, Optional, Tuple

class TransactionCategorizer:
    """Categorize transactions based on rules.json"""
    
    def __init__(self, rules_path: str = "rules.json"):
        with open(rules_path, 'r') as f:
            self.rules = json.load(f)
        
        # Build keyword map for faster lookup
        self.keyword_map = self._build_keyword_map()
    
    def _build_keyword_map(self) -> Dict[str, Tuple[str, str, str]]:
        """Build a map of keyword to (category, type, rule_type)"""
        keyword_map = {}
        
        # Process all rule types
        rule_types = [
            'business_income',
            'business_expenses', 
            'personal_expenses',
            'investments',
            'transfers',
            'loans',
            'credit_card_payments'
        ]
        
        for rule_type in rule_types:
            if rule_type in self.rules:
                for rule_name, rule_data in self.rules[rule_type].items():
                    category = rule_data['category']
                    trans_type = rule_data.get('type', 'expense')
                    
                    for keyword in rule_data['keywords']:
                        keyword_lower = keyword.lower()
                        # Store with priority based on rule type order
                        priority = rule_types.index(rule_type)
                        keyword_map[keyword_lower] = (category, trans_type, rule_type, priority)
        
        return keyword_map
    
    def categorize_transaction(self, description: str, amount: float, trans_type: str) -> Dict:
        """Categorize a transaction based on description"""
        description_lower = description.lower()
        
        # Apply global rules
        if abs(amount) < self.rules['global_rules']['ignore_amount_below']:
            return {
                'auto_category': 'Small Transaction',
                'suggested_type': trans_type,
                'confidence': 'low'
            }
        
        # Check for keyword matches
        best_match = None
        best_priority = float('inf')
        
        for keyword, (category, rule_type, rule_name, priority) in self.keyword_map.items():
            if keyword in description_lower:
                if priority < best_priority:
                    best_match = (category, rule_type, rule_name)
                    best_priority = priority
        
        if best_match:
            category, suggested_type, rule_used = best_match
            return {
                'auto_category': category,
                'suggested_type': suggested_type,
                'rule_used': rule_used,
                'confidence': 'high'
            }
        
        # Default categorization
        defaults = self.rules['classification_defaults']
        if trans_type == 'income':
            default_cat = defaults['credit']
        else:
            default_cat = defaults['debit']
        
        return {
            'auto_category': default_cat,
            'suggested_type': trans_type,
            'confidence': 'low'
        }
    
    def get_all_categories(self) -> List[str]:
        """Get all unique categories from rules"""
        categories = set()
        
        for rule_type in self.rules:
            if isinstance(self.rules[rule_type], dict):
                for rule_name, rule_data in self.rules[rule_type].items():
                    if isinstance(rule_data, dict) and 'category' in rule_data:
                        categories.add(rule_data['category'])
        
        return sorted(list(categories))
