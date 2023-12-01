from datetime import datetime, timedelta

from libgravatar import Gravatar
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from src.database.models import Users
from src.schemas import UserModel, UserEmailModel


async def get_users(db: Session):
    """
    The get_users function returns a list of all users in the database.

    :param db: Session: Pass the database session to the function
    :return: A list of all the users in the database
    :doc-author: Trelent
    """
    users = db.query(Users).all()
    return users


async def get_user(user_id: int, db: Session):
    """
    The get_user function is used to retrieve a user from the database.
    It takes in an integer representing the id of the user and a Session object
    representing an open connection to our database. It returns either None or
    a User object.

    :param user_id: int: Specify the user_id of the user we want to retrieve
    :param db: Session: Pass the database session to the function
    :return: A user object
    :doc-author: Trelent
    """
    user = db.query(Users).filter_by(id=user_id).first()
    return user


async def create_user(body: UserModel, db: Session):
    """
    The create_user function creates a new user in the database.

    :param body: UserModel: Validate the request body against the usermodel schema
    :param db: Session: Pass the database session to the function
    :return: The user object
    :doc-author: Trelent
    """
    g = Gravatar(body.email)
    user = Users(**body.model_dump(), avatar=g.get_image())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def update_token(user: Users, refresh_token, db: Session):
    """
    The update_token function updates the refresh token for a user.

    :param user: Users: Pass in the user object
    :param refresh_token: Update the user's refresh token in the database
    :param db: Session: Commit the changes to the database
    :return: The user's refresh token
    :doc-author: Trelent
    """
    user.refresh_token = refresh_token
    db.commit()


async def update_user(body: UserModel, user_id: int, db: Session):
    """
    The update_user function updates the user's information in the database.
        Args:
            body (UserModel): The UserModel object containing all of the user's information.
            user_id (int): The id of the current logged in user.

    :param body: UserModel: Get the data from the request body
    :param user_id: int: Get the user with that id from the database
    :param db: Session: Access the database
    :return: A user object
    :doc-author: Trelent
    """
    user = db.query(Users).filter_by(id=user_id).first()
    if user:
        user.first_name = body.first_name
        user.last_name = body.last_name
        user.email = body.email
        user.phone_number = body.phone_number
        user.born_date = body.born_date
        user.description = body.description
        db.commit()
    return user


async def update_user_email(body: UserEmailModel, user_id: int, db: Session):
    """
    The update_user_email function updates the email of a user.

    :param body: UserEmailModel: Pass the data from the request body into the function
    :param user_id: int: Identify the user that is being updated
    :param db: Session: Pass the database session to the function
    :return: The user object
    :doc-author: Trelent
    """
    user = db.query(Users).filter_by(id=user_id).first()
    if user:
        user.email = body.email
        db.commit()
    return user


async def remove_user(user_id: int, db: Session):
    """
    The remove_user function removes a user from the database.

    :param user_id: int: Specify the user to be deleted
    :param db: Session: Pass the database session to the function
    :return: The user object that was deleted from the database
    :doc-author: Trelent
    """
    user = db.query(Users).filter_by(id=user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user


async def search_user(q: str, skip: int, limit: int, db: Session):
    """
    The search_user function searches for users in the database.

    :param q: str: Search for a user by first name, last name or email
    :param skip: int: Skip the first n results
    :param limit: int: Limit the number of results returned
    :param db: Session: Pass the database session to the function
    :return: A list of users
    :doc-author: Trelent
    """
    users = (
        db.query(Users)
        .query.filter(
            or_(
                Users.first_name.ilike(f"%{q}%"),
                Users.last_name.ilike(f"%{q}%"),
                Users.email.ilike(f"%{q}%"),
            )
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
    return users


async def birthdays_per_week(days: int, skip: int, limit: int, db: Session):
    """
    The birthdays_per_week function returns a list of users whose birthdays are within the next
        'days' days. The function takes three arguments:

    :param days: int: Determine how many days in the future to look for birthdays
    :param skip: int: Skip the first n records
    :param limit: int: Limit the number of users returned
    :param db: Session: Pass the database session to the function
    :return: A list of users whose birthday is within the next n days
    :doc-author: Trelent
    """
    today = datetime.now().date()
    date_to = today + timedelta(days=days)

    upcoming_birthdays_filter = (
        func.to_char(Users.born_date, "MM-DD") >= today.strftime("%m-%d")
    ) & (func.to_char(Users.born_date, "MM-DD") <= date_to.strftime("%m-%d"))

    birthday_users = (
        db.query(Users)
        .filter(upcoming_birthdays_filter)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return birthday_users


async def get_user_by_email(email: str, db: Session) -> Users | None:
    """
    The get_user_by_email function is used to retrieve a user from the database by their email address.
    It returns None if no user with that email exists.

    :param email: str: Specify the email of the user we want to get
    :param db: Session: Pass the database session to the function
    :return: The first user with the given email address
    :doc-author: Trelent
    """
    return db.query(Users).filter_by(email=email).first()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function takes an email and a database session as arguments.
    It then gets the user by their email, sets their confirmed status to True, and commits the change.

    :param email: str: Get the email of the user
    :param db: Session: Pass the database session to the function
    :return: Nothing
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> Users:
    """
    The update_avatar function takes an email and a url as arguments.
    It then uses the get_user_by_email function to find the user with that email,
    and sets their avatar property to be equal to the url argument. It then commits
    the changes made in db and returns the updated user.

    :param email: Find the user in the database
    :param url: str: Specify the type of data that is expected to be passed in
    :param db: Session: Pass a database session to the function
    :return: A user object
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
