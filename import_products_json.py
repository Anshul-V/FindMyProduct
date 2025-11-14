import json
import time
from app import app, db
from models import Product

def import_products_from_json(json_file_path, batch_size=10, delay=0.1):
    with app.app_context():
        with open(json_file_path, 'r', encoding='utf-8') as f:
            products_data = json.load(f)

        total = len(products_data)
        for i in range(0, total, batch_size):
            batch = products_data[i:i+batch_size]
            for prod in batch:
                product = Product(
                    name=prod.get('name'),
                    category=prod.get('category'),
                    sub_category=prod.get('sub_category'),
                    brand=prod.get('brand'),
                    price=prod.get('price'),
                    features=",".join(prod.get('features', [])) if isinstance(prod.get('features'), list) else prod.get('features'),
                    use_case=",".join(prod.get('use_case', [])) if isinstance(prod.get('use_case'), list) else prod.get('use_case'),
                    size=prod.get('size')
                )
                db.session.add(product)

            db.session.commit()
            print(f"✅ Imported batch {i//batch_size + 1} of {((total-1)//batch_size) + 1}")
            time.sleep(delay)  # small delay to reduce locking issues

        print(f"✅ Imported total {total} products from {json_file_path}")

if __name__ == "__main__":
    import_products_from_json('products.json')
