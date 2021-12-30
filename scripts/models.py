from dataclasses import dataclass


@dataclass
class DailyData:
        date: str
        active: str
        casesSymptomatic: str
        contacts: str
        hospitalCases:str
        dayOfWeek: int

@dataclass
class VaccineDailyData:
        date: str
        total: str
        first: str
        second: str
        booster:str