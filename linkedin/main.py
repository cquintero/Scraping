from actions import LinkedinScraper
from datetime import datetime
import time
import csv
import random
import config # or config_public


def urls_to_scrape():
    # Open list of urls to scrape
    with open(config.company_url_path) as company_urls:
        list_of_urls = company_urls.read().splitlines()
        # Open previously scraped data (if it exists)
        with open(config.output_file_path) as scraped_data:
            scraped_data = scraped_data.read().splitlines()
            # Assume we want to append to previous data (if it exists)
            if len(scraped_data) > 0:
                previous_company = scraped_data[-1].split(",")[0]
                previous_index = list_of_urls.index(previous_company)
                num_remaining = len(list_of_urls) - previous_index
                start_index = previous_index + 1
                if num_remaining < config.num_records_to_scrape:
                    stop_index = start_index + num_remaining
                else:
                    stop_index = start_index + config.num_records_to_scrape
                company_url_list = list_of_urls[start_index:stop_index]
            # Otherwise start from 0
            elif len(scraped_data) == 0:
                if config.num_records_to_scrape > len(list_of_urls):
                    stop_index = len(list_of_urls)
                else:
                    stop_index = config.num_records_to_scrape
                company_url_list = list_of_urls[0:stop_index]
    return company_url_list

def write_header():
    with open(config.output_file_path,"r+") as scraped_data:
        writer = csv.writer(scraped_data)
        scraped_data = scraped_data.read().splitlines()
        # If file is blank, write header
        if len(scraped_data) == 0:
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
            elif config.insights_only == True:
                writer.writerow([
                    'linkedinUrl', 
                    'num_employees', 
                    'six_month_growth', 
                    'twelve_month_growth', 
                    'two_year_growth', 
                    'insights_unreachable', 
                    'timestamp'
                ])

if __name__ == "__main__":
        company_url_list = urls_to_scrape()
        write_header()
        print(company_url_list)
        #raise SystemExit()
        scraper = LinkedinScraper()
        scraper.login()        
        # Determine which data to obtain and write
        with open(config.output_file_path,"a+") as scraped_data:
            writer = csv.writer(scraped_data)
            if config.insights_only == False:
                for url in company_url_list:
                    about_info = scraper.get_about(url)
                    insights_info = scraper.get_insights(url)
                    writer.writerow([
                        url, 
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
                    # Add delay between pageloads to avoid detection?
                    if config.randomWait == True:
                        time.sleep(random.randint(1,5))
            
            elif config.insights_only == True:
                for url in company_url_list:
                    insights_info = scraper.get_insights(url)
                    writer.writerow([
                        url, 
                        insights_info.num_employees, 
                        insights_info.six_month_growth, 
                        insights_info.twelve_month_growth, 
                        insights_info.two_year_growth, 
                        insights_info.insights_unreachable, 
                        datetime.now()
                    ]) 
                    # Add delay between pageloads to avoid detection?
                    if config.randomWait == True:
                        time.sleep(random.randint(1,5))  
        scraper.driver.quit()

