# models.py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.orm import Session
from database import SessionLocal

DATABASE_URL = "postgresql://postgres:123456789@postgres:5432/booklib"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("author.id"))
    author = relationship("Author", back_populates="books")

class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    borrowed_books = relationship("Borrow", back_populates="client")

class Borrow(Base):
    __tablename__ = "borrow"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("book.id"))
    client_id = Column(Integer, ForeignKey("client.id"))
    book = relationship("Book")
    client = relationship("Client")

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
