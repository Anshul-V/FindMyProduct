import json

def load_products(file_path='products.json'):
    with open(file_path, 'r') as f:
        return json.load(f)

def filter_products(query_details, products):
    scored_products = []

    for product in products:
        score = 0

        # Category filtering
        if query_details.get("category"):
            if product["category"].lower() != query_details["category"].lower():
                continue

        # Sub-category filtering
        if query_details.get("sub_category"):
            if product.get("sub_category") is None or product["sub_category"].lower() != query_details["sub_category"].lower():
                continue

        #  Budget filtering (skip if over budget)
        if query_details["budget"] and product["price"] > query_details["budget"]:
            continue

        #  Strict brand filtering (skip if brand doesn't match)
        if query_details["brand"]:
            if product["brand"].lower() != query_details["brand"].lower():
                continue  #  skip this product completely if brand doesn't match
            else:
                score += 2  #  score for matching brand

        #  Use-case match
        matching_use_cases = [
            uc for uc in query_details["use_case"] if uc in product["use_case"]
        ]
        score += len(matching_use_cases)

        #  Feature match
        matching_features = [
            f for f in query_details["features"] if f in product["features"]
        ]
        score += len(matching_features)

        #  Price bonus
        if query_details["budget"]:
            if (query_details["budget"] - product["price"]) >= 5000:
                score += 1

        if score > 0:
            scored_products.append((product, score))

    #  Sort by score descending
    sorted_products = sorted(scored_products, key=lambda p: p[1], reverse=True)

    #  Return products only (strip scores)
    final_results = [p[0] for p in sorted_products]
    return final_results
