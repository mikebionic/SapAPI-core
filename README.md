# **SAPHASAP E-Commerce Web Application**

*A powerful and flexible e-commerce platform with API + Flask Jinja template support*

---

## **Overview**

This is a **large-scale e-commerce platform** designed as part of the **SAPHASAP System**.
It combines:

* A **robust API backend**
* A **Flask Jinja2-compatible frontend system**
* Multiple **sample templates** ready to configure and deploy

The system is fully customizable, scalable, and built on a strong codebase using **Flask** and **SQLAlchemy ORM**.

### **Core Concept**

The platform supports building **entire marketplaces** where each business can:

* Create their own online store
* Add and manage their products
* Organize with custom categories and attributes
* Design their storefront look and feel

It supports:

* Multiple currencies & exchange rates
* Precision attribute filtering
* Multiple image upload with watermarking
* Brand, collection, and slider creation
* Checkout with online bank BPC integration (Turkmenistan legacy support)
* Rich, flexible database structure
* Strong security & session management

---

## **Tech Stack**

**Languages & Frameworks:**

* Python (≥ 3.6)
* Flask + Flask-Jinja Templates
* SQLAlchemy ORM
* JavaScript / jQuery / ReactJS

**Database & Caching:**

* PostgreSQL
* Redis (session and DB cache support)

---

## **Features**

✅ Stable REST API
✅ Web service for client applications
✅ Web-admin UI
✅ Web-client UI
✅ Multi-language (n18) support
✅ File management & compression
✅ Security & encryption
✅ Relational DB management
✅ PostgreSQL support
✅ Redis session & caching
✅ Modular architecture

🔲 Client Admin API
🔲 Full feature key activation
🔲 WebSocket support

---

## **TODO**

* [ ] Write admin client application
* [x] Prevent HTTP 500 server errors
* [x] Email server error notifications
* [x] Configure BCrypt usage toggler
* [ ] Reconfigure app to separate API from UI:

  * [ ] Separate API repository
  * [ ] Separate UI repository
  * [ ] Build new Flask-style repo
  * [ ] Optimize backend using Node.js
* [ ] Database updates:

  * [x] Track last user login, device, etc.
  * [ ] Migrate app configs to database

---

## **Installation Guide**

### **1. Install Python, pip, and venv**

```bash
sudo apt install python3-dev python3-venv python3-pip
```

### **2. Install PostgreSQL**

```bash
sudo apt install postgresql postgresql-contrib libpq-dev
```

### **3. Install Redis**

```bash
sudo apt install redis
```

### **4. Create a Python Virtual Environment**

```bash
python3 -m venv example_env
source example_env/bin/activate
```

### **5. Install Requirements**

```bash
pip3 install -r documentation/requirements.txt
```

Or use the alternative [pip installation command](documentation/pip_installation_command.md).

---

## **Configuration**

1. Edit settings in [`config.py`](main_pack/config.py)
2. Load sensitive data from `.env` ([example here](main_pack/.env.example.config))
3. Ensure `.env` is listed in `.gitignore` to prevent leaks

### **Site Configuration**

In `main_pack/static/web_config`:

* Add `robots.txt`
* Add `sitemap.xml`
* Add `watermark.png`

### **Database Migration**

```bash
python3 migrate.py
```

Or restore from the backup:

```bash
commerceDBTemplate.backup
```

---

## **API Highlights**

The backend provides a **rich set of endpoints** for managing categories, resources, orders, companies, and more.

### **Example: Category Management**

**Get all categories:**

```http
GET /api/categories/
```

**Add categories:**

```http
POST /api/categories/
```

**Update categories:**

```http
PUT /api/categories/
```

(See full examples in documentation)

---

## **Additional Documentation**

* [API Backend Info](documentation/api_backend.md)
* [API Routes](documentation/api_documentation.md)
* [Mail Setup](documentation/mail_setup.md)
* [py-Babel Translation](documentation/pybabel_usage.md)

---

## **Developer Notes**

* Supports **CLI testing** with `curl` commands for device registration.
* Authentication can be done via **username/password** or **Google OAuth**.
* Includes **order invoice API** with payment validation integration.

