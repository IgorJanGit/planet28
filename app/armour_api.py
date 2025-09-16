import json
import os

def get_armour_data():
    """Load armour data from the JSON file."""
    try:
        armour_path = os.path.join(os.path.dirname(__file__), 'armour_data.json')
        with open(armour_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading armour data: {e}")
        # Return empty data if file not found or invalid
        return {"armour_list": [], "special_rules": {}}

def list_armour():
    """Return all available armour items."""
    data = get_armour_data()
    return data.get("armour_list", [])

def get_armour(armour_name):
    """Get details of a specific armour by name."""
    armour_list = list_armour()
    for armour in armour_list:
        if armour["name"] == armour_name:
            return armour
    return None

def get_armour_special_rules():
    """Get all armour special rules and their descriptions."""
    data = get_armour_data()
    return data.get("special_rules", {})

def get_armour_special_rule_description(rule_name):
    """Get the description of a specific armour special rule."""
    rules = get_armour_special_rules()
    return rules.get(rule_name, "No description available")