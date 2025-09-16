import json
import os
from typing import Dict, List, Any, Optional

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Path to the misc items data file
MISC_ITEMS_DATA_FILE = os.path.join(current_dir, "misc_items_data.json")

def get_all_misc_items() -> List[Dict[str, Any]]:
    """Get all miscellaneous items data."""
    with open(MISC_ITEMS_DATA_FILE, "r") as f:
        data = json.load(f)
    return data["items"]

def get_misc_item_by_name(name: str) -> Optional[Dict[str, Any]]:
    """Get a specific miscellaneous item by name."""
    items = get_all_misc_items()
    for item in items:
        if item["name"] == name:
            return item
    return None

def get_misc_items_special_rules() -> Dict[str, str]:
    """Get all special rules for miscellaneous items."""
    with open(MISC_ITEMS_DATA_FILE, "r") as f:
        data = json.load(f)
    return data["special_rules"]

def get_misc_item_cost(name: str) -> int:
    """Get the cost of a specific miscellaneous item."""
    item = get_misc_item_by_name(name)
    if item:
        return item["cost"]
    return 0

def calculate_total_misc_items_cost(items: List[str]) -> int:
    """Calculate the total cost of a list of miscellaneous items."""
    total = 0
    for item_name in items:
        total += get_misc_item_cost(item_name)
    return total