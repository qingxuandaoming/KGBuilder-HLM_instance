# -*- coding: utf-8 -*-
import json
import os

# Path to the data file
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'profile_data.json')

def load_data():
    """
    Load profile data from JSON file.
    """
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, encoding='utf-8') as f:
        return json.load(f)

# Load data once at module level (or could be loaded on demand)
data = load_data()

def get_profile(name):
    """
    Generate HTML profile string for a character.
    
    Args:
        name (str): Character name.
        
    Returns:
        str: HTML string of key-value pairs.
    """
    s = ''
    if name in data:
        for key, value in data[name].items():
            st = f"<dt class=\"basicInfo-item name\">{key}</dt><dd class=\"basicInfo-item value\">{value}</dd>"
            s += st
    return s
