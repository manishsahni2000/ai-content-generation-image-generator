import json

def load_brief(path):
    with open(path, 'r') as f:
        brief = json.load(f)
    if len(brief.get("products", [])) < 2:
        raise ValueError("Brief must include at least two products.")
    return brief