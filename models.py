from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    sub_category = db.Column(db.String(50), nullable=True)
    brand = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Integer, nullable=False)
    features = db.Column(db.String(500))  # store as comma-separated string
    use_case = db.Column(db.String(200))  # store as comma-separated string

    # ✅ New column for fashion/sports sizes (optional)
    size = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "sub_category": self.sub_category,
            "brand": self.brand,
            "price": self.price,
            "features": self.features.split(",") if self.features else [],
            "use_case": self.use_case.split(",") if self.use_case else [],
            "size": self.size  # include size in dict
        }


# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")  # user or admin

    # New fields for registration
    unique_id = db.Column(db.String(100), unique=True, nullable=True)  # only for admin
    mobile_number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    address = db.Column(db.String(200), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# AdminID model to store valid admin unique ids
class AdminID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(100), unique=True, nullable=False)
