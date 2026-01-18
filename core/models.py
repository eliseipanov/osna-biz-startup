from sqlalchemy import Column, Integer, String, Float, Boolean, Text, BigInteger, DateTime, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship
from .database import Base
import datetime
from enum import Enum as PyEnum
from flask_login import UserMixin

# Junction table for many-to-many relationship between Product and Category
product_categories_association = Table(
    'product_categories_association',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

class OrderStatus(PyEnum):
    NEW = "NEW"
    VERIFIED = "VERIFIED"
    PROCUREMENT = "PROCUREMENT"
    IN_DELIVERY = "IN_DELIVERY"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class LanguagePref(PyEnum):
    uk = "uk"
    de = "de"

class AvailabilityStatus(PyEnum):
    IN_STOCK = "IN_STOCK"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    ON_REQUEST = "ON_REQUEST"

class TransactionType(PyEnum):
    DEPOSIT = "DEPOSIT"
    PAYMENT = "PAYMENT"
    REFUND = "REFUND"

class TransactionStatus(PyEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(BigInteger, unique=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password_hash = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(Text)
    is_trusted = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    language_pref = Column(Enum(LanguagePref), default=LanguagePref.de)
    admin_notes = Column(Text)
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    orders = relationship("Order", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user")

    def __str__(self):
        return self.full_name or self.username or f"User {self.id}"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    type = Column(Enum(TransactionType))
    status = Column(Enum(TransactionStatus))
    external_id = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="transactions")

    def __str__(self):
        return f"Transaction {self.id}: {self.type.value} {self.amount}"

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Float, default=1.0)

    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

    def __str__(self):
        return f"CartItem {self.id}: {self.product.name} x{self.quantity}"

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Float)
    final_weight = Column(Float, nullable=True)
    price_at_time = Column(Float)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

    def __str__(self):
        return f"OrderItem {self.id}: {self.product.name} x{self.quantity}"

class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    name_de = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)

    farms = relationship("Farm", back_populates="region")

    def __str__(self):
        return self.name


class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description_uk = Column(Text, nullable=True)
    description_de = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    contact_info = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    image_path = Column(String(255), nullable=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=True)
    farm_type = Column(String(50), nullable=True)

    products = relationship("Product", back_populates="farm")
    region = relationship("Region", back_populates="farms")

    def __str__(self):
        return self.name

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    name_de = Column(String)
    price = Column(Float)
    unit = Column(String, default='kg')
    sku = Column(String(50), unique=True, nullable=True)
    availability_status = Column(Enum(AvailabilityStatus), default=AvailabilityStatus.IN_STOCK)
    description = Column(Text)
    description_de = Column(Text)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=True)
    image_path = Column(String(255), nullable=True)

    categories = relationship("Category", secondary="product_categories_association", back_populates="products")
    farm = relationship("Farm", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

    def __str__(self):
        return f"{self.name} ({self.farm.name if self.farm else 'No Farm'})"

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    name_de = Column(String)
    slug = Column(String, unique=True)
    image_url = Column(String)
    description = Column(Text)
    description_de = Column(Text)
    image_path = Column(String(255), nullable=True)

    products = relationship("Product", secondary="product_categories_association", back_populates="categories")

    def __str__(self):
        return self.name

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(OrderStatus), default=OrderStatus.NEW)
    total_price = Column(Float)
    delivery_address = Column(Text)
    contact_phone = Column(String)
    delivery_slot = Column(String)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class StaticPage(Base):
    __tablename__ = "static_pages"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    title_de = Column(String)
    slug = Column(String, unique=True)
    content = Column(Text)
    content_de = Column(Text)
    seo_title_uk = Column(String)
    seo_title_de = Column(String)
    seo_description_uk = Column(Text)
    seo_description_de = Column(Text)

class GlobalSettings(Base):
    __tablename__ = "global_settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True)
    value = Column(Text)

class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True)
    value_uk = Column(Text)
    value_de = Column(Text)