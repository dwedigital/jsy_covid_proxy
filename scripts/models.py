from dataclasses import dataclass


@dataclass
class DailyData:
        date: str
        active: str
        casesSymptomatic: str
        contacts: str
        dayOfWeek: int

