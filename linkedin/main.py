from actions import LinkedinScraper
import time

if __name__ == "__main__":
    scraper = LinkedinScraper()
    companies = ['https://www.linkedin.com/company/andela/', 'https://www.linkedin.com/company/recurse-center/']
    scraper.login()
    for company in companies:
        print(scraper.get_company(company))
    scraper.driver.quit()