import unittest
import sqlite3
import os
from backend.services.src.implementation.Database_Impl import add_user, add_post, get_latest_post, create_tables
import backend.services.src.implementation.Database_Impl as database
from backend.services.src.entity.User import User
from backend.services.src.entity.Post import Post


class TestDatabase(unittest.TestCase):
    test_db_path = '../../database/test_social_media.db'

    @classmethod
    def setUpClass(cls):
        # Set the database path in database module to the test database
        database.DB_PATH = cls.test_db_path
        database.create_tables()
    def setUp(self):
        # Verwenden einer separaten Testdatenbank
        self.conn = sqlite3.connect(self.test_db_path)
        create_tables()
        self.conn.commit()

    def tearDown(self):
        # Schließen der Verbindung und Löschen der Testdatenbank
        self.conn.close()
        os.remove(self.test_db_path)

    def test_add_user(self):
        # Test zum Hinzufügen eines Benutzers
        user = User(username="TestUser", email="test@example.com")
        user = add_user(user)
        self.assertIsNotNone(user.id)
        c = self.conn.cursor()
        c.execute("SELECT * FROM users WHERE id = ?", (user.id,))
        fetched_user = c.fetchone()
        self.assertIsNotNone(fetched_user)
        self.assertEqual(fetched_user[1], "TestUser")

    def test_add_post(self):
        # Test zum Hinzufügen eines Beitrags
        user = User(username="TestUser", email="test@example.com")
        user = add_user(user)
        post = Post(image="test_image.jpg", text="Test text", user_id=user.id)
        add_post(post)
        c = self.conn.cursor()
        c.execute("SELECT * FROM posts WHERE user_id = ?", (user.id,))
        fetched_post = c.fetchone()
        self.assertIsNotNone(fetched_post)
        self.assertEqual(fetched_post[1], "test_image.jpg")

    def test_get_latest_post(self):
        # Test für das Abrufen des neuesten Beitrags
        user = User(username="TestUser", email="test@example.com")
        user = add_user(user)
        post1 = Post(image="test_image1.jpg", text="Test text 1", user_id=user.id)
        add_post(post1)
        post2 = Post(image="test_image2.jpg", text="Test text 2", user_id=user.id)
        add_post(post2)
        latest_post, latest_user = get_latest_post()
        self.assertIsNotNone(latest_post)
        self.assertEqual(latest_post.image, "test_image2.jpg")
        self.assertEqual(latest_user.username, "TestUser")


if __name__ == '__main__':
    unittest.main()
