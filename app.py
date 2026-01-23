from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from models import db, Product
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create database tables and seed data
with app.app_context():
    db.create_all()
    
    # Check if database is empty, then seed with sample data
    if Product.query.count() == 0:
        sample_plants = [
            Product(name='Monstera Deliciosa', price=29.99, 
                   description='A beautiful tropical plant with large, glossy leaves. Perfect for indoor spaces.',
                   category='Indoor'),
            Product(name='Snake Plant', price=19.99,
                   description='Low maintenance succulent perfect for beginners. Purifies air naturally.',
                   category='Indoor'),
            Product(name='Fiddle Leaf Fig', price=39.99,
                   description='Tall, elegant plant with large violin-shaped leaves. Makes a statement.',
                   category='Indoor'),
            Product(name='Pothos', price=14.99,
                   description='Fast-growing trailing plant. Very easy to care for and propagate.',
                   category='Indoor'),
            Product(name='Peace Lily', price=24.99,
                   description='Elegant flowering plant that thrives in low light conditions.',
                   category='Indoor'),
            Product(name='Lavender', price=12.99,
                   description='Fragrant herb perfect for gardens. Attracts pollinators.',
                   category='Outdoor'),
            Product(name='Rosemary', price=9.99,
                   description='Aromatic herb great for cooking. Drought-tolerant and hardy.',
                   category='Outdoor'),
            Product(name='Succulent Mix', price=16.99,
                   description='Variety pack of colorful succulents. Perfect for small spaces.',
                   category='Succulent'),
        ]
        db.session.add_all(sample_plants)
        db.session.commit()
        print("Database seeded with sample plants!")

@app.route('/')
def index():
    # Get search query from URL parameters
    search_query = request.args.get('search', '')
    
    # Filter plants by name if search query exists
    if search_query:
        plants = Product.query.filter(
            Product.name.ilike(f'%{search_query}%')
        ).all()
    else:
        plants = Product.query.all()
    
    # Get cart count for display
    cart = session.get('cart', [])
    cart_count = len(cart)
    
    return render_template('index.html', plants=plants, search_query=search_query, cart_count=cart_count)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # Get or create cart in session
    cart = session.get('cart', [])
    
    # Find product
    product = Product.query.get_or_404(product_id)
    
    # Add product to cart
    cart.append({
        'id': product.id,
        'name': product.name,
        'price': product.price
    })
    
    # Save cart back to session
    session['cart'] = cart
    
    return redirect(url_for('index'))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    
    # Calculate total
    total = sum(item['price'] for item in cart)
    
    return render_template('cart.html', cart=cart, total=total)

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session['cart'] = []
    return redirect(url_for('view_cart'))

@app.route('/remove_from_cart/<int:index>', methods=['POST'])
def remove_from_cart(index):
    cart = session.get('cart', [])
    if 0 <= index < len(cart):
        cart.pop(index)
        session['cart'] = cart
    return redirect(url_for('view_cart'))

if __name__ == '__main__':
    app.run(debug=True)
