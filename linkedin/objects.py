from dataclasses import dataclass

@dataclass
class Company:
    url: str
    name: str = None
    webname: str = None
    overview: str = None
    website: str = None
    num_employees: str = None
    six_month_growth: str = None
    unreachable: bool = True
    industry: str = None
    hq: str = None
    founded: str = None
    specialties: str = None
