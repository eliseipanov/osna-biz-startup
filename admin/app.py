from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL").replace("postgresql+asyncpg", "postgresql")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

from core.models import Base, User, Product, Order

Base.metadata.create_all(engine)

app = Flask(__name__)

admin = Admin(app, name='Osna Farm Admin', template_mode='bootstrap3')

admin.add_view(ModelView(User, Session()))
admin.add_view(ModelView(Product, Session()))
admin.add_view(ModelView(Order, Session()))

if __name__ == '__main__':
    app.run(debug=True)