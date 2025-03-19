import requests
from bs4 import BeautifulSoup
import pandas as pd
from db import save_to_db
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def scrape_bdjobs():
    print("Scraping BdJobs...")
    url = "https://www.bdjobs.com/jobsearch.asp"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for job_card in soup.find_all('div', class_='text-left job-title-text'):
        title = job_card.text.strip()
        link = "https://www.bdjobs.com" + job_card.find('a')['href']
        jobs.append({"title": title, "deadline": "N/A", "link": link, "source": "BdJobs"})

    return jobs

def scrape_linkedin():
    print("Scraping LinkedIn... (headless browser)")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.linkedin.com/jobs/search/?keywords=software%20engineer")
    time.sleep(5)  # Wait for dynamic content to load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    jobs = []

    for card in soup.find_all('div', class_='base-card'):
        title = card.find('h3', class_='base-search-card__title').text.strip()
        link = card.find('a', class_='base-card__full-link')['href']
        company = card.find('h4', class_='base-search-card__subtitle').text.strip()
        jobs.append({"title": f"{title} at {company}", "deadline": "N/A", "link": link, "source": "LinkedIn"})

    driver.quit()
    return jobs

def scrape_remoteok():
    print("Scraping RemoteOK...")
    url = "https://remoteok.io/remote-dev-jobs"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for job in soup.find_all('tr', class_='job'):
        title = job.find('h2').text.strip() if job.find('h2') else "N/A"
        link = "https://remoteok.io" + job['data-url']
        jobs.append({"title": title, "deadline": "N/A", "link": link, "source": "RemoteOK"})
    return jobs

def aggregate_jobs():
    print("Aggregating jobs from multiple sources...")
    all_jobs = []
    try:
        all_jobs.extend(scrape_bdjobs())
        all_jobs.extend(scrape_linkedin())
        all_jobs.extend(scrape_remoteok())
    except Exception as e:
        print(f"Error during scraping: {e}")

    df = pd.DataFrame(all_jobs)
    print(df.head())
    save_to_db(df)
    print("Data saved to DB successfully!")

if __name__ == "__main__":
    aggregate_jobs()
