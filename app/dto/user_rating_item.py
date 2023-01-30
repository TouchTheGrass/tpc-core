from dataclasses import dataclass


@dataclass
class UserRatingItem:
    id: int
    name: str
    scores: int
