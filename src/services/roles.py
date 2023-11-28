from typing import Any, List

from fastapi import Depends, HTTPException, status, Request

from src.database.models import Users, Role
from src.services.auth import auth_service


class RoleAccess:
    def __init__(self, allowed_roles: List[Role]) -> None:
        self.allowed_roles = allowed_roles

    async def __call__(
        self,
        request: Request,
        curent_user: Users = Depends(auth_service.get_current_user),
    ) -> Any:
        """
        The __call__ function is a decorator that allows us to use the class as a function.
        It takes in the request and current user, then checks if the current user's role is allowed to access this endpoint.
        If not, it raises an HTTPException with status code 403 (Forbidden).


        :param self: Access the class attributes
        :param request: Request: Get the request object
        :param curent_user: Users: Get the current user from the database
        :param : Get the current user from the database
        :return: The decorated function
        :doc-author: Trelent
        """
        print(request.method, request.url)
        print(f"User role {curent_user.roles}")
        print(f"Allowed roles: {self.allowed_roles}")
        if curent_user.roles not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Operation forbidden"
            )
