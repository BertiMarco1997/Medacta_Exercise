import requests
import time
from Client import Client
import json


class AdminClient(Client):
    
    def __init__(self, base_url: str):
        super().__init__(base_url)
        self.user_type = "administrator"


    def login(self, username: str, password: str):
        login_url = self.base_url + "auth/login_admin"  # auth/login_admin - endpoint
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
                print("\nAdmin login successful.")
            else:
                print(f"\nLogin error. Status code {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print("\nAn error occurred during the login request:", e)


    def add_book(self, title: str, author: str):
        """Add a new book to the library"""

        if self.check_session_expiry():
            return

        max_id = max(book["id"] for book in self.books) if self.books else 0
        new_id = max_id if len(self.books) == 0 else max_id + 1

        book_url = self.base_url + "books"  # books - endpoint
        headers = headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        book_data = {
            "id": new_id,
            "title": title,
            "author": author,
            "is_borrowed": False,  # Adding as NOT borrowed..
        }

        try:
            # POST request
            response = requests.post(book_url, json=book_data, headers=headers)
            if response.ok:
                print(f"\nBook '{title}' successfully added to the library!")
            else:
                print(f"\nError adding the book. Status code {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print("\nAn error occurred during the add book request:", e)


    def find_book_by_id(self, book_id: int) -> bool:
        """Check if the book with the given ID exists in the books list"""

        for book in self.books:
            if int(book["id"]) == book_id:
                return True
        return False


    def update_book(self, book_id: int, title: str = None, author: str = None):
        """Update an existing book in the library"""

        if self.check_session_expiry():
            return

        book = next((b for b in self.books if b["id"] == book_id), None)

        book_url = f"{self.base_url}books/{book_id}"  # books - endpoint ---> books/id for put method
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        if title is not None:
            book["title"] = title
        if author is not None:
            book["author"] = author
        try:
            # PUT request
            response = requests.put(book_url, data=json.dumps(book), headers=headers)
            if response.ok:
                print(f"\nBook '{book_id}' successfully updated!")
            else:
                print(f"\nError updating the book. Status code {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print("\nAn error occurred during the update book request:", e)


    def delete_book(self, book_id: int):
        """Delete a book from the library"""

        if self.check_session_expiry():
            return

        book_url = f"{self.base_url}books/{book_id}"  # books - endpoint ---> books/id for delete method
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            # DELETE request
            response = requests.delete(book_url, headers=headers)
            if response.ok:
                print(f"\nBook '{book_id}' successfully deleted from the library!")
            else:
                print(f"\nError deleting the book. Status code {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print("\nAn error occurred during the delete book request:", e)