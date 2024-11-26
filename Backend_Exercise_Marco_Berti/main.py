import time
from Client import Client
from AdminClient import AdminClient


def main():

    url = "http://localhost:3001/"

    while True:
        print("\nWelcome to the Medacta books library")
        print("To authenticate, enter your username and press enter, then type your password and press enter. Type 'quit' in username field to exit the program.")

        username = input("Username: ").strip()
        if username.lower() == "quit":
            print("Thank you for using the Medacta books library. Goodbye!")
            break
        password = input("Password: ").strip()

        if username == "admin":
            client = AdminClient(url)
        else:
            client = Client(url)

        client.login(username, password)

        if client.token:
            client.display_books()

        while True:
            i = 1

            if client.check_session_expiry():
                #print("\nSession expired.") already printed inside the method check_session_expiry()
                break
            
            # Refresh information
            client.get_books()

            print("\nMenu:")
            print(f"{i}) View the list of books")
            list_ = i
            i += 1
            print(f"{i}) Borrow a book")
            borrow = i
            i += 1
            print(f"{i}) Return a book")
            return_ = i
            i += 1

            if client.user_type == "administrator":
                # print("Further administrator options:")
                print(f"{i}) Add a book")
                add = i
                i += 1
                print(f"{i}) Update a book")
                update = i
                i += 1
                print(f"{i}) Delete a book")
                delete = i
                i += 1

            print(f"{i}) End the session")
            end = i
            i += 1
            print(f"{i}) Quit the program")
            quit_ = i

            if client.user_type == "standard":
                try:
                    choice = int(input("Choose an option (1/2/3/4/5): ").strip())
                except:
                    print("Error: the input must be an integer. Please try again.")
                    continue
            else:  # client.user_type == "administrator"
                try:
                    choice = int(input("Choose an option (1/2/3/4/5/6/7/8): ").strip())
                except:
                    print("Error: the input must be an integer. Please try again.")
                    continue

            if choice == list_:
                client.display_books()

            elif choice == borrow:
                if client.printAvailableBooks():
                    try:
                        book_id = input("\nEnter the ID of the book to borrow (or type 'back' to go to the previous menu): ").strip()
                        if book_id.lower() == "back":
                            continue
                        book_id = int(book_id)
                        client.borrow_book(book_id)
                    except ValueError:
                        print("Error: the ID must be an integer. Please try again.")
                else:
                    continue

            elif choice == return_:
                if client.printUnavailableBooks():
                    try:
                        book_id = input("\nEnter the ID of the book to return (or type 'back' to go to the previous menu): ").strip()
                        if book_id.lower() == "back":
                            continue
                        book_id = int(book_id)
                        client.return_book(book_id)
                    except ValueError:
                        print("Error: the ID must be an integer. Please try again.")
                else:
                    continue

            elif client.user_type == "administrator":  # Only admin user has these possibilities..
                if choice == add:
                    title = input("\nEnter the title of the new book (or type 'back' to go to the previous menu): ").strip()
                    if title.lower() == "back":
                        continue
                    author = input("Enter the author of the new book: ").strip()
                    client.add_book(title, author)

                elif choice == update:
                    client.display_books()
                    if not client.books:
                        continue
                    else:
                        while True:
                            try:
                                book_id = input("\nEnter the ID of the book to update (or type 'back' to go to the previous menu): ").strip()
                                if book_id.lower() == "back":
                                    break
                                book_id = int(book_id)
                                try:
                                    if client.find_book_by_id(book_id):
                                        print("Available options:\n1) Edit title\n2) Edit author\n3) Edit both")
                                        req = int(input("Choose an option (1/2/3): ").strip())
                                        if req == 1:
                                            new_title = input("Enter the new title: ").strip()
                                            if new_title:
                                                client.update_book(book_id=book_id, title=new_title)
                                                break
                                            else:
                                                print("Missing title.")
                                                continue
                                        if req == 2:
                                            new_author = input("Enter the new author: ").strip()
                                            if new_author:
                                                client.update_book(book_id=book_id, author=new_author)
                                                break
                                            else:
                                                print("Missing author.")
                                                continue
                                        new_title = input("Enter the new title: ").strip()
                                        new_author = input("Enter the new author: ").strip()
                                        if new_title:
                                            if new_author:
                                                client.update_book(book_id, new_title, new_author)
                                                break
                                            else:
                                                print("Missing author.")
                                                continue
                                        else:
                                            print("Missing title.")
                                            continue
                                    else:
                                        print(f"Book with ID {book_id} not found. Please try again.")
                                except:
                                    print("Input can only be an integer. Please try again.")
                            except ValueError:
                                print("Error: the ID must be an integer. Please try again.")

                elif choice == delete:
                    client.display_books()
                    if not client.books:
                        continue
                    else:
                        while True:
                            try:
                                book_id = input("\nEnter the ID of the book to delete (or type 'back' to go to the previous menu): ").strip()
                                if book_id.lower() == "back":
                                    break
                                book_id = int(book_id)
                                if client.find_book_by_id(book_id):
                                    client.delete_book(book_id)
                                    print(f"Book with ID {book_id} has been deleted.")
                                    break
                                else:
                                    print(f"Book with ID {book_id} not found. Please try again.")
                            except ValueError:
                                print("Error: the ID must be an integer. Please try again.")

                elif choice == end:
                    client.end_session()
                    break

                elif choice == quit_:
                    client.end_session()
                    print("Thank you for using the Medacta books library. Goodbye!")
                    exit(0)

            elif choice == end:
                client.end_session()
                break

            elif choice == quit_:
                client.end_session()
                print("Thank you for using the Medacta books library. Goodbye!")
                exit(0)

            else:
                print("Invalid option. Please try again.")

            time.sleep(1)
        print("\nThe session has expired, please log in again.")


if __name__ == "__main__":
    main()
