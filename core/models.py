from sqlalchemy import Column, Integer, String, Float, Boolean, Text, BigInteger, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
import datetime
from enum import Enum as PyEnum

class OrderStatus(PyEnum):
    pending = "pending"
    confirmed = "confirmed"
    shipping = "shipping"
    done = "done"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(BigInteger, unique=True, index=True)
    full_name = Column(String)
    phone = Column(String)
    address = Column(Text)
    is_trusted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    orders = relationship("Order", back_populates="user")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    unit = Column(String, default='kg')
    is_available = Column(Boolean)
    description = Column(Text)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    total_price = Column(Float)
    delivery_slot = Column(String)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="orders")