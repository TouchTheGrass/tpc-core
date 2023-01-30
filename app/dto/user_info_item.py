from dataclasses import dataclass


@dataclass
class UserInfoItem:
    id: int
    name: str
    status: str
    rating: int
    color: str
