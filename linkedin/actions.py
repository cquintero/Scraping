import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from objects import Company
import config #or config_public 

"""
#Next actions
-Add Search scraping
-Add profile scraping
-Create list of tech companies in the US to monitor for hiring trends? From the Crunchbase database?
-Figure out how to do persistent cookies / sessions with specific users?
-Add proxy / user agent support / change viewport / navigator.plugins  https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec/53040904#53040904


#Open Questions
- How much rate limiting to implement / how many profiles or companies to scrape each day? 
- Better to create a few LI profiles and use phantombuster or use proxies / multilogin / 
"""

class LinkedinScraper:

    def __init__(self):
        self.options = Options()
        self.options.headless = config.headless
        self.options.add_argument(f'user-agent={config.user_agent}')
        self.driver = webdriver.Chrome(config.driver_path, chrome_options=self.options)
        

    
    def login(self):
        self.driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
        username = self.driver.find_element_by_name('session_key')
        username.send_keys(config.email)
        pw = self.driver.find_element_by_name('session_password')
        pw.send_keys(config.password)
        login = self.driver.find_element_by_class_name('login__form_action_container')
        login.click()

    def is_loaded(self, classname):
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, classname)))
            return True
        except:
            print('Timeout or element not located')
            raise

    def get_about(self, url):
        #about page scrape
        self.driver.get(url + "about/")
        if self.is_loaded("org-page-details__definition-term"):
            try: 
                name = self.driver.find_element_by_xpath('//span[@dir="ltr"]').text.strip()
            except:
                name = None
            try: 
                overview = self.driver.find_element_by_class_name("break-words").text
            except:
                overview = None
            try:
                website = self.driver.find_element_by_xpath("//dd[1]/a/span").text
            except:
                website = None
            try:
                dl = self.driver.find_element_by_xpath("//dl")
                children = dl.find_elements_by_xpath("./child::*")
                topic = None
                descript_dict = {}
                for i in children:
                    if i.tag_name == 'dt':
                        key = i.text
                    elif i.tag_name == 'dd':
                        if topic in descript_dict:
                            value = descript_dict[key] + " " + i.text
                        else:
                            value = i.text
                        descript_dict[key] = value
                if 'Industry' in descript_dict.keys():
                    industry = descript_dict['Industry']
                if 'Headquarters' in descript_dict.keys():
                    hq = descript_dict['Headquarters']
                if 'Founded' in descript_dict.keys():
                    founded = descript_dict['Founded']
                if 'Specialties' in descript_dict.keys():
                    specialties = descript_dict['Specialties']
            except:
                raise 
                industry = hq = founded = specialties = dt_elements = None
            about_unreachable = False
        else:
            about_unreachable = True
        return Company(
            name=name, 
            overview=overview, 
            website=website, 
            hq=hq, 
            industry=industry, 
            founded=founded, 
            specialties=specialties,
            about_unreachable=about_unreachable
        )

        #insights page scrape
    def get_insights(self, url):
        self.driver.get(url + "insights/")
        if self.is_loaded("org-insights-module__summary-table"):
            try:
                num_employees = int(self.driver.find_element_by_xpath("//td[@headers='org-insights-module__a11y-summary-total']/span").text.replace(',','').replace(' ',''))
            except:
                num_employees = None
            try:
                six_month_growth = int(self.driver.find_element_by_xpath("//td[@headers='org-insights-module__a11y-summary-6']/span/span").text.replace(',','').replace(' ','').replace('%',''))/100
            except:
                six_month_growth = None
            try:
                twelve_month_growth = int(self.driver.find_element_by_xpath("//td[@headers='org-insights-module__a11y-summary-12']/span/span").text.replace(',','').replace(' ','').replace('%',''))/100
            except:
                twelve_month_growth = None
            try:
                two_year_growth = int(self.driver.find_element_by_xpath("//td[@headers='org-insights-module__a11y-summary-24']/span/span").text.replace(',','').replace(' ','').replace('%',''))/100
            except:
                two_year_growth = None
            try:
                job_openings = int(self.driver.find_element_by_css_selector("#highcharts-1ogi98k-91 > svg > text.highcharts-title > tspan").text)
            except:
                job_openings = None
            insights_unreachable = False
        else:
            insights_unreachable = True 
        return Company(
            num_employees=num_employees, 
            six_month_growth=six_month_growth, 
            twelve_month_growth=twelve_month_growth, 
            two_year_growth=two_year_growth, 
            job_openings=job_openings, 
            insights_unreachable=insights_unreachable
        )

    def get_person(self, url):
        pass

