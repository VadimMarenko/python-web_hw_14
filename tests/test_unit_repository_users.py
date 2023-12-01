from datetime import datetime
import sys
import os

import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)


from src.database.models import Users
from src.schemas import UserModel, UserDb, UserEmailModel, UserResponse
from src.repository.users import (
    get_users,
    get_user,
    create_user,
    update_token,
    update_user,
    update_user_email,
    remove_user,
    search_user,
    birthdays_per_week,
    get_user_by_email,
    confirmed_email,
    update_avatar,
)


class TestUsers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = Users(id=1)

    async def test_get_users(self):
        users = [Users(), Users(), Users()]
        self.session.query().all.return_value = users
        result = await get_users(db=self.session)
        self.assertEqual(result, users)

    async def test_get_user_found(self):
        user = Users(id=1)
        self.session.query().filter_by(id=user.id).first.return_value = user
        result = await get_user(user_id=1, db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_not_found(self):
        self.session.query().filter_by().first.return_value = None
        result = await get_user(user_id=99, db=self.session)
        self.assertIsNone(result)

    async def test_create_user(self):
        user = Users()
        body = UserModel(
            first_name="Bill",
            last_name="Johnson",
            username="bill.johnson",
            email="bill.johnson@example.com",
            password="passwd",
            phone_number="999 999 99 99",
            born_date="2000-05-05",
            description="test",
        )
        self.session.query().filter().first.return_value = user
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.born_date, body.born_date)
        self.assertEqual(result.description, body.description)
        self.assertTrue(hasattr(result, "id"))
        self.assertTrue(hasattr(result, "created_at"))

    async def test_update_user(self):
        user = Users(
            id=1,
            first_name="Bill",
            last_name="Johnson",
            username="bill.johnson",
            email="bill.johnson@example.com",
            password="passwd",
            phone_number="999 999 99 99",
            born_date="2000-05-05",
            description="test",
        )
        body = UserModel(
            first_name="Bill",
            last_name="Johnson",
            username="bill.johnson",
            email="bill.johnson@example.com",
            password="passwd",
            phone_number="999 999 99 99",
            born_date="2000-05-05",
            description="test",
        )
        self.session.query(Users).filter_by(id=user.id).first.return_value = user
        result = await update_user(body=body, user_id=user.id, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.born_date, body.born_date)
        self.assertEqual(result.description, body.description)
        self.assertTrue(hasattr(result, "updated_at"))

    async def test_remove_user_found(self):
        user = Users()
        self.session.query().filter_by().first.return_value = user
        result = await remove_user(user_id=2, db=self.session)
        self.assertEqual(result, user)

    async def test_remove_user_not_found(self):
        self.session.query().filter_by().first.return_value = None
        result = await remove_user(user_id=99, db=self.session)
        self.assertIsNone(result)

    async def test_update_token_found(self):
        user = Users()
        old_token = "old_token"
        new_token = "new_token"
        self.session.query().filter_by().first.return_value = user
        result = await update_token(user=user, refresh_token=new_token, db=self.session)
        self.session.commit.assert_called_once()
        self.assertEqual(user.refresh_token, new_token)

    async def test_update_user_email_found(self):
        user = Users()
        new_email = "new_email@example.com"
        body = UserEmailModel(email=new_email)
        self.session.query().filter_by().first.return_value = user
        result = await update_user_email(body=body, user_id=user.id, db=self.session)
        self.session.commit.assert_called_once()
        self.assertEqual(user.email, new_email)
        self.assertEqual(result, user)

    async def test_update_user_email_not_found(self):
        user = Users()
        new_email = "new_email@example.com"
        body = UserEmailModel(email=new_email)
        self.session.query().filter_by().first.return_value = None
        result = await update_user_email(body=body, user_id=user.id, db=self.session)
        self.session.commit.assert_not_called()
        self.assertIsNone(result)

    async def test_search_user_not_found(self):
        query = "user@ex.com"
        user = Users()
        self.session.query().filter().offset().limit().all.return_value = user
        result = await search_user(q=query, skip=0, limit=10, db=self.session)
        self.assertNotEqual(result, user)

    async def test_birthdays_per_week(self):
        users = Users(born_date=datetime.now().date())
        self.session.query().filter().offset().limit().all.return_value = users
        result = await birthdays_per_week(db=self.session, days=7, skip=0, limit=10)
        self.assertEqual(result, users)

    async def test_get_user_by_email_found(self):
        user = Users(email="username@example.com")
        self.session.query().filter_by().first.return_value = user
        result = await get_user_by_email(email="username@example.com", db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_by_email_not_found(self):
        self.session.query().filter_by().first.return_value = None
        result = await get_user_by_email(email="user@example.com", db=self.session)
        self.assertIsNone(result)

    async def test_confirmed_email(self):
        email = "username@example.com"
        user = Users(email=email)
        self.session.query().filter_by().first.return_value = user
        await confirmed_email(email=email, db=self.session)
        self.assertTrue(user.confirmed)
        self.session.commit.assert_called_once()

    async def test_update_avatar(self):
        user = Users()
        url = "avatar.com"
        result = await update_avatar(user.email, url, db=self.session)
        self.assertEqual(result.avatar, url)
        self.session.commit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
