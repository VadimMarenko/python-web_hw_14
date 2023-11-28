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
    birthday_users = await repository_users.birthdays_per_week(db, days, skip, limit)
    if birthday_users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return birthday_users


@router.get(
    "/me/",
    response_model=UserDb,
)
async def read_users_me(current_user: Users = Depends(auth_service.get_current_user)):
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
