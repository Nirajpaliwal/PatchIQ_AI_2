import json

# In-memory database for books and user carts
books_db = [
    {"id": "1", "title": "The Great Adventure", "author": "A.B. Coder", "price": 15.00, "stock": 5},
    {"id": "2", "title": "Mystery of the Missing Semicolon", "author": "C.D. Bugfixer", "price": 12.50, "stock": 3},
    {"id": "3", "title": "Learning Python", "author": "E.F. Developer", "price": 20.00, "stock": 0}
]

user_carts = {} # Stores carts as: {"user_id": {"book_id": quantity, ...}}

def list_books():
    """Lists all available books with their details."""
    print("--- Available Books ---")
    for book in books_db:
        stock_status = f"{book['stock']} in stock" if book['stock'] > 0 else "Out of stock"
        print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}, Price: ${book['price']:.2f}, Stock: {stock_status}")
    print("-----------------------")

def add_book_to_cart():
    """Allows a user to add a book to their cart."""
    user_id = input("Enter your user ID: ")
    book_id = input("Enter the ID of the book you want to add: ")
    quantity_str = input("Enter the quantity: ")

    try:
        quantity = int(quantity_str)
        if quantity <= 0:
            print("Quantity must be a positive number.")
            return
    except ValueError:
        print("Invalid quantity. Please enter a number.")
        return

    found_book = None
    for book in books_db:
        if book["id"] == book_id:
            found_book = book
            break

    if not found_book:
        print("Book not found.")
        return

    if found_book.get("stock", 0) > 0: # Fix: Use .get() with a default value to prevent KeyError
        if found_book["stock"] >= quantity:
            if user_id not in user_carts:
                user_carts[user_id] = {}
            
            user_carts[user_id][book_id] = user_carts[user_id].get(book_id, 0) + quantity
            found_book["stock"] -= quantity
            print(f"{quantity} of '{found_book['title']}' added to your cart.")
        else:
            print(f"Not enough stock for '{found_book['title']}'. Available: {found_book['stock']}")
    else:
        print(f"'{found_book['title']}' is out of stock.")

def view_cart():
    """Displays the contents of a user's cart."""
    user_id = input("Enter your user ID to view cart: ")

    cart = user_carts.get(user_id)
    if not cart:
        print("Your cart is empty or user ID not found.")
        return

    print(f"--- {user_id}'s Cart ---")
    total_price = 0
    for book_id, quantity in cart.items():
        book = next((b for b in books_db if b["id"] == book_id), None)
        if book:
            item_price = book["price"] * quantity
            total_price += item_price
            print(f"Title: {book['title']}, Quantity: {quantity}, Price: ${item_price:.2f}")
    print(f"Total: ${total_price:.2f}")
    print("-----------------------")

def checkout():
    """Processes the user's cart and clears it."""
    user_id = input("Enter your user ID to checkout: ")

    if user_id not in user_carts or not user_carts[user_id]:
        print("Your cart is empty.")
        return

    print(f"--- Checking out {user_id}'s Cart ---")
    total_price = 0
    for book_id, quantity in list(user_carts[user_id].items()): # Use list() to allow modification during iteration
        book = next((b for b in books_db if b["id"] == book_id), None)
        if book:
            item_price = book["price"] * quantity
            total_price += item_price
            print(f"Purchased: {book['title']} x {quantity}")
        else:
            print(f"Warning: Book with ID {book_id} not found in database, but was in cart.")
    
    print(f"Total amount: ${total_price:.2f}")
    user_carts[user_id] = {} # Clear the cart
    print("Checkout complete. Your cart has been cleared.")
    print("-----------------------")

def main():
    """Main function to run the bookstore application."""
    while True:
        print("\n--- Bookstore Menu ---")
        print("1. List Books")
        print("2. Add Book to Cart")
        print("3. View Cart")
        print("4. Checkout")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            list_books()
        elif choice == '2':
            add_book_to_cart()
        elif choice == '3':
            view_cart()
        elif choice == '4':
            checkout()
        elif choice == '5':
            print("Exiting Bookstore. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
