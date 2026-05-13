from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    avatar_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    old_price = db.Column(db.Float)
    image_url = db.Column(db.String(500))
    description = db.Column(db.Text)
    specs = db.Column(db.Text)
    specs_full = db.Column(db.Text)
    socket = db.Column(db.String(50))
    form_factor = db.Column(db.String(50))
    ram_type = db.Column(db.String(20))
    gpu_length_max = db.Column(db.Integer)
    psu_form_factor = db.Column(db.String(20))
    cpu_cooler_height_max = db.Column(db.Integer)
    stock = db.Column(db.Integer, default=10)
    rating = db.Column(db.Float, default=0)
    reviews_count = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    price_history = db.relationship('PriceHistory', backref='product', lazy='dynamic', cascade='all, delete-orphan')

    def get_specs(self):
        if self.specs:
            try:
                return json.loads(self.specs)
            except:
                return {}
        return {}

    def get_specs_full(self):
        if self.specs_full:
            try:
                return json.loads(self.specs_full)
            except:
                return {}
        return {}

    def get_price_history_24h(self):
        from datetime import timedelta
        day_ago = datetime.utcnow() - timedelta(hours=24)
        return self.price_history.filter(PriceHistory.changed_at >= day_ago).order_by(PriceHistory.changed_at.asc()).all()

class PriceHistory(db.Model):
    __tablename__ = 'price_history'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    old_price = db.Column(db.Float)
    new_price = db.Column(db.Float, nullable=False)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)

class Brand(db.Model):
    __tablename__ = 'brands'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    logo_url = db.Column(db.String(500))

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, default=1)

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    total = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(50), default='Новый')

class PCBuild(db.Model):
    __tablename__ = 'pc_builds'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(200))
    cpu_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    motherboard_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    gpu_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    ram_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    storage_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    psu_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    case_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    cooler_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    total_price = db.Column(db.Float, default=0.0)
    is_compatible = db.Column(db.Boolean, default=True)
    compatibility_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class RepairOrder(db.Model):
    __tablename__ = 'repair_orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    client_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    device_type = db.Column(db.String(50), nullable=False)
    device_model = db.Column(db.String(200), nullable=False)
    problem_description = db.Column(db.Text, nullable=False)
    contact_method = db.Column(db.String(50))
    call_time = db.Column(db.String(50))
    status = db.Column(db.String(50), default='Новая заявка')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)