from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from fastapi_demo.main import app
from fastapi_demo.models import Book, Wishlist
from fastapi import HTTPException

client = TestClient(app)

@patch('fastapi_demo.routers.books.get_db')
def test_create_book(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    response = client.post('/books/', json={
        'title': 'Test Book',
        'author': 'Test Author',
        'pages': 100,
        'genre': 'Fiction'
    })
    assert response.status_code == 200
    assert response.json().get('title') == 'Test Book'
    assert response.json().get('author') == 'Test Author'
    assert response.json().get('pages') == 100
    assert response.json().get('genre') == 'Fiction'

@patch('fastapi_demo.routers.books.get_db')
def test_read_book_success(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title='Test Book', author='Test Author', pages=100, genre='Fiction')
    response = client.get('/books/1')
    assert response.status_code == 200
    assert response.json().get('title') == 'Test Book'
    assert response.json().get('author') == 'Test Author'
    assert response.json().get('pages') == 100
    assert response.json().get('genre') == 'Fiction'

@patch('fastapi_demo.routers.books.get_db')
def test_read_book_not_found(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.get('/books/1')
    assert response.status_code == 404
    assert response.json().get('detail') == 'Book not found'

@patch('fastapi_demo.routers.books.get_db')
def test_update_book_success(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title='Old Title', author='Old Author', pages=100, genre='Fiction')
    response = client.put('/books/1', json={
        'title': 'New Title',
        'author': 'New Author',
        'pages': 200,
        'genre': 'Non-Fiction'
    })
    assert response.status_code == 200
    assert response.json().get('title') == 'New Title'
    assert response.json().get('author') == 'New Author'
    assert response.json().get('pages') == 200
    assert response.json().get('genre') == 'Non-Fiction'

@patch('fastapi_demo.routers.books.get_db')
def test_update_book_not_found(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.put('/books/1', json={
        'title': 'New Title',
        'author': 'New Author',
        'pages': 200,
        'genre': 'Non-Fiction'
    })
    assert response.status_code == 404
    assert response.json().get('detail') == 'Book not found'

@patch('fastapi_demo.routers.books.get_db')
def test_delete_book_success(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    mock_db_session.query.return_value.filter.return_value.first.return_value = Book(id=1, title='Test Book', author='Test Author', pages=100, genre='Fiction')
    response = client.delete('/books/1')
    assert response.status_code == 200
    assert response.json().get('message') == 'Book deleted successfully'

@patch('fastapi_demo.routers.books.get_db')
def test_delete_book_not_found(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    response = client.delete('/books/1')
    assert response.status_code == 404
    assert response.json().get('detail') == 'Book not found'

@patch('fastapi_demo.routers.books.get_db')
def test_get_random_books_by_genre(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    mock_db_session.query.return_value.distinct.return_value.all.return_value = [('Fiction',), ('Non-Fiction',)]
    mock_db_session.query.return_value.filter.return_value.order_by.return_value.first.side_effect = [
        Book(id=1, title='Random Fiction Book', author='Author A', pages=123, genre='Fiction'),
        Book(id=2, title='Random Non-Fiction Book', author='Author B', pages=456, genre='Non-Fiction')
    ]
    response = client.get('/books/random')
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]['genre'] == 'Fiction'
    assert response.json()[1]['genre'] == 'Non-Fiction'

@patch('fastapi_demo.routers.books.get_db')
@patch('fastapi_demo.routers.books.get_current_user')
def test_add_to_wishlist(mock_get_current_user, mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    mock_get_current_user.return_value = MagicMock(id=1)
    response = client.post('/wishlist/', json={'book_id': 1})
    assert response.status_code == 200
    assert response.json().get('user_id') == 1
    assert response.json().get('book_id') == 1
