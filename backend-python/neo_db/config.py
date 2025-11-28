from py2neo import Graph

# Default configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "12345678" # Default password, override in local_config.py

# Try to import local configuration
try:
    from neo_db.local_config import NEO4J_URI as LOCAL_URI, NEO4J_USER as LOCAL_USER, NEO4J_PASSWORD as LOCAL_PASSWORD
    NEO4J_URI = LOCAL_URI
    NEO4J_USER = LOCAL_USER
    NEO4J_PASSWORD = LOCAL_PASSWORD
except ImportError:
    pass

graph = Graph(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

# Load configuration from JSON file
import json
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
data_map_path = os.path.join(base_dir, "data_map.json")

try:
    with open(data_map_path, 'r', encoding='utf-8') as f:
        data_map = json.load(f)
        CA_LIST = data_map.get("CA_LIST", {})
        similar_words = data_map.get("similar_words", {})
except FileNotFoundError:
    print(f"Warning: Configuration file {data_map_path} not found. Using empty defaults.")
    CA_LIST = {}
    similar_words = {}
except Exception as e:
    print(f"Error loading configuration: {e}")
    CA_LIST = {}
    similar_words = {}
