from dataclasses import dataclass

@dataclass
class Company:
    url: str = ''
    name: str = ''
    webname: str = ''
    overview: str = ''
    website: str = ''
    num_employees: int = None
    six_month_growth: int = None
    industry: str = ''
    hq: str = ''
    founded: int = None
    specialties: str = ''
    about_unreachable: bool = False
    insights_unreachable: bool = False
