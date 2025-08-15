# ==============================================================================
# ||                                                                          ||
# ||             SIMPLE DIGITAL BOOKSTORE SCRIPT (WITH A BUG)                 ||
# ||                                                                          ||
# ==============================================================================
#
# Description: This version contains an intentional logic error that will
#              cause the program to crash with a KeyError under a specific
#              scenario.

import traceback


# --- 1. GLOBAL DATA "DATABASE" ---
BOOK_DATABASE = [
    {
        "id": 101,
        "title": "The Hitchhiker's Guide to the Galaxy",
        "author": "Douglas Adams",
        "price": 12.50,
        "stock": 5
    },
    {
        "id": 205,
        "title": "Dune",
        "author": "Frank Herbert",
        "price": 15.75,
        "stock": 8
    },
    {
        "id": 310,
        "title": "Fahrenheit 451",
        "author": "Ray Bradbury",
        "price": 10.00,
        "stock": 10
    },
    {
        "id": 451,
        "title": "1984",
        "author": "George Orwell",
        "price": 9.25,
        "stock": 0
    },
    # !!! THIS BOOK IS DESIGNED TO CAUSE THE ERROR !!!
    # Notice it has a "format" key but is MISSING the "stock" key.
    {
        "id": 777,
        "title": "The Art of Python (Digital E-book)",
        "author": "AI Coder",
        "price": 25.00,
        "format": "digital" 
    }
]

SHOPPING_CART = []


# --- 2. CORE FUNCTIONS ---

def display_all_books():
    """
    This function loops through the BOOK_DATABASE and prints the details.
    """
    print("\n--- Available Books in Our Store ---")
    print("-" * 75)
    print(f"{'ID':<5} | {'Title':<45} | {'Author':<15} | {'Price':<7}")
    print("-" * 75)
    
    for book in BOOK_DATABASE:
        title = book["title"]
        author = book["author"]
        price_str = f"${book['price']:.2f}"
        
        # Check if the book has a 'stock' key and if it's > 0
        if 'stock' in book and book["stock"] > 0:
            print(f"{book['id']:<5} | {title:<45} | {author:<15} | {price_str:<7}")
        # Check if the book is digital
        elif 'format' in book and book['format'] == 'digital':
            print(f"{book['id']:<5} | {title:<45} | {author:<15} | {price_str:<7}")
        else:
            # Otherwise, assume it's out of stock
            print(f"{book['id']:<5} | {title:<45} | {author:<15} | {'OUT OF STOCK':<7}")
            
    print("-" * 75)


def add_book_to_cart():
    """
    This function asks the user for a book ID and adds it to the cart.
    
    !!! INTENTIONAL LOGIC ERROR IS IN THIS FUNCTION !!!
    
    THE FLAW:
    The code correctly finds the book by its ID. However, it then immediately
    tries to check `if found_book["stock"] > 0:`. This line of code ASSUMES
    that EVERY book dictionary will have a "stock" key.
    
    When the user tries to add the "Digital E-book" (ID 777), the `found_book`
    dictionary will be `{'id': 777, 'title': ..., 'format': 'digital'}`.
    When Python tries to access `found_book["stock"]`, it won't find that key,
    and the program will crash with a `KeyError`.
    """
    try:
        book_id_to_add = int(input("\nEnter the ID of the book you want to add to your cart: "))
    except ValueError:
        print("\n[!] Invalid input. Please enter a numerical ID.")
        return

    found_book = None
    for book in BOOK_DATABASE:
        if book["id"] == book_id_to_add:
            found_book = book
            break

    if found_book:
        # --- THE CRASH WILL HAPPEN ON THE NEXT LINE ---
        # The code does not check if the 'stock' key exists before using it.
        if found_book["stock"] > 0: 
            SHOPPING_CART.append(found_book["id"])
            found_book["stock"] -= 1 # This would also fail for the same reason
            print(f"\n[SUCCESS] '{found_book['title']}' has been added to your cart.")
        else:
            print(f"\n[SORRY] '{found_book['title']}' is currently out of stock.")
    else:
        print(f"\n[!] Error: No book found with ID {book_id_to_add}.")


def view_shopping_cart():
    """
    Displays the contents of the shopping cart, including the total cost.
    """
    print("\n--- Your Shopping Cart ---")
    if not SHOPPING_CART:
        print("Your shopping cart is currently empty.")
        print("-" * 28)
        return

    total_price = 0.0
    for item_id in SHOPPING_CART:
        for book in BOOK_DATABASE:
            if book["id"] == item_id:
                print(f"  - {book['title']:<40} ${book['price']:.2f}")
                total_price += book['price']
                break 

    print("-" * 28)
    print(f"Total Price: ${total_price:.2f}")
    print("-" * 28)


def checkout():
    """
    Finalizes the purchase and clears the cart.
    """
    view_shopping_cart()
    if not SHOPPING_CART:
        print("Add items to your cart before checking out.")
        return

    print("\nThank you for your purchase!")
    SHOPPING_CART.clear()
    print("Your shopping cart has been cleared.")


# --- 3. MAIN PROGRAM LOOP ---
def main():
    try:
        """Main function that runs the application loop."""

        ERROR_LOG = "/Users/apple/Desktop/GenAI Stuff/PatchIQ_AI/PatchIQAI_App/Agent Test Code/errors.log"

        print("\nWelcome to the Digital Bookstore!")
        while True:
            print("\n==================== MENU ====================")
            print("1. View all available books")
            print("2. Add a book to your shopping cart")
            print("3. View your shopping cart")
            print("4. Checkout")
            print("5. Exit the bookstore")
            print("============================================")
            
            choice = input("Please enter your choice (1-5): ")
            
            if choice == '1':
                display_all_books()
            elif choice == '2':
                add_book_to_cart()
            elif choice == '3':
                view_shopping_cart()
            elif choice == '4':
                checkout()
            elif choice == '5':
                print("\nThank you for visiting. Goodbye!\n")
                break
            else:
                print("\n[!] Invalid choice. Please enter a number from 1 to 5.")
    except Exception:
        traceback_str = traceback.format_exc()
        with open(ERROR_LOG, "w") as f:
            f.write(traceback_str)

        print("\n⚠️ Exception occurred! Error written to", ERROR_LOG)
        print("🤖 Triggering fix agent...")

        # spawn agent in same event loop
        from agent_fix_bot import fix_agent_main
        import asyncio

        result = asyncio.run(fix_agent_main())
        print("\n✅ Fix process completed. JSON summary:")
        print(result)


main()
