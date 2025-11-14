from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Product, User, AdminID
from nlp_utils import extract_query_details
from product_filter import filter_products

# -------------------------
# APP CONFIG
# -------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursecretkey'  # change in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product_finder.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------------
# AUTH ROUTES
# -------------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        role = request.form.get("role", "user")
        username = request.form["username"]
        password = request.form["password"]
        mobile_number = request.form.get("mobile_number")
        email = request.form.get("email")
        address = request.form.get("address")
        state = request.form.get("state")
        country = request.form.get("country")
        unique_id = request.form.get("unique_id") if role == "admin" else None

        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash("❌ Username already exists", "danger")
            return redirect(url_for("register"))
        if email and User.query.filter_by(email=email).first():
            flash("❌ Email already registered", "danger")
            return redirect(url_for("register"))

        # If admin, validate unique_id
        if role == "admin":
            if not unique_id:
                flash("❌ Unique ID is required for admin registration", "danger")
                return redirect(url_for("register"))
            admin_id_entry = AdminID.query.filter_by(unique_id=unique_id).first()
            if not admin_id_entry:
                flash("❌ Invalid Unique ID for admin registration", "danger")
                return redirect(url_for("register"))

        new_user = User(
            username=username,
            role=role,
            unique_id=unique_id,
            mobile_number=mobile_number,
            email=email,
            address=address,
            state=state,
            country=country
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        flash("✅ Account created! Please login.", "success")
        return redirect(url_for("index"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("✅ Logged in successfully!", "success")
            return redirect(url_for("index"))
        else:
            flash("❌ Invalid username or password", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("✅ You have been logged out.", "info")
    return redirect(url_for("login"))


# -------------------------
# ADMIN PRODUCT MANAGEMENT
# -------------------------

@app.route("/admin/add_product", methods=["GET", "POST"])
@login_required
def add_product():
    if current_user.role != "admin":
        flash("🚫 Access denied!", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form["name"]
        category = request.form.get("category", "General")  # Default to "General" since category box removed
        sub_category = request.form.get("sub_category")  # Optional
        brand = request.form["brand"]
        price = request.form["price"]
        features = request.form["features"]
        use_case = request.form["use_case"]
        size = request.form.get("size")  # ✅ new size field (optional)

        new_product = Product(
            name=name,
            category=category,
            sub_category=sub_category,
            brand=brand,
            price=int(price),
            features=features,
            use_case=use_case,
            size=size  # ✅ include size in product creation
        )

        db.session.add(new_product)
        db.session.commit()
        flash("✅ Product added successfully!", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("add_product.html")



@app.route("/admin/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    if current_user.role != "admin":
        flash("🚫 Access denied!", "danger")
        return redirect(url_for("index"))

    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        product.name = request.form["name"]
        product.category = request.form.get("category", product.category)  # Keep existing if not provided
        product.sub_category = request.form.get("sub_category", product.sub_category)  # Keep existing if not provided
        product.brand = request.form["brand"]
        product.price = int(request.form["price"])
        product.features = request.form["features"]
        product.use_case = request.form["use_case"]
        product.size = request.form.get("size")  # ✅ update size field

        db.session.commit()
        flash("✅ Product updated successfully!", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("edit_product.html", product=product)



@app.route("/admin/delete_product/<int:product_id>", methods=["POST"])
@login_required
def delete_product(product_id):
    if current_user.role != "admin":
        flash("🚫 Access denied!", "danger")
        return redirect(url_for("index"))

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("✅ Product deleted successfully!", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/dashboard", methods=["GET"])
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        flash("🚫 Access denied! Admins only.", "danger")
        return redirect(url_for("index"))

    search_query = request.args.get("q", "")

    if search_query:
        products = Product.query.filter(
            (Product.name.ilike(f"%{search_query}%")) |
            (Product.brand.ilike(f"%{search_query}%")) |
            (Product.category.ilike(f"%{search_query}%")) |
            (Product.sub_category.ilike(f"%{search_query}%"))
        ).all()
    else:
        products = Product.query.all()

    return render_template("admin_dashboard.html", products=products, search_query=search_query)


# -------------------------
# PUBLIC ROUTES
# -------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "Missing 'query' field"}), 400

    query_details = extract_query_details(data["query"])
    # Override with filters from UI
    if data.get("category"):
        query_details["category"] = data["category"]
    if data.get("sub_category"):
        query_details["sub_category"] = data["sub_category"]

    products = Product.query.all()
    product_dicts = [p.to_dict() for p in products]
    matching_products = filter_products(query_details, product_dicts)
    return jsonify(matching_products)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_password != confirm_password:
            flash("❌ Passwords do not match.", "danger")
            return redirect(url_for("profile"))

        current_user.set_password(new_password)
        db.session.commit()
        flash("✅ Password updated successfully!", "success")
        return redirect(url_for("profile"))

    return render_template("profile.html")



# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


