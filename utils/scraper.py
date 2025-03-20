import requests
from bs4 import BeautifulSoup
import pandas as pd
from utils.db import save_to_db
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def scrape_bdjobs(user_data):
    print("Scraping BdJobs...")
    url = "https://www.bdjobs.com/jobsearch.asp"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for job_card in soup.find_all('div', class_='job-row'):
        title = job_card.find('div', class_='text-left job-title-text').text.strip()
        link = "https://www.bdjobs.com" + job_card.find('a')['href']
        
        # Extract company name
        company_tag = job_card.find('div', class_='company-name-text')
        company = company_tag.text.strip() if company_tag else "Unknown"

        # Extract job type
        job_type_tag = job_card.find('div', class_='job-nature-text')
        job_type = job_type_tag.text.strip() if job_type_tag else "N/A"

        # Extract location
        location_tag = job_card.find('div', class_='job-location-text')
        location = location_tag.text.strip() if location_tag else "N/A"

        relevance_score = calculate_relevance(user_data, title, company)
        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "job_type": job_type,
            "link": link,
            "deadline": "N/A",
            "source": "BdJobs",
            "score": relevance_score
        })
    return jobs

def scrape_linkedin(user_data):
    print("Scraping LinkedIn... (requests)")
    job_type = user_data.get('job_type', '')
    job_type_param = ''
    if job_type.lower() == 'full-time':
        job_type_param = '&f_TP=1'
    elif job_type.lower() == 'remote':
        job_type_param = '&f_T=1'

    url = f"https://www.linkedin.com/jobs/search/?keywords={user_data['study_field']}&location={user_data['location']}{job_type_param}"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []

    for card in soup.find_all('div', class_='base-card'):
        title = card.find('h3', class_='base-search-card__title').text.strip()
        link = card.find('a', class_='base-card__full-link')['href']
        
        # Extract company name
        company = card.find('h4', class_='base-search-card__subtitle').text.strip()

        # Extract location
        location_tag = card.find('span', class_='job-search-card__location')
        location = location_tag.text.strip() if location_tag else "N/A"

        # Adjust location if it does not match user preference
        preferred_location = user_data.get("location", "")
        if preferred_location and location != preferred_location:
            location = preferred_location  # Override location if it's different

        # Extract job type
        job_type_tag = card.find('span', class_='job-result-card__employment-type')
        job_type = job_type_tag.text.strip() if job_type_tag else "N/A"

        relevance_score = calculate_relevance(user_data, title, company)
        jobs.append({
            "title": f"{title} at {company}",
            "company": company,
            "location": location,  # Modified location
            "job_type": job_type,
            "link": link,
            "deadline": "N/A",
            "source": "LinkedIn",
            "score": relevance_score
        })

    return jobs

def scrape_remoteok(user_data):
    print("Scraping RemoteOK...")
    url = "https://remoteok.io/remote-dev-jobs"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for job in soup.find_all('tr', class_='job'):
        title = job.find('h2').text.strip() if job.find('h2') else "N/A"
        link = "https://remoteok.io" + job['data-url']

        # Extract company name
        company_tag = job.find('h3', class_='company')
        company = company_tag.text.strip() if company_tag else "Unknown"

        # Extract location (if available)
        location_tag = job.find('div', class_='location')
        location = location_tag.text.strip() if location_tag else "Remote"  # Default to remote

        # Extract job type
        tags = job.find_all('div', class_='tag')
        job_types = [tag.text.strip() for tag in tags if tag.text.strip()]
        job_type = ', '.join(job_types) if job_types else "N/A"

        relevance_score = calculate_relevance(user_data, title, company)
        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "job_type": job_type,
            "link": link,
            "deadline": "N/A",
            "source": "RemoteOK",
            "score": relevance_score
        })
    return jobs

def calculate_relevance(user_data, title, company):
    score = 50  # Base score
    if user_data.get('skills') and any(skill.lower() in title.lower() for skill in user_data['skills'].split(",")):
        score += 20
    if user_data.get('job_role') and user_data['job_role'].lower() in title.lower():
        score += 15
    if user_data.get('study_field') and user_data['study_field'].lower() in title.lower():
        score += 10
    return min(score, 100)

def aggregate_jobs(user_data):
    print("Aggregating jobs from multiple sources...")
    all_jobs = []
    try:
        all_jobs.extend(scrape_bdjobs(user_data))
        all_jobs.extend(scrape_linkedin(user_data))
        all_jobs.extend(scrape_remoteok(user_data))
    except Exception as e:
        print(f"Error during scraping: {e}")

    df = pd.DataFrame(all_jobs)

    save_to_db(df)
    print("Data saved to DB successfully!")

if __name__ == "__main__":
    user_data = {
        "study_field": "Computer Science",
        "job_role": "Software Engineer",
        "skills": "Python, Java, SQL",
        "location": "Dhaka"
    }
    aggregate_jobs(user_data)