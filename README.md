# BookTime E-Commerce Platform

BookTime is a Django-based e-commerce web application for browsing products, managing a shopping basket, and processing orders. It supports user authentication, address management, and full order checkout capabilities. Product images and thumbnails are handled via media directories.

---

## 🚀 Features

- **User Authentication**: Register, login, and logout functionality.
- **Product Management**: Browse products and view detailed information.
- **Basket Management**: Add items to a shopping basket and manage quantities.
- **Order Processing**: Choose billing/shipping addresses and complete purchases.
- **Media Handling**: Support for product images and thumbnails stored in `/media/product-images/` and `/media/productthumbnails/`.

---

## 🧰 Requirements

- Python 3.12+
- Django 5.2.1+
- PostgreSQL (recommended) or SQLite (for development)
- Virtual environment tool (e.g., `venv`)

---

## 🛠️ Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/smt-dev123/BookTime_Learning
   cd booktime
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Create a `.env` file in the project root and add:

   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///db.sqlite3  # Or use PostgreSQL connection URL
   ```

5. **Apply Migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

   Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to access the app.

---

## 📁 Directory Structure

```
booktime/
├── main/
│   ├── migrations/
│   ├── models.py              # Basket, Order, Product models
│   ├── views.py               # Views including add_to_basket, address selection
│   ├── forms.py               # AddressSelectionForm
│   ├── middleware.py          # Basket middleware
│   ├── templates/             # HTML templates
├── media/
│   ├── product-images/        # Original product images
│   ├── productthumbnails/     # Thumbnails for faster loading
├── booktime/
│   ├── settings.py            # Django settings
│   ├── urls.py                # URL routing
├── .gitignore                 # Ignore media/, venv/, etc.
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
```

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---
