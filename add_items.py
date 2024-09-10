from market import app, db
from market.models import Item

def add_item(name, price, barcode, description):
    with app.app_context():
        new_item = Item(name=name, price=price, barcode=barcode, description=description)
        db.session.add(new_item)
        db.session.commit()
        print(f"Added item: {name}")

if __name__ == "__main__":
    add_item("Wireless Earbuds", 150, "345678901234", "High-quality wireless earbuds with noise cancellation")
