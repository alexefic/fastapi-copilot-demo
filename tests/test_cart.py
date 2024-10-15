from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Book, Cart, CartItem
from fastapi_demo.database import SessionLocal, engine
import pytest

client = TestClient(app)

@pytest.fixture(scope='module')
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope='function')
def mock_db_session(setup_database):
    db = setup_database
    db.query(CartItem).delete()
    db.query(Cart).delete()
    db.query(Book).delete()
    db.commit()
    yield db

@pytest.fixture(scope='function')
def test_user():
    return {'id': 1, 'username': 'testuser'}

def test_add_book_to_cart(mock_db_session, test_user):
    book = Book(id=1, title='Test Book', author='Test Author', pages=100, price=19.99)
    mock_db_session.add(book)
    mock_db_session.commit()
    response = client.post('/cart/add', json={'book_id': 1, 'quantity': 1}, headers={'Authorization': f'Bearer {test_user[