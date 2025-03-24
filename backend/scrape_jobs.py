from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from extractor2 import process_cv

def scrape_linkedin_jobs(keywords, location="Bangladesh"):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)")
    print(keywords)
    print(location)

    driver = webdriver.Chrome(options=options)

    search_query = "+".join(keywords)
    url = f"https://www.linkedin.com/jobs/search/?keywords={search_query}&location={location}"
    driver.get(url)
    time.sleep(7)  # Increase if needed to load full content

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    print(keywords)
    print(location)


    jobs = []
    # Correct class selector for individual job cards
    for job_card in soup.find_all('div', class_='base-card'):
        title_tag = job_card.find('h3', class_='base-search-card__title')
        company_tag = job_card.find('h4', class_='base-search-card__subtitle')
        location_tag = job_card.find('span', class_='job-search-card__location')
        link_tag = job_card.find('a', class_='base-card__full-link')

        if title_tag and company_tag and link_tag:
            jobs.append({
            'title': title_tag.get_text(strip=True),
            'company': company_tag.get_text(strip=True),
            'location': location_tag.get_text(strip=True) if location_tag else "N/A",
            'link': link_tag['href'],  # ✅ Extracting job link
            'source': 'LinkedIn'
            })

    return jobs

# Example Run
if __name__ == "__main__":
    extracted_keywords = "Python, Machine Learning, Data Science".split(", ")
    job_list = scrape_linkedin_jobs(extracted_keywords)
    if not job_list:
        print("No jobs found. LinkedIn may require login or more delay.")
    for job in job_list:
        print(f"{job['title']} at {job['company']} - {job['location']}")
