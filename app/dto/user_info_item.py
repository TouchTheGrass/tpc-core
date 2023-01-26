from dataclasses import dataclass
from ..models.enumerations.color import Color
from ..models.enumerations.user_status import UserStatus

@dataclass
class UserInfoItem:
    id: int
    name: str
    status: UserStatus
    color: Color
