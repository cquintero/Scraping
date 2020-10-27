from dataclasses import dataclass

@dataclass
class Company:
    url: str = ''
    name: str = ''
    webname: str = ''
    overview: str = ''
    website: str = ''
    industry: str = ''
    hq: str = ''
    founded: int = None
    specialties: str = ''
    num_employees: int = None
    six_month_growth: int = None
    twelve_month_growth: int = None
    two_year_growth: int = None
    job_openings: int = None
    about_unreachable: bool = False
    insights_unreachable: bool = False


@dataclass
class Person:
    url: str ''