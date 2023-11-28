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
        print(request.method, request.url)
        print(f"User role {curent_user.roles}")
        print(f"Allowed roles: {self.allowed_roles}")
        if curent_user.roles not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Operation forbidden"
            )
