import unittest
from market import app, db
from market.models import User, Item
from sqlalchemy.exc import IntegrityError

class TestUserModel(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        user = User(username="testuser", email_address="test@example.com", password="password")
        user.save()
        self.assertIsNotNone(User.query.filter_by(username="testuser").first())

    def test_duplicate_user(self):
        user1 = User(username="testuser", email_address="test@example.com", password="password")
        user1.save()
        user2 = User(username="testuser", email_address="test@example.com", password="password")
        with self.assertRaises(ValueError):
            user2.save()

    def test_password_setter(self):
        user = User(username="testuser", email_address="test@example.com", password="password")
        self.assertNotEqual(user.password_hash, "password")

    def test_check_password(self):
        user = User(username="testuser", email_address="test@example.com", password="password")
        self.assertTrue(user.check_password_correction("password"))
        self.assertFalse(user.check_password_correction("wrongpassword"))

    def test_invalid_password(self):
        with self.assertRaises(ValueError):
            user = User(username="testuser", email_address="test@example.com", password="short")

    
class TestItemModel(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_item(self):
        item = Item(name="TestItem", price=100, barcode="123456789012", description="Test description")
        item.save()
        self.assertIsNotNone(Item.query.filter_by(name="TestItem").first())

    def test_duplicate_item(self):
        item1 = Item(name="TestItem", price=100, barcode="123456789012", description="Test description")
        item1.save()
        item2 = Item(name="TestItem", price=100, barcode="123456789013", description="Another description")
        with self.assertRaises(ValueError):
            item2.save()

    def test_item_representation(self):
        item = Item(name="TestItem", price=100, barcode="123456789012", description="Test description")
        self.assertEqual(str(item), "Item TestItem")


if __name__ == "__main__":
    unittest.main()
