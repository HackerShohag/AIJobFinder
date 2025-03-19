import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlencode
from db import save_to_db

# Accept user input as parameters
def scrape_jobs(user_data):
    # Example: Mapping user input to a query string for job websites
    query = f"{user_data.get('study_field', '')} {user_data.get('job_role', '')} {user_data.get('skills', '')}"
    location = user_data.get('location', '')
    
    # Encode query for URLs
    query_params = urlencode({'q': query, 'l': location})
    
    # Example job sites (you need to check their actual search URL patterns)
    job_sites = [
        f"https://www.bdjobs.com/search.asp?{query_params}",
        f"https://www.linkedin.com/jobs/search/?keywords={query.replace(' ', '%20')}&location={location}"
    ]
    
    all_jobs = []

    for url in job_sites:
        try:
            print(f"Scraping: {url}")
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, "html.parser")

            # Example parsing logic (update selectors based on website structure)
            job_listings = soup.find_all("div", class_="job-card")  # Change class accordingly

            for job in job_listings:
                title_tag = job.find("h3") or job.find("h2")
                title = title_tag.text.strip() if title_tag else "N/A"

                link_tag = job.find("a", href=True)
                link = link_tag['href'] if link_tag else "N/A"

                company = job.find("h4").text.strip() if job.find("h4") else "Unknown"
                deadline_tag = job.find("span", class_="deadline")
                deadline = deadline_tag.text.strip() if deadline_tag else "N/A"

                # Optional: Score calculation based on skill match or keywords (simplified)
                relevance_score = calculate_relevance(user_data, title, company)

                all_jobs.append({
                    "title": title,
                    "company": company,
                    "link": link,
                    "deadline": deadline,
                    "source": url.split("//")[1].split("/")[0],
                    "score": relevance_score
                })
        except Exception as e:
            print(f"Failed scraping {url}: {e}")

    # Convert to DataFrame
    df = pd.DataFrame(all_jobs)
    save_to_db(df)  # Save to database (your logic)
    print("Data saved!")

    return all_jobs


def calculate_relevance(user_data, title, company):
    score = 50  # Base score
    if user_data.get('skills') and any(skill.lower() in title.lower() for skill in user_data['skills'].split(",")):
        score += 20
    if user_data.get('job_role') and user_data['job_role'].lower() in title.lower():
        score += 15
    if user_data.get('study_field') and user_data['study_field'].lower() in title.lower():
        score += 10
    return min(score, 100)
