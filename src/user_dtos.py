from pydantic import BaseModel


class UserResponseDTO(BaseModel):
    name: str | None
    last_online: str | None
    is_banned: bool
    is_support: bool
