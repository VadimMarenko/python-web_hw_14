from typing import List

import cloudinary
import cloudinary.uploader
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Path,
    Query,
    File,
    UploadFile,
)
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import Users, Role
from src.schemas import UserDb, UserModel, UserEmailModel
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.services.roles import RoleAccess
from src.conf.config import settings

# from src.services.cloud_image import CloudImage

router = APIRouter(prefix="/users", tags=["users"])

allowed_operation_get = RoleAccess([Role.admin, Role.moderator, Role.user])
# allowed_operation_create = RoleAccess([Role.admin, Role.moderator])
allowed_operation_update = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_remove = RoleAccess([Role.admin])


@router.get(
    "/",
    response_model=List[UserDb],
)
async def get_users(
    db: Session = Depends(get_db),
    curent_user: Users = Depends(auth_service.get_current_user),
):
    """
    The get_users function returns a list of users.

    :param db: Session: Pass the database connection to the function
    :param curent_user: Users: Get the current user from the database
    :return: A list of users
    :doc-author: Trelent
    """
    users = await repository_users.get_users(db)
    return users


@router.get(
    "/{user_id}",
    response_model=UserDb,
    dependencies=[Depends(allowed_operation_get)],
)
async def get_user(
    user_id: int = Path(ge=1),
    db: Session = Depends(get_db),
    curent_user: Users = Depends(auth_service.get_current_user),
):
    """
    The get_user function returns a user object with the given id.
    If the user does not exist, it raises an HTTP 404 error.

    :param user_id: int: Specify the user_id that is passed in as a path parameter
    :param db: Session: Get the database session
    :param curent_user: Users: Get the current user
    :return: The user object if it exists, otherwise raises an httpexception
    :doc-author: Trelent
    """
    user = await repository_users.get_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


@router.post(
    "/",
    response_model=UserDb,
    status_code=status.HTTP_201_CREATED,
    # dependencies=[Depends(allowed_operation_create)],
)
async def create_user(
    body: UserModel,
    db: Session = Depends(get_db),
    curent_user: Users = Depends(auth_service.get_current_user),
):
    """
    The create_user function creates a new user in the database.

    :param body: UserModel: Get the data from the request body
    :param db: Session: Pass the database session to the function
    :param curent_user: Users: Get the current user from the database
    :return: A user object
    :doc-author: Trelent
    """
    user = await repository_users.create_user(body, db)
    return user


@router.put(
    "/{user_id}",
    response_model=UserDb,
    # dependencies=[Depends(allowed_operation_update)],
    description="Only moderator and admin",
)
async def update_user(
    body: UserModel,
    user_id: int = Path(ge=1),
    db: Session = Depends(get_db),
    curent_user: Users = Depends(auth_service.get_current_user),
):
    """
    The update_user function updates a user in the database.
        The function takes an id, and a body of type UserModel.
        It returns the updated user.

    :param body: UserModel: Get the data from the request body
    :param user_id: int: Specify the path parameter
    :param db: Session: Pass the database session to the function
    :param curent_user: Users: Get the current user
    :return: The updated user
    :doc-author: Trelent
    """
    user = await repository_users.update_user(body, user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


@router.patch(
    "/{user_id}",
    response_model=UserDb,
    # dependencies=[Depends(allowed_operation_update)],
    # description="Only moderator and admin",
)
async def update_user_email(
    body: UserEmailModel,
    user_id: int = Path(ge=1),
    db: Session = Depends(get_db),
    curent_user: Users = Depends(auth_service.get_current_user),
):
    """
    The update_user_email function updates the user's email.
        Args:
            body (UserEmailModel): The new email to be updated.
            user_id (int): The id of the user whose email is being updated.

    :param body: UserEmailModel: Pass the useremailmodel object to the update_user_email function
    :param user_id: int: Get the user_id from the url
    :param db: Session: Get the database session
    :param curent_user: Users: Get the current user from the database
    :return: A usermodel object
    :doc-author: Trelent
    """
    user = await repository_users.update_user_email(body, user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(allowed_operation_remove)],
    description="Only admin",
)
async def remove_user(
    user_id: int = Path(ge=1),
    db: Session = Depends(get_db),
    curent_user: Users = Depends(auth_service.get_current_user),
):
    """
    The remove_user function removes a user from the database.
        Args:
            user_id (int): The id of the user to remove.
            db (Session, optional): An open DB session. Defaults to Depends(get_db).

    :param user_id: int: Get the user_id from the url
    :param db: Session: Pass the database connection to the function
    :param curent_user: Users: Get the current user
    :return: The removed user
    :doc-author: Trelent
    """
    user = await repository_users.remove_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


@router.get(
    "/search/",
    response_model=List[UserDb],
    dependencies=[Depends(allowed_operation_get)],
)
async def search_user(
    q: str = Query(description="Search by name, last name or email"),
    skip: int = 0,
    limit: int = Query(
        default=10,
        le=100,
        ge=10,
    ),
    db: Session = Depends(get_db),
    curent_user: Users = Depends(auth_service.get_current_user),
):
    """
    The search_user function allows you to search for users by name, last name or email.
        The function returns a list of users that match the query.

    :param q: str: Search by name, last name or email
    :param last name or email&quot;): Search by name, last name or email
    :param skip: int: Skip the first n results
    :param limit: int: Limit the number of results returned
    :param le: Limit the number of results returned by the search_user function
    :param ge: Set a minimum value for the limit parameter
    :param ): Define the number of results to return
    :param db: Session: Get the database session
    :param curent_user: Users: Get the current user
    :return: A list of users
    :doc-author: Trelent
    """
    users = await repository_users.search_user(db, q, skip, limit)
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return users


@router.get(
    "/birthdays/",
    response_model=List[UserDb],
    dependencies=[Depends(allowed_operation_get)],
)
async def birthday_users(
    days: int = Query(default=7, description="Enter the number of days"),
    skip: int = 0,
    limit: int = Query(
        default=10,
        le=100,
        ge=10,
    ),
    db: Session = Depends(get_db),
    curent_user: Users = Depends(auth_service.get_current_user),
):
    """
    The birthday_users function returns a list of users who have birthdays in the next 7 days.

    :param days: int: Get the number of days from the user
    :param description: Provide a description for the endpoint
    :param skip: int: Skip the first n users in the database
    :param limit: int: Limit the number of results returned
    :param le: Limit the number of records returned to 100
    :param ge: Set the minimum value for the limit parameter
    :param db: Session: Get the database session
    :param curent_user: Users: Get the current user from the database
    :return: A list of users that have a birthday in the next 7 days
    :doc-author: Trelent
    """
    birthday_users = await repository_users.birthdays_per_week(db, days, skip, limit)
    if birthday_users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return birthday_users


@router.get(
    "/me/",
    response_model=UserDb,
)
async def read_users_me(current_user: Users = Depends(auth_service.get_current_user)):
    """
    The read_users_me function returns the current user's information.

    :param current_user: Users: Pass the user object to the function
    :return: The current_user object, which is the user who made the request
    :doc-author: Trelent
    """
    return current_user


# @router.patch(
#     "/avatar",
#     response_model=UserDb,
#     dependencies=[Depends(allowed_operation_update)],
# )
# async def update_avatar_user(
#     file: UploadFile = File(),
#     current_user: Users = Depends(auth_service.get_current_user),
#     db: Session = Depends(get_db),
# ):
#     public_id = CloudImage.generate_name_avatar(current_user.email)
#     r = CloudImage.upload(file.file, public_id)
#     src_url = CloudImage.get_url_for_avatar(public_id, r)
#     user = await repository_users.update_avatar(current_user.email, src_url, db)
#     return user


@router.patch("/avatar/", response_model=UserDb)
async def update_avatar_user(
    file: UploadFile = File(),
    current_user: Users = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    The update_avatar_user function updates the avatar of a user.
        The function takes in an UploadFile object, which is a file that has been uploaded to the server.
        It also takes in the current_user and db objects as dependencies.

    :param file: UploadFile: Upload the file to cloudinary
    :param current_user: Users: Get the current user that is logged in
    :param db: Session: Pass the database session to the repository layer
    :return: The user object
    :doc-author: Trelent
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )

    r = cloudinary.uploader.upload(
        file.file, public_id=f"Avatars/{current_user.username}", overwrite=True
    )
    src_url = cloudinary.CloudinaryImage(f"Avatars/{current_user.username}").build_url(
        width=250, height=250, crop="fill", version=r.get("version")
    )
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user
