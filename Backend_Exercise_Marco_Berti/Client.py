import requests
import time
import json


class Client:

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.token = None
        self.start_time = None
        self.expiration = None
        self.books = []
        self.available_books = []
        self.borrowed_books = []
        self.user_type = "standard"


    def login(self, username: str, password: str):
        login_url = self.base_url + "auth/login"  # auth/login - endpoint
        login_data = {"username": username, "password": password}

        try:
            # POST request
            response = requests.post(login_url, json=login_data)
            if response.ok:
                response_json = response.json()
                self.token = response_json.get("token")
                #print("Token: ", self.token)
                self.expiration = float(response_json.get("expires_in_sec", 3600))
                self.start_time = time.perf_counter()
                print("\nLogin successful.")
            else:
                print(f"\nLogin error. Status code {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print("\nAn error occurred during the login request:", e)


    def check_session_expiry(self):
        """Check if the session has expired"""

        if self.token is None:
            print("\nSession not authenticated.")
            return True
        elapsed_time = time.perf_counter() - self.start_time
        if elapsed_time >= self.expiration:
            print("\nSession expired.")
            self.token = None
            return True
        return False


    def get_books(self):
        """Retrieves the books on the server"""

        if self.check_session_expiry():
            return

        books_url = self.base_url + "books"  # books - endpoint
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            # GET request
            response = requests.get(books_url, headers=headers)
            if response.ok:
                self.books = response.json()
                self.available_books = [book for book in self.books if not book["is_borrowed"]]
                self.borrowed_books = [book for book in self.books if book["is_borrowed"]]
            else:
                print(f"\nError: Status code {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print("\nAn error occurred during the books request:", e)


    def display_books(self):
        """Display the list of books from the local list"""

        self.get_books()

        if not self.books:
            print("\nNo books available in the library.")
            return

        print("\nBooks in the library:")
        for book in self.books:
            print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}, Borrowed: {book['is_borrowed']}")


    def borrow_book(self, book_id: int):
        """Try to borrow a book if available"""

        if self.check_session_expiry():
            return

        book = next((b for b in self.available_books if int(b["id"]) == book_id), None)
        if not book:
            print("\nThe book is not available for borrowing.")
            return

        borrow_url = f"{self.base_url}books/{book_id}"  # books - endpoint ---> books/id for put method
        book["is_borrowed"] = True
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        try:
            # PUT request
            response = requests.put(borrow_url, headers=headers, data=json.dumps(book))
            if response.ok:
                print(f"\nBook '{book['title']}' successfully borrowed!")
            else:
                print(
                    f"\nError borrowing the book. Status code {response.status_code}: {response.text}"
                )
        except requests.exceptions.RequestException as e:
            print("\nAn error occurred during the borrow request:", e)


    def return_book(self, book_id: int):
        """Return a borrowed book"""

        if self.check_session_expiry():
            return

        book = next((b for b in self.borrowed_books if int(b["id"]) == book_id), None)
        if not book:
            print("\nThe book was not found among your borrowed books.")
            return

        return_url = f"{self.base_url}books/{book_id}"  # books - endpoint ---> books/id for put method
        book["is_borrowed"] = False
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        try:
            # PUT request
            response = requests.put(return_url, headers=headers, data=json.dumps(book))
            if response.ok:
                print(f"\nBook '{book['title']}' successfully returned!")
            else:
                print(
                    f"\nError returning the book. Status code {response.status_code}: {response.text}"
                )
        except requests.exceptions.RequestException as e:
            print("\nAn error occurred during the return request:", e)


    def end_session(self):
        """End the session (invalidate the token)"""

        print("\nSession ended.")
        self.token = None
        self.start_time = None
        self.expiration = None
        self.books = []
        self.available_books = []
        self.borrowed_books = []


    def printAvailableBooks(self):
        if not self.available_books:
            print("\nThere are no available books to borrow")
            return False
        else:
            print("\nList of available books:")
            for b in self.available_books:
                print(f"ID: {b['id']}, Title: {b['title']}, Author: {b['author']}")
            return True


    def printUnavailableBooks(self):
        if not self.borrowed_books:
            print("\nThere are no books to return")
            return False
        else:
            print("\nList of books to return:")
            for b in self.borrowed_books:
                print(f"ID: {b['id']}, Title: {b['title']}, Author: {b['author']}")
            return True