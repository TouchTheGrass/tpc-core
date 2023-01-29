from dataclasses import dataclass
from ..models.enumerations.ready_status import ReadyStatus

@dataclass
class ReadyStatus:
    value: ReadyStatus
