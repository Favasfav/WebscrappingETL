# Django Product Scraper

This Django project provides an API endpoint to scrape product information from the Sprouts Farmers Market website based on a given product name.

## Features

- Scrape product information including name, price, quantity, unit, and image URL.
- Save scraped product data to a PostgreSQL database.
- Return the scraped data as a JSON response.

## Technologies Used

- Django
- Django REST Framework
- Selenium
- BeautifulSoup
- pandas
- PostgreSQL

## Setup and Installation

### Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package installer)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/django-product-scraper.git
    cd django-product-scraper
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the PostgreSQL database:**

    - Create a PostgreSQL database and user.
    - Update the `DATABASES` setting in `settings.py` with your database credentials.

5. **Apply the database migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

## Usage

### API Endpoint

- **Endpoint:** `/datasorting/<str:product_name>/`
- **Method:** POST
- **Description:** Scrapes product information from Sprouts Farmers Market based on the given product name and returns the data as a JSON response. The data is also saved to the database.

### Example Request

```bash
POST http://localhost:8000/datasorting/apple/




[
    {
        "name": "Organic Fuji Apple",
        "price": 1.99,
        "stock": true,
        "quantity": 1.0,
        "unit": "lb",
        "price_per_unit": "1.99",
        "product_url": "https://shop.sprouts.com/search?search_term=apple&page=1",
        "image_url": "https://example.com/image.jpg"
    }
]





django-product-scraper/
├── myapp/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── urls.py
├── project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── venv/
├── manage.py
├── requirements.txt
└── README.md





asgiref==3.8.1
attrs==23.2.0
beautifulsoup4==4.12.3
certifi==2024.2.2
cffi==1.16.0
charset-normalizer==3.3.2
Django==5.0.6
djangorestframework==3.15.1
h11==0.14.0
idna==3.7
numpy==1.26.4
outcome==1.3.0.post0
packaging==24.0
pandas==2.2.2
psycopg2==2.9.9
pycparser==2.22
PySocks==1.7.1
python-dateutil==2.9.0.post0
python-dotenv==1.0.1
pytz==2024.1
requests==2.32.2
selenium==4.21.0
six==1.16.0
sniffio==1.3.1
sortedcontainers==2.4.0
soupsieve==2.5
sqlparse==0.5.0
trio==0.25.1
trio-websocket==0.11.1
typing_extensions==4.11.0
tzdata==2024.1
urllib3==2.2.1
webdriver-manager==4.0.1
wsproto==1.2.0
