from market import app, db
from market.models import Item

def add_item(name, price, barcode, description):
    """
    Adds a new item to the database within the Flask app's application context.
    Parameters:
        name (str): The name of the item.
        price (float): The price of the item.
        barcode (str): The barcode of the item.
        description (str): A brief description of the item.
    This function creates a new `Item` object and commits it to the database.
    """
    with app.app_context():
        new_item = Item(name=name, price=price, barcode=barcode, description=description)
        db.session.add(new_item)
        db.session.commit()
        print(f"Added item: {name}")

if __name__ == "__main__":
    """
    Optional script entry point. 
    If this file is executed directly, it will add a specific item to the database.
    This is only a helper function for testing or quick database entries.
    """
    add_item("Wireless Earbuds", 150, "345678901234", "High-quality wireless earbuds with noise cancellation")
