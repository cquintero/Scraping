from actions import LinkedinScraper
import time
import csv
from config import company_url_path #or config_public

if __name__ == "__main__":
    with open(company_url_path,"r") as csvfile:
        company_url_list = csv.reader(csvfile)
        scraper = LinkedinScraper()
        scraper.login()
        with open("scraped_companies.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            for url in company_url_list:
                scraped_info = scraper.get_company(url[0])
                print(scraped_info.url, scraped_info.num_employees, scraped_info.about_unreachable, scraped_info.overview)
                writer.writerow([scraped_info.url, scraped_info.about_unreachable, scraped_info.insights_unreachable])
        scraper.driver.quit()


    # Consider saving as excel even thought it will take awhile?? Or Json? Or pickle and in/out in pandas?