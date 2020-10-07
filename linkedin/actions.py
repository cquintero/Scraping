import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from objects import Company
from config import *

"""
# Project Goals: 
# Learn about OOP
# Replicate PhantomBuster functionality
- Take in a Linkedin company URL and scrape the page for: name, description, domain, location, employee count, year founded, growth rate
- Take in a Linkedin profile URL and scrape all major attributes

#Next actions
- Figure out how to sign in on Selenium and keep a persistent session
- Pull out all the relevant data and add to csv
- add toggle for headless
- Turn into a database?
- Any benefits to using beautiful soup over selenium's find elements?

"""

class LinkedinScraper:

    def __init__(self):
        self.driver = webdriver.Chrome(driver_path)
        self.driver_wait = WebDriverWait(self.driver, 10)
    
    def login(self):
        self.driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
        username = self.driver.find_element_by_name('session_key')
        username.send_keys(email)
        pw = self.driver.find_element_by_name('session_password')
        pw.send_keys(password)
        login = self.driver.find_element_by_class_name('login__form_action_container')
        login.click()

    #look at a better way to check that
    def is_loaded(self, classname):
        try:
            self.driver_wait.until(EC.visibility_of_element_located((By.CLASS_NAME, classname)))
            return True
        except:
            return False

    def get_company(self, url):
        self.driver.get(url + "/about/")
        if self.is_loaded("org-page-details__definition-term"):
            # time.sleep(5)
            try: 
                webname = self.driver.find_element_by_xpath("/html/body/div[8]/div[3]/div/div[3]/div[1]/section/div/div/div[2]/div[1]/div[1]/div[2]/div/h1/span").text
            except:
                webname = None
            try: 
                overview = self.driver.find_element_by_class_name("break-words").text
            except:
                overview = None
            try:
                website = self.driver.find_element_by_xpath("/html/body/div[8]/div[3]/div/div[3]/div[2]/div[2]/div[1]/div[1]/section/dl/dd[1]/a/span").text
            except:
                website = None
            try:
                industry = self.driver.find_element_by_xpath("/html/body/div[8]/div[3]/div/div[3]/div[2]/div[2]/div[1]/div[1]/section/dl/dd[2]").text
            except:
                industry = None
            try:
                hq = self.driver.find_element_by_xpath("/html/body/div[8]/div[3]/div/div[3]/div[2]/div[2]/div[1]/div[1]/section/dl/dd[5]").text
            except:
                hq = None
            try:
                founded = self.driver.find_element_by_xpath("/html/body/div[8]/div[3]/div/div[3]/div[2]/div[2]/div[1]/div[1]/section/dl/dd[7]").text
            except:
                founded = None
            try:
                specialties = self.driver.find_element_by_xpath("/html/body/div[8]/div[3]/div/div[3]/div[2]/div[2]/div[1]/div[1]/section/dl/dd[8]").text
            except:
                specialties = None
        #insights scrape
        self.driver.get(url + "/insights/")
        # time.sleep(5)
        if self.is_loaded("org-insights-module__summary-table"):
            try:
                num_employees = self.driver.find_element_by_xpath("/html/body/div[8]/div[3]/div/div[3]/div[2]/div[2]/section/div[1]/div/div/div[2]/div/table[1]/tr[1]/td[1]/span").text
            except:
                num_employees = None
            try:
                six_month_growth = self.driver.find_element_by_xpath("/html/body/div[8]/div[3]/div/div[3]/div[2]/div[2]/section/div[1]/div/div/div[2]/div/table[1]/tr[1]/td[2]/span/span[1]").text
            except:
                six_month_growth = None
            return Company(url=url, name=name, webname=webname, overview=overview, website=website, industry=industry, hq=hq, founded=founded, specialties=specialties, num_employees=num_employees, six_month_growth=six_month_growth, unreachable=False)
        else:
            #wait and try again?
            return Company(url=url, name=name, unreachable=True)
    def get_person(self, url):
        pass

#database file
