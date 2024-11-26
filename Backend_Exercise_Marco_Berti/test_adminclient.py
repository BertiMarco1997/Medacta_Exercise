import pytest
from unittest.mock import patch, Mock
from AdminClient import AdminClient
import json


######################################################### LOGIN ADMIN CLIENT TESTS
def test_adminClient_login_success():
    admin = AdminClient("http://localhost:3001/")
    
    # Mock of the answer
    mock_response = {
        "token": "mocked_admin_token",
        "expires_in_sec": 3600
    }
    
    with patch("requests.post") as mock_post:
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = mock_response
        
        admin.login("test_admin_username", "test_admin_password")
        
        # Success since there's the token
        assert admin.token is not None
        assert admin.token == "mocked_admin_token"
        assert admin.expiration is not None

def test_client_login_failed():
    admin = AdminClient("http://localhost:3001/")
    
    with patch("requests.post") as mock_post:
        mock_post.return_value.ok = False
        mock_post.return_value.status_code = 401  # Unauthorized
        mock_post.return_value.text = "Unauthorized access"
        
        admin.login("test_admin_wrong_username", "test_admin_wrong_password")
        
        assert admin.token is None
        assert admin.expiration is None


######################################################### ADD_BOOK TESTS
def test_add_book_success():
    admin = AdminClient("http://localhost:3001/")
    admin.token = "test_token"
    admin.books = [{"id": 0, "title": "Existing Book", "author": "Author1", "is_borrowed": False}]
    admin.available_books = [{"id": 0, "title": "Existing Book", "author": "Author1", "is_borrowed": False}]

    with patch.object(admin, "check_session_expiry", return_value=False):
        # Mock of POST request
        with patch("requests.post") as mock_post:
            mock_response = Mock()
            mock_response.ok = True
            mock_post.return_value = mock_response

            # Adding the new book
            admin.add_book("New Book", "Author Name")

            # Check POST request had correct parameters and called exactly once
            mock_post.assert_called_once_with(
                "http://localhost:3001/books",
                json={
                    "id": 1,
                    "title": "New Book",
                    "author": "Author Name",
                    "is_borrowed": False,
                },
                headers={
                    "Authorization": "Bearer test_token",
                    "Content-Type": "application/json",
                },
            )

def test_add_book_failure():
    admin = AdminClient("http://localhost:3001/")
    admin.token = "test_token"
    admin.books = []

    with patch.object(admin, "check_session_expiry", return_value=False):
        # Mock of POST request
        with patch("requests.post") as mock_post:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.status_code = 400
            mock_response.text = "Bad Request"
            mock_post.return_value = mock_response

            # Mock of print
            with patch("builtins.print") as mock_print:
                admin.add_book("New Book", "Author Name")

                # Check right message was print
                mock_print.assert_called_once_with(
                    "\nError adding the book. Status code 400: Bad Request"
                )


######################################################### FIND BOOK BY ID TEST
def test_find_book_by_id_found():
    admin = AdminClient("http://localhost:3001/")
    admin.books = [
        {"id": 0, "title": "Book1", "author": "Author1", "is_borrowed": False},
        {"id": 1, "title": "Book2", "author": "Author2", "is_borrowed": True},
    ]

    # Check the book with ID = 0 is found
    assert admin.find_book_by_id(0) is True

    # Check the book with ID = 1 is found
    assert admin.find_book_by_id(1) is True

def test_find_book_by_id_not_found():
    admin = AdminClient("http://localhost:3001/")
    admin.books = [
        {"id": 0, "title": "Book1", "author": "Author1", "is_borrowed": False},
        {"id": 1, "title": "Book2", "author": "Author2", "is_borrowed": True},
    ]

    # Check that book with different ID w.r.t. the library is not found
    assert admin.find_book_by_id(2) is False
    assert admin.find_book_by_id(45) is False


######################################################### UPDATE_BOOK TEST
def test_update_book_success():
    admin = AdminClient("http://localhost:3001/")
    admin.token = "test_token"
    admin.books = [
        {"id": 0, "title": "Old Title", "author": "Old Author", "is_borrowed": False},
        {"id": 1, "title": "Book2", "author": "Author2", "is_borrowed": True},
    ]

    updated_title = "New Title"
    updated_author = "New Author"

    with patch.object(admin, "check_session_expiry", return_value=False):
        # Mock of PUT request
        with patch("requests.put") as mock_put:
            mock_response = Mock()
            mock_response.ok = True
            mock_put.return_value = mock_response

            # Mock of print
            with patch("builtins.print") as mock_print:
                # Updating book with ID = 0
                admin.update_book(0, title=updated_title, author=updated_author)

                # Check PUT request had correct parameters and called exactly once 
                mock_put.assert_called_once_with(
                    "http://localhost:3001/books/0",
                    data=json.dumps(
                        {"id": 0, "title": updated_title, "author": updated_author, "is_borrowed": False}
                    ),
                    headers={
                        "Authorization": "Bearer test_token",
                        "Content-Type": "application/json",
                    },
                )

                mock_print.assert_called_once_with("\nBook '0' successfully updated!")

def test_update_book_failure():
    admin = AdminClient("http://localhost:3001/")
    admin.token = "test_token"
    admin.books = [
        {"id": 0, "title": "Old Title", "author": "Old Author", "is_borrowed": False},
        {"id": 1, "title": "Book2", "author": "Author2", "is_borrowed": True},
    ]

    with patch.object(admin, "check_session_expiry", return_value=False):
        # Mock of PUT request
        with patch("requests.put") as mock_put:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.status_code = 400
            mock_response.text = "Bad Request"
            mock_put.return_value = mock_response

            # Mock of print
            with patch("builtins.print") as mock_print:
                # Updating book with ID = 0
                admin.update_book(0, title="New Title", author="New Author")

                # Check right print that is called exaclty once with correct message
                mock_print.assert_called_once_with("\nError updating the book. Status code 400: Bad Request")


######################################################### DELETE BOOK TESTS
def test_delete_book_success():
    admin = AdminClient("http://localhost:3001/")
    admin.token = "test_token"
    admin.books = [
        {"id": 0, "title": "Book1", "author": "Author1", "is_borrowed": False},
        {"id": 1, "title": "Book2", "author": "Author2", "is_borrowed": False},
    ]

    with patch.object(admin, "check_session_expiry", return_value=False):
        # Mock of DELETE request
        with patch("requests.delete") as mock_delete:
            mock_response = Mock()
            mock_response.ok = True
            mock_delete.return_value = mock_response

            # Mock of print
            with patch("builtins.print") as mock_print:
                # Deleting book with ID = 1
                admin.delete_book(1)

                # Check DELETE request had correct parameters and called exactly once 
                mock_delete.assert_called_once_with(
                    "http://localhost:3001/books/1",
                    headers={"Authorization": "Bearer test_token"},
                )

                # Check right print that is called exaclty once with correct message
                mock_print.assert_called_once_with("\nBook '1' successfully deleted from the library!")

def test_delete_book_failure():
    admin = AdminClient("http://localhost:3001/")
    admin.token = "test_token"
    admin.books = [
        {"id": 0, "title": "Book1", "author": "Author1", "is_borrowed": False},
        {"id": 1, "title": "Book2", "author": "Author2", "is_borrowed": False},
    ]

    with patch.object(admin, "check_session_expiry", return_value=False):
        # Mock of DELETE request
        with patch("requests.delete") as mock_delete:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.status_code = 404
            mock_response.text = "Book not found"
            mock_delete.return_value = mock_response

            # Mock of print
            with patch("builtins.print") as mock_print:
                # Deleting a book not present in self.books
                admin.delete_book(2)

                # Check right print that is called exaclty once with correct message
                mock_print.assert_called_once_with("\nError deleting the book. Status code 404: Book not found")
