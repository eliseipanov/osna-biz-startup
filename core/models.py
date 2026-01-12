from sqlalchemy import Column, Integer, String, Float, Boolean, Text, BigInteger, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
import datetime
from enum import Enum as PyEnum
from flask_login import UserMixin

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
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    orders = relationship("Order", back_populates="user")

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

    products = relationship("Product", back_populates="farm")

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
    category_id = Column(Integer, ForeignKey("categories.id"))
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=True)
    image_path = Column(String(255), nullable=True)

    category = relationship("Category", back_populates="products")
    farm = relationship("Farm", back_populates="products")

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

    products = relationship("Product", back_populates="category")

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