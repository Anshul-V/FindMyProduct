import re

known_brands = {"dell", "hp", "lenovo", "asus", "acer", "redmi", "apple", "vivo"}
known_use_cases = {"gaming", "office", "student", "professional"}
known_features = {
    "long battery", "portable", "lightweight", "high performance", "decent performance",
    "rgb keyboard", "durable", "touchscreen", "backlit keyboard", "good camera", "gaming optimized",
    "premium build", "thermal cooling", "ultraportable", "high refresh rate", "2-in-1 design", "affordable"
}
sub_category_map = {
    "laptop": "laptop",
    "phone": "phone",
    "mobile": "phone",
    "smartphone": "phone",
    "tablet": "tablet",
    "desktop": "desktop",
    "monitor": "monitor"
}

def extract_query_details(text):
    text_lower = text.lower()

    # Extract budget using regex
    budget = None
    budget_match = re.search(r"(?:under|below|less than)\s*(\d{4,6})", text_lower)
    if budget_match:
        budget = int(budget_match.group(1))

    # Extract brand using set intersection
    brand = next((b.title() for b in known_brands if b in text_lower), None)

    # Extract use cases
    use_case_matches = [uc for uc in known_use_cases if uc in text_lower]

    # Extract features
    feature_matches = [f for f in known_features if f in text_lower]

    sub_category = None
    for key in sub_category_map:
        if key in text_lower:
            sub_category = sub_category_map[key]
            break

    return {
        "budget": budget,
        "brand": brand,
        "features": feature_matches,
        "use_case": use_case_matches,
        "sub_category": sub_category
    }
