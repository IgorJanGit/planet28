import json
import os

def get_special_rules_data():
    """Load special rules data from the JSON file."""
    try:
        rules_path = os.path.join(os.path.dirname(__file__), 'special_rules_data.json')
        print(f"Loading special rules from: {rules_path}")
        with open(rules_path, 'r') as f:
            data = json.load(f)
        print(f"Loaded data: {data}")
        return data
    except Exception as e:
        print(f"Error loading special rules data: {e}")
        # Return empty data if file not found or invalid
        return {"special_rules": {}}

def get_all_special_rules():
    """Return all special rules and their descriptions."""
    data = get_special_rules_data()
    return data.get("special_rules", {})

def get_special_rule_description(rule_name):
    """Get the description of a specific special rule."""
    print(f"Looking for description of rule: {rule_name}")
    rules = get_all_special_rules()
    description = rules.get(rule_name.strip(), "No description available")
    print(f"Found description: {description}")
    return description