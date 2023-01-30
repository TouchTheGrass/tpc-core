import typing
from dataclasses import dataclass

from app.dto.user_rating_item import UserRatingItem


@dataclass
class UserRatingList:
    list: typing.List[UserRatingItem]
