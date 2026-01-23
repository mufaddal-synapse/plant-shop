# Plant E-Commerce Store

A Flask-based plant e-commerce web application with SQLite database and Bootstrap 5 UI.

## Features

- 🌱 Product catalog with plants organized by category
- 🔍 Search functionality to filter plants by name
- 🛒 Shopping cart system using Flask sessions (no login required)
- 📱 Responsive Bootstrap 5 design
- 💾 SQLite database with SQLAlchemy ORM

## Tech Stack

- **Backend**: Flask 3.0
- **Database**: SQLite with Flask-SQLAlchemy
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Session Management**: Flask Sessions

## Installation

1. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python app.py
```

4. **Open your browser** and navigate to:
```
http://127.0.0.1:5000
```

## Project Structure

```
plant-web-app/
├── app.py              # Main Flask application with routes
├── models.py           # Database models (Product)
├── requirements.txt    # Python dependencies
├── templates/
│   ├── index.html     # Home page with product grid
│   └── cart.html      # Shopping cart page
└── plants.db          # SQLite database (created automatically)
```

## Database Schema

### Product Model
- `id`: Primary key
- `name`: Product name (String)
- `price`: Product price (Float)
- `description`: Product description (Text)
- `category`: Product category (String)

## Features Details

### Search Functionality
- Real-time search filtering by plant name
- Uses SQLAlchemy's `ilike` for case-insensitive search
- Clear search button to reset filters

### Shopping Cart
- Session-based cart (no login required)
- Add items to cart
- Remove individual items
- Clear entire cart
- Display cart count in navbar
- Calculate total price

### Sample Data
The application automatically seeds the database with 8 sample plants on first run:
- Indoor plants (Monstera, Snake Plant, Fiddle Leaf Fig, Pothos, Peace Lily)
- Outdoor plants (Lavender, Rosemary)
- Succulents

## Routes

- `GET /` - Home page with all plants and search
- `POST /add_to_cart/<product_id>` - Add product to cart
- `GET /cart` - View shopping cart
- `POST /clear_cart` - Clear all items from cart
- `POST /remove_from_cart/<index>` - Remove specific item from cart

## Customization

### Adding More Plants
You can add more plants by modifying the seed data in [app.py](app.py) or by directly adding to the database through a Python shell:

```python
from app import app, db
from models import Product

with app.app_context():
    new_plant = Product(
        name='Your Plant Name',
        price=25.99,
        description='Plant description',
        category='Indoor'
    )
    db.session.add(new_plant)
    db.session.commit()
```

### Changing Secret Key
For production, change the secret key in [app.py](app.py):
```python
app.config['SECRET_KEY'] = 'your-secure-random-key-here'
```

## Future Enhancements

- User authentication and registration
- Product images
- Quantity selection in cart
- Checkout and payment integration
- Order history
- Admin panel for managing products
- Product categories filter
- Pagination for large product catalogs

## License

MIT License - Feel free to use this project for learning or commercial purposes.
