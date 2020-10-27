from actions import LinkedinScraper
from datetime import datetime
import time
import csv
import random
import config #or config_public


if __name__ == "__main__":
    with open(config.company_url_path,"r") as csvfile:
        company_url_object = csv.reader(csvfile)
        scraper = LinkedinScraper()
        scraper.login()
        #if scraped companies exists, ask whether to overrite or start with the last company scraped...
        #ask for input of how many profiles to scrape
        #ask or add to config whether just insights or full scrape
        with open("scraped_companies.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            if config.insights_only == False:
                writer.writerow([
                    'linkedinUrl', 
                    'name', 
                    'overview', 
                    'website', 
                    'industry', 
                    'hq', 
                    'founded', 
                    'specialties', 
                    'num_employees', 
                    'six_month_growth', 
                    'twelve_month_growth', 
                    'two_year_growth', 
                    'about_unreachable', 
                    'insights_unreachable', 
                    'timestamp'
                ])
                for url_row in company_url_object:
                        about_info = scraper.get_about(url_row[0])
                        insights_info = scraper.get_insights(url_row[0])
                        writer.writerow([
                            url_row[0], 
                            about_info.name, 
                            about_info.overview, 
                            about_info.website,
                            about_info.industry, 
                            about_info.hq, 
                            about_info.founded, 
                            about_info.specialties, 
                            insights_info.num_employees, 
                            insights_info.six_month_growth, 
                            insights_info.twelve_month_growth, 
                            insights_info.two_year_growth, 
                            insights_info.about_unreachable, 
                            insights_info.insights_unreachable, 
                            datetime.now()
                        ])
            else:
                writer.writerow([
                    'linkedinUrl', 
                    'num_employees', 
                    'six_month_growth', 
                    'twelve_month_growth', 
                    'two_year_growth', 
                    'insights_unreachable', 
                    'timestamp'
                ])
                for url_row in company_url_object:
                    insights_info = scraper.get_insights(url_row[0])
                    writer.writerow([
                        url_row[0], 
                        insights_info.num_employees, 
                        insights_info.six_month_growth, 
                        insights_info.twelve_month_growth, 
                        insights_info.two_year_growth, 
                        insights_info.insights_unreachable, 
                        datetime.now()
                    ])                
            if config.randomWait == True:
                time.sleep(random.randint(1,5))
        scraper.driver.quit()

