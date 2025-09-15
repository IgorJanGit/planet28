import json
import os

def get_weapons_data():
    """Load weapons data from the JSON file."""
    try:
        weapons_path = os.path.join(os.path.dirname(__file__), 'weapons_data.json')
        with open(weapons_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading weapons data: {e}")
        # Return empty data if file not found or invalid
        return {"weapons": [], "special_rules": {}}

def list_weapons():
    """Return the list of all available weapons."""
    data = get_weapons_data()
    return data.get("weapons", [])

def get_weapon(name):
    """Get a specific weapon by name."""
    weapons = list_weapons()
    for weapon in weapons:
        if weapon["name"] == name:
            return weapon
    return None

def get_weapon_types():
    """Return a list of unique weapon types."""
    weapons = list_weapons()
    types = set()
    for weapon in weapons:
        # Split multiple types and add each separately
        for t in weapon["type"].split(","):
            types.add(t.strip())
    return sorted(list(types))

def get_weapons_by_type(weapon_type):
    """Return weapons filtered by type."""
    weapons = list_weapons()
    return [w for w in weapons if weapon_type.strip() in w["type"]]

def get_special_rules():
    """Return the dictionary of special rules."""
    data = get_weapons_data()
    return data.get("special_rules", {})

def get_special_rule(rule_name):
    """Get the description of a specific special rule."""
    rules = get_special_rules()
    return rules.get(rule_name, "No description available.")