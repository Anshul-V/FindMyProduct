# 🛒 Personalized Product Finder

**An NLP-powered intelligent web application to understand user requirements and recommend the most relevant products using natural language queries.**

---

## Table of Contents

* [✨ Overview](#-overview)
* [🎯 Project Objectives](#-project-objectives)
* [🧠 System Features](#-system-features)
* [⚙️ Tech Stack](#️-tech-stack)
* [🏗️ System Architecture](#-system-architecture)
* [📝 NLP Pipeline](#-nlp-pipeline)
* [🚀 Backend APIs](#-backend-apis)
* [🗂️ Dataset & Metadata](#️-dataset--metadata)
* [🧪 Testing](#-testing)
* [📊 Results](#-results)
* [📦 Installation & Setup](#-installation--setup)
* [🧩 Folder Structure](#-folder-structure)
* [📚 Future Enhancements](#-future-enhancements)
* [👨‍💻 Author](#-author)

---

## Overview

The **Personalized Product Finder** is a smart product-recommendation web application built with Flask that interprets **natural language queries** (e.g., "I want a lightweight laptop for office work under 50k") and returns the most relevant products from a database.

The project features:

* **Keyword Extraction (Regex + Custom Rules)**
* **Brand, Category, Feature & Price Parsing**
* **Flask Backend API with Web UI**
* User authentication and role-based access (User/Admin)
* Admin dashboard for product management
* SQLite database with SQLAlchemy
* JSON-based product metadata
* Clean modular development with templates

---

## Project Objectives

✔️ Build an efficient **NLP-based keyword extraction engine**
✔️ Enable users to search products using **natural language** via web interface
✔️ Implement a secure **Flask web application** with authentication
✔️ Provide admin functionality for **product management**
✔️ Maintain a scalable & flexible **metadata structure** for products
✔️ Create a blueprint for extending this into a full-scale AI product recommender

---

## System Features

### NLP Understanding

* Identifies **brand**, **category**, **features**, **use-cases**, **price limits**
* Handles both short and long queries
* Uses regex, sets, and rule-based keyword extraction

### Product Matching & Filtering

* Matches user-extracted attributes with product metadata
* Supports multi-attribute filtering with scoring
* Ranking based on matching score and budget considerations

### Web Application (Flask)

* User registration and login with secure password hashing
* Natural language search interface
* Admin dashboard for product CRUD operations
* Responsive Bootstrap UI with templates

### Authentication & Security

* Role-based access control (User/Admin)
* Session management with Flask-Login
* Admin registration with unique ID validation

### Database Management

* SQLite database with SQLAlchemy ORM
* Product, User, and AdminID models
* Database seeding from JSON data

---

## Tech Stack

| Layer            | Technology                       |
| ---------------- | -------------------------------- |
| Backend          | **Python Flask 3.1.2**           |
| Database         | **SQLite with SQLAlchemy 2.0.43**|
| Authentication   | **Flask-Login 0.6.3**            |
| Frontend         | **HTML/CSS with Bootstrap 5.3.2**|
| NLP              | Regex, Custom Keyword Extraction |
| Testing          | Manual testing, API validation   |
| Data             | JSON product metadata            |

---

## System Architecture

```
User Query (Web UI) → NLP Processor → Extracted Keywords → Product Filter → Database Query → Ranked Results → Web Display
```

**Components**

* 🧠 `nlp_utils.py` – Keyword extraction logic
* 🗂️ `products.json` – Initial product data
* 🔌 `app.py` – Flask web application server
* 🗃️ `models.py` – Database models (Product, User, AdminID)
* 🔍 `product_filter.py` – Product matching and scoring
* 🎨 `templates/` – HTML templates for UI
* 🧪 Manual testing and validation

---

## NLP Pipeline

### 1️⃣ **Preprocessing**

* Lowercasing input text
* Removing unnecessary punctuation
* Basic tokenization

### 2️⃣ **Keyword Extraction Modules**

* **Brand extraction**: Matches against known brands (Dell, HP, Lenovo, Asus, Acer, Redmi, Apple, Vivo)
* **Category extraction**: Maps keywords to categories (electronics, etc.)
* **Sub-category extraction**: Maps to product types (laptop, phone, tablet)
* **Feature extraction**: Matches against known features (lightweight, gaming optimized, long battery, etc.)
* **Use-case extraction**: Matches use cases (gaming, office, student, professional)
* **Price detection**: Regex patterns for budget constraints ("under/below/less than X")

### 3️⃣ **Rule-based Mapping**

* Matches tokens with predefined sets:

  ```python
  known_brands = {"dell", "hp", "lenovo", "asus", "acer", "redmi", "apple", "vivo"}
  known_use_cases = {"gaming", "office", "student", "professional"}
  known_features = {"long battery", "portable", "lightweight", "high performance", ...}
  sub_category_map = {"laptop": "laptop", "phone": "phone", "mobile": "phone", ...}
  ```

### 4️⃣ **Output Structure**

```json
{
  "budget": 50000,
  "brand": "dell",
  "features": ["lightweight", "portable"],
  "use_case": ["office", "student"],
  "sub_category": "laptop"
}
```

---

## Backend APIs

### 📌 **1. /recommend (POST)**

Returns product recommendations based on NLP analysis.

**Input:**

```json
{
  "query": "I want a lightweight Dell laptop for office use under 50k",
  "category": "electronics",
  "sub_category": "laptop"
}
```

**Output:**

```json
[
  {
    "id": 1,
    "name": "Dell Inspiron 14",
    "category": "electronics",
    "sub_category": "laptop",
    "brand": "Dell",
    "price": 47990,
    "features": ["long battery", "portable", "lightweight"],
    "use_case": ["office", "student"],
    "size": null
  }
]
```

### 📌 **2. /health (GET)**

Health check endpoint.

**Output:**

```json
{"status": "ok"}
```

### 📌 **Authentication Endpoints**

* `GET/POST /register` – User registration
* `GET/POST /login` – User login
* `GET /logout` – User logout
* `GET/POST /profile` – User profile management

### 📌 **Admin Endpoints** (Require Admin Role)

* `GET/POST /admin/add_product` – Add new product
* `GET/POST /admin/edit_product/<id>` – Edit product
* `POST /admin/delete_product/<id>` – Delete product
* `GET /admin/dashboard` – Admin dashboard

---

## Dataset & Metadata

Products stored in JSON format and imported to SQLite database:

```json
{
  "name": "Dell Inspiron 14",
  "category": "electronics",
  "sub_category": "laptop",
  "brand": "Dell",
  "price": 47990,
  "features": ["long battery", "portable", "lightweight"],
  "use_case": ["office", "student"]
}
```

**Database Models:**

* **Product**: id, name, category, sub_category, brand, price, features, use_case, size
* **User**: id, username, password_hash, role, unique_id, mobile_number, email, address, state, country
* **AdminID**: id, unique_id

---

## Testing

### Manual Testing

* NLP extraction accuracy for various query types
* Price parsing and budget filtering
* Category, brand, and feature recognition
* Product matching and scoring logic

### API Testing

* Web interface testing for search functionality
* Authentication flow testing
* Admin dashboard operations
* Database operations and data integrity

### Edge Cases

* Empty or invalid queries
* Products over budget
* Missing product attributes
* Authentication failures

---

## Results

* **High accuracy** for common keywords and brand recognition
* **Effective filtering** based on budget and multiple attributes
* **Stable API performance** with proper error handling
* **Fully functional web application** with secure authentication
* **Scalable database design** supporting product management

---

## Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone <repository-url>
cd product_finder_next_phase
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set up the database

```bash
python seed_db.py
```

### 5️⃣ Run the application

```bash
python app.py
```

**Access at:** `http://localhost:5000`

### 6️⃣ Test the application

* Register as user or admin
* Search for products using natural language
* Admin users can manage products via dashboard

---

## Folder Structure

```
📦 product_finder_next_phase
├── app.py                      # Main Flask application
├── models.py                   # Database models
├── nlp_utils.py               # NLP keyword extraction
├── product_filter.py          # Product filtering logic
├── import_products_json.py    # JSON import utilities
├── seed_db.py                 # Database seeding script
├── requirements.txt           # Python dependencies
├── products.json              # Initial product data
├── README.md                  # Project documentation
├── instance/
│   └── product_finder.db      # SQLite database
└── templates/
    ├── base.html              # Base template
    ├── index.html             # Home page with search
    ├── login.html             # Login page
    ├── register.html          # Registration page
    ├── profile.html           # User profile
    ├── add_product.html       # Add product form
    ├── edit_product.html      # Edit product form
    └── admin_dashboard.html   # Admin dashboard
```

---

## Future Enhancements

🚀 Replace regex with **ML models (BERT, SpaCy)** for better NLP
🛒 Integrate with real **e-commerce APIs** (Amazon, Flipkart)
📊 Implement advanced **ranking algorithms** with user preferences
📱 Add **mobile app** or **React frontend**
🧠 Add **intent classification** using transformers
🔍 Implement **fuzzy matching** for brand names
📈 Add **analytics dashboard** for search patterns
🔐 Enhance security with **OAuth** and **JWT tokens**
☁️ Deploy to cloud platforms (**Heroku, AWS, Azure**)

---

## 👨‍💻 Author

**Anshul V** 

---

*Happy Product Finding! 🛒✨*
