# seed_db.py
from app import app, db, Product, AdminID

with app.app_context():
    db.create_all()
    print("✅ Database tables created")

    # Add some sample admin unique ids
    if not AdminID.query.first():
        admin_ids = [
            AdminID(unique_id="ADMIN001"),
            AdminID(unique_id="ADMIN002"),
            AdminID(unique_id="ADMIN003")
        ]
        db.session.add_all(admin_ids)
        print("✅ Sample admin unique ids added")

    db.session.commit()

