# Medacta_Exercise
Backend exercise for Medacta

**Python Version** -- 3.11.9  
**IDE** -- Visual Studo Code  
**Libraries used** -- Requests 2.32.3 - pytest 8.3.3 - unittest - time - json

# How to run the program
1. Download the folder "Backend_Exercice_Marco_Berti" and open it on Visual Studio Code (or any other IDE)
2. Open Mockoon and click on File-> Open Local Environment and select the file "library.json"
3. Run the imported API to simulate the server
4. Run main.py on VS Code and follow the instructions in the terminal

Valid login:
- Standard Client --> username: "mario"  password: "rossi"
- Admin Client --> username: "admin"  password: "admin123"  

# How to run the tests
1. Open a new terminal and ensure you are in the folder containing the scripts
2. Digit "pytest test_client.py" for testing the Client class, or digit "pytest test_adminclient.py" for testing the adminClient class

# Problem solved
Using the provided library.json file to import into Mockoon, there was an issue with logging in with the correct username but an incorrect password or no password at all. It incorrectly logged in every time.

# Considerations
Since a data bucket for users and their personal information, such as borrowed books, has not been implemented, it is not possible to assign borrowed books to a user, but the book is generally marked as borrowed. This is because, at the end of the session, this information is deleted locally. As a result, a book reserved by "mario" can be returned by "admin", and vice versa.
