#### **Objective:**
Create an API client that interacts with a mocked API (using Mockoon). You will simulate a library book management system that interacts with the predefined API endpoints provided via Mockoon.
---
### **Task Overview:**
Your task is to create a simple client (preferably in Python) to perform CRUD operations on the library’s books and manage user authentication.
You will be provided with a **Mockoon API** configuration that simulates a backend for this.
---
### **Step 2: Task Requirements**
 
**Key Features to Implement:**
1. **Login Page/Functionality:**
   - The client should allow a user to log in.
   - On successful login, the JWT token returned by the API should be saved (e.g. in memory for a Python script).
2. **Book Listing:**
   - Fetch and display a list of available books.
   - Display basic information for each book, such as the title, author, and whether it's currently borrowed.
3. **Borrow/Return Books:**
   - Users should be able to borrow a book, but only if it’s available.
   - Users should be able to return a borrowed book.
4. **Admin Actions (Optional for extra points, require updating mocked API):**
   - Admins should be able to add, update, and delete books using the appropriate endpoints
   - You can simulate Admin access by logging in with a specific username and password (provided in the Mockoon config).
---
### **Bonus Tasks (Optional):**
1. **GUI:**
   - A nice and clean GUI is a bonus! 
2. **Handle API Errors:**
   - Show appropriate error messages if login fails or if a user tries to borrow a book that’s already borrowed.
3. **Testing:**
   - For Python: Write basic unit tests using `unittest` or `pytest` for API interaction functions. 
4. **Admin Role:**
   - Add functionality to create, edit, or delete books (admin-only actions).
5. **Mock API updates**
   - Improve API, add useful endpoints...
---
 
### **Mockoon Configuration Example (For Testing)**
 
You can import the file "library.json" into mockoon; to import it simply click on File-> Open Local Environment.
Valid login:   "username":"mario", "password":"rossi"
 
### **Deliverables:**
 
1. **Source Code**: A GitHub repository with either a Python script or frontend code that interacts with the Mockoon API.
2. **Instructions/Documentation**: Simple documentation explaining how to run the client and connect it to the Mockoon API.
 
---
 
### **Evaluation Criteria:**

With this exercise we would like to evaluate how you approach a problem, how you solve it, your coding style...

1. **Correctness**: The client should successfully interact with the mocked API endpoints (login, list books, borrow/return books).
2. **Code Quality**: The code should be clean, well-organized, and easy to understand.
3. **Error Handling**: Properly handle errors like invalid login attempts or borrowing already borrowed books.
4. **API Usage**: The ability to correctly handle JWT tokens and make authenticated requests.
5. **Time**: You have one week to complete the test, take the time you need for complete the exercise.
---


