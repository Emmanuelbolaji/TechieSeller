import unittest
from market import app, db
from market.models import User, Item
from sqlalchemy.exc import IntegrityError

class TestUserModel(unittest.TestCase):
    """
    Test case class for the User model.
    Contains tests to ensure the functionality of creating, managing, and verifying users in the database.
    """
    def setUp(self):
        """
        Set up a temporary test environment.
        This method is executed before each test method to create a new SQLite database for testing purposes.
        """
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """
        Tear down the test environment.
        This method is executed after each test method to remove the database and clear the session.
        """
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        """
        Test user creation.
        Ensure that a new user can be successfully added to the database.
        """
        user = User(username="testuser", email_address="test@example.com", password="password")
        user.save()
        self.assertIsNotNone(User.query.filter_by(username="testuser").first())

    def test_duplicate_user(self):
        """
        Test that creating a user with a duplicate username or email raises an error.
        Ensure that the system enforces unique constraints on the username and email fields.
        """
        user1 = User(username="testuser", email_address="test@example.com", password="password")
        user1.save()
        user2 = User(username="testuser", email_address="test@example.com", password="password")
        with self.assertRaises(ValueError):
            user2.save()

    def test_password_setter(self):
        """
        Test password hashing functionality.
        Ensure that the password is stored as a hash, not in plain text.
        """
        user = User(username="testuser", email_address="test@example.com", password="password")
        self.assertNotEqual(user.password_hash, "password")

    def test_check_password(self):
        """
        Test password verification.
        Ensure that the correct password is validated, and incorrect passwords are rejected.
        """
        user = User(username="testuser", email_address="test@example.com", password="password")
        self.assertTrue(user.check_password_correction("password"))
        self.assertFalse(user.check_password_correction("wrongpassword"))

    def test_invalid_password(self):
        """
        Test that setting an invalid password raises an error.
        Ensure the system rejects passwords that do not meet security standards (e.g., too short).
        """
        with self.assertRaises(ValueError):
            user = User(username="testuser", email_address="test@example.com", password="short")

    
class TestItemModel(unittest.TestCase):
    """
    Test case class for the Item model.
    Contains tests to ensure the functionality of creating and managing items in the database.
    """
    def setUp(self):
        """
        Set up a temporary test environment.
        This method is executed before each test method to create a new SQLite database for testing purposes.
        """
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """
        Tear down the test environment.
        This method is executed after each test method to remove the database and clear the session.
        """
        db.session.remove()
        db.drop_all()

    def test_create_item(self):
        """
        Test item creation.
        Ensure that a new item can be successfully added to the database.
        """
        item = Item(name="TestItem", price=100, barcode="123456789012", description="Test description")
        item.save()
        self.assertIsNotNone(Item.query.filter_by(name="TestItem").first())

    def test_duplicate_item(self):
        """
        Test that creating an item with a duplicate name or barcode raises an error.
        Ensure that the system enforces unique constraints on these fields.
        """
        item1 = Item(name="TestItem", price=100, barcode="123456789012", description="Test description")
        item1.save()
        item2 = Item(name="TestItem", price=100, barcode="123456789013", description="Another description")
        with self.assertRaises(ValueError):
            item2.save()

    def test_item_representation(self):
        """
        Test the string representation of an item.
        Ensure that calling str() on an item object returns a meaningful description.
        """
        item = Item(name="TestItem", price=100, barcode="123456789012", description="Test description")
        self.assertEqual(str(item), "Item TestItem")


if __name__ == "__main__":
    unittest.main()
