import pytest
from unittest.mock import patch, MagicMock
from Client import Client
import json


######################################################### LOGIN STANDARD CLIENT TESTS
def test_client_login_success():
    client = Client("http://localhost:3001/")
    
    # Mock of the answer
    mock_response = {
        "token": "mocked_token",
        "expires_in_sec": 3600
    }
    
    # Mock of the POST request
    with patch("requests.post") as mock_post:
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = mock_response
        
        client.login("test_username", "test_password")
        
        # Success since there's the token
        assert client.token is not None
        assert client.token == "mocked_token"
        assert client.expiration is not None

def test_client_login_failed():
    client = Client("http://localhost:3001/")
    
    # Mock of the POST request
    with patch("requests.post") as mock_post:
        mock_post.return_value.ok = False
        mock_post.return_value.status_code = 401  # Unauthorized
        mock_post.return_value.text = "Unauthorized access"
        
        client.login("invalid_username", "invalid_password")
        
        assert client.token is None
        assert client.expiration is None

        
######################################################### DISPLAY BOOKS TESTS
def test_display_books_no_books():
    client = Client("http://localhost:3001/")
    
    with patch.object(client, "check_session_expiry", return_value=False):
        # Mock of GET request to retrieve books
        with patch("requests.get") as mock_requests_get:
            mock_requests_get.return_value.ok = True
            # No books in the answer
            mock_requests_get.return_value.json.return_value = []

            # No books to visualize
            client.books = []

            # Mock of print
            with patch("builtins.print") as mock_print:
                
                client.display_books()

                # Check correctness of print that is called exactly once with correct message
                mock_print.assert_called_once_with("\nNo books available in the library.")


def test_display_books_with_books():
    client = Client("http://localhost:3001/")
    # Books in the library
    client.books = [
        {"id": 0, "title": "Book One", "author": "Author A", "is_borrowed": False},
        {"id": 1, "title": "Book Two", "author": "Author B", "is_borrowed": True},
    ]

    # Mock of print
    with patch("builtins.print") as mock_print:
        client.display_books()
        
        # Check correctness of print
        mock_print.assert_any_call("\nBooks in the library:")
        mock_print.assert_any_call("ID: 0, Title: Book One, Author: Author A, Borrowed: False")
        mock_print.assert_any_call("ID: 1, Title: Book Two, Author: Author B, Borrowed: True")

######################################################### BORROW BOOK TESTS
def test_borrow_book_success():
    # There's a Client with an available book
    client = Client("http://localhost:3001/")
    client.token = "test_token"
    client.available_books = [{"id": 0, "title": "Book1", "author": "Author1", "is_borrowed": False}]
    client.borrowed_books = []

    with patch.object(client, "check_session_expiry", return_value=False):
        # Mock of PUT request
        with patch("requests.put") as mock_put:
            mock_response = MagicMock()
            mock_response.ok = True
            mock_put.return_value = mock_response

            # Borrowing the available book
            client.borrow_book(0)

            # Checking put request is called exactly once
            mock_put.assert_called_once_with(
                f"{client.base_url}books/0",
                headers={
                    "Authorization": f"Bearer {client.token}",
                    "Content-Type": "application/json",
                },
                data=json.dumps({"id": 0, "title": "Book1", "author": "Author1", "is_borrowed": True}),
            )

def test_borrow_book_not_available():
    client = Client("http://localhost:3001/")
    client.available_books = [{"id": 0, "title": "Book1", "author": "Author1", "is_borrowed": False}]
    client.borrowed_books = []

    with patch.object(client, "check_session_expiry", return_value=False):
        # Mock of print
        with patch("builtins.print") as mock_print:
            client.borrow_book(1)  # Prova a prendere un libro non disponibile

        # Check correctness of print that is called exactly once with correct message
            mock_print.assert_called_with("\nThe book is not available for borrowing.")


######################################################### RETURN BOOK TESTS
def test_return_book_success():
    # There's a Client with a borrowed book
    client = Client("http://localhost:3001/")
    client.token = "test_token"
    client.borrowed_books = [{"id": 0, "title": "Book1", "author": "Author1", "is_borrowed": True}]
    client.available_books = []

    with patch.object(client, "check_session_expiry", return_value=False):
        # Mock of PUT request
        with patch("requests.put") as mock_put:
            mock_response = MagicMock()
            mock_response.ok = True
            mock_put.return_value = mock_response

            # Returning the borrowed book
            client.return_book(0)

            # Checking put request is called exactly once
            mock_put.assert_called_once_with(
                f"{client.base_url}books/0",
                headers={
                    "Authorization": f"Bearer {client.token}",
                    "Content-Type": "application/json",
                },
                data=json.dumps({"id": 0, "title": "Book1", "author": "Author1", "is_borrowed": False}),
            )

def test_return_book_not_borrowed():
    client = Client("http://localhost:3001/")
    client.borrowed_books = [{"id": 0, "title": "Book1", "author": "Author1", "is_borrowed": True}]
    client.available_books = []

    with patch.object(client, "check_session_expiry", return_value=False):
        # Mock of print
        with patch("builtins.print") as mock_print:
            # Try to return a book non borrowed
            client.return_book(1) 

            # Check correctness of print that is called exactly once with correct message
            mock_print.assert_called_with("\nThe book was not found among your borrowed books.")


######################################################### END SESSION TEST
def test_end_session():
    client = Client("http://localhost:3001/")
    
    # Simulating initial conditions of the Client
    client.token = "test_token"
    client.start_time = 123456.78
    client.expiration = 3600
    client.books = [{"id": 0, "title": "Book1", "author": "Author1", "is_borrowed": False}, {"id": 1, "title": "Book2", "author": "Author2", "is_borrowed": True}]
    client.available_books = [{"id": 0, "title": "Book1", "author": "Author1", "is_borrowed": False}]
    client.borrowed_books = [{"id": 1, "title": "Book2", "author": "Author2", "is_borrowed": True}]
    
    # Ending the session
    client.end_session()
    
    # Check reset of Client attribute
    assert client.token is None
    assert client.start_time is None
    assert client.expiration is None
    assert client.books == []
    assert client.available_books == []
    assert client.borrowed_books == []


######################################################### PRINT AVAILABLE BOOKS TESTS
def test_printAvailableBooks_no_books():
    client = Client("http://localhost:3001/")
    # No available books
    client.available_books = []  

    # Mock of print
    with patch("builtins.print") as mock_print:
        result = client.printAvailableBooks()
        
        # Check correctness of print
        mock_print.assert_called_once_with("\nThere are no available books to borrow")
        # Check return value
        assert result is False

def test_printAvailableBooks_with_books():
    client = Client("http://localhost:3001/")
    # 2 available books
    client.available_books = [
        {"id": 0, "title": "Book1", "author": "Author1"},
        {"id": 1, "title": "Book2", "author": "Author2"},
    ] 

    # Mock of print
    with patch("builtins.print") as mock_print:
        result = client.printAvailableBooks()
        
        # Check correctness of print
        mock_print.assert_any_call("\nList of available books:")
        mock_print.assert_any_call("ID: 0, Title: Book1, Author: Author1")
        mock_print.assert_any_call("ID: 1, Title: Book2, Author: Author2")
        # Check return value
        assert result is True


######################################################### PRINT UNAVAILABLE BOOKS TESTS
def test_printUnavailableBooks_no_books():
    client = Client("http://localhost:3001/")
    # No borrowed books
    client.borrowed_books = [] 

    # Mock of print
    with patch("builtins.print") as mock_print:
        result = client.printUnavailableBooks()
        
        # Check correctness of print
        mock_print.assert_called_once_with("\nThere are no books to return")
        # Check return value
        assert result is False

def test_printUnavailableBooks_with_books():
    client = Client("http://localhost:3001/")
    # 2 borrowed books
    client.borrowed_books = [
        {"id": 0, "title": "Book1", "author": "Author1"},
        {"id": 1, "title": "Book2", "author": "Author2"},
    ]  

    # Mock of print
    with patch("builtins.print") as mock_print:
        result = client.printUnavailableBooks()
        
        # Check correctness of print
        mock_print.assert_any_call("\nList of books to return:")
        mock_print.assert_any_call("ID: 0, Title: Book1, Author: Author1")
        mock_print.assert_any_call("ID: 1, Title: Book2, Author: Author2")
        # Check return value
        assert result is True