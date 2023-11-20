# api.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from models import Book, Author, Client, Borrow, SessionLocal

router = APIRouter()

# Static token list for demonstration purposes
STATIC_TOKENS = ["token1", "token2"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token_and_get_client_id(token: str = Depends(oauth2_scheme)):
    if token not in STATIC_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Replace this logic with your actual user identification based on the token
    # For simplicity, using a static client_id for each token
    # In real-world, you should authenticate and authorize users based on your system's logic
    if token == "token1":
        return 1
    elif token == "token2":
        return 2

@router.post("/books/")
def create_book(book_name: str, author_name: str, db: Session = Depends(SessionLocal), token: str = Depends(oauth2_scheme)):
    client_id = verify_token_and_get_client_id(token)

    author = db.query(Author).filter(Author.name == author_name).first()
    if author is None:
        author = Author(name=author_name)
        db.add(author)
        db.commit()
        db.refresh(author)

    book = Book(name=book_name, author_id=author.id, client_id=client_id)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@router.get("/books/")
def read_books(letter: str = None, author_name: str = None, db: Session = Depends(SessionLocal)):
    # Removed the 'token' parameter since it's already a dependency
    client_id = verify_token_and_get_client_id()

    query = db.query(Book).filter(Book.client_id == client_id)

    if letter:
        query = query.filter(Book.name.startswith(letter))
    if author_name:
        query = query.join(Author).filter(Author.name == author_name)

    books = query.all()
    return books

@router.get("/books/borrowed")
def get_borrowed_books(db: Session = Depends(SessionLocal), token: str = Depends(oauth2_scheme)):
    client_id = verify_token_and_get_client_id(token)

    borrowed_books = db.query(Book).filter(Book.client_id == client_id).all()
    
    return borrowed_books

@router.post("/authors/")
def create_author(author_name: str, db: Session = Depends(SessionLocal), token: str = Depends(oauth2_scheme)):
    verify_token_and_get_client_id(token)

    author = Author(name=author_name)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author

@router.post("/clients/")
def create_client(client_name: str, db: Session = Depends(SessionLocal), token: str = Depends(oauth2_scheme)):
    verify_token_and_get_client_id(token)

    client = Client(name=client_name)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client