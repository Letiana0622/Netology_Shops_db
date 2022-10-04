# ORM WEBINAR NOTES:
# import sqlalchemy
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import declarative_base, relationship
# from models import create_tables, Course
# DSN = 'postgresql://postgres:postgres@localhost:5432/clients_db'
# engine = sqlalchemy.create_engine(DSN)
# Session = sessionmaker(bind=engine)
# session = Session()
#
# Base = declarative_base()
#
# class Course(Base):
#     __tablename__ = 'course'
#
# def create_tables(engine):
#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)
#
# def __str__(self):
#     return f'{self.id}:{self.name}'
#
# create_tables()
# course1 = Course(name = 'Python')
# session.add(course1)
# session.commit()
# print(course1)
#
# session.close()

import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)
    book = relationship("Book", back_populates="publisher")

class Book(Base):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.Text, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship(Publisher, back_populates="book")

class Shop(Base):
    __tablename__ = "shop"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

class Stock(Base):
    __tablename__ = "stock"
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")

class Sale(Base):
    __tablename__ = "sale"
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric, nullable=False)
    date_sale = sq.Column(sq.TIMESTAMP, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    stock = relationship(Stock, backref="sale")

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
