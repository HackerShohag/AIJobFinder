import requests
from bs4 import BeautifulSoup
import pandas as pd

from utils.db import save_to_db

# dummy scraper function
def scrape_opportunities():
    url = "https://example.com/jobs"  # Replace with actual site
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    opportunities = []
    for item in soup.find_all("div", class_="opportunity"):
        title = item.find("h2").text
        deadline = item.find("span", class_="deadline").text
        link = item.find("a")["href"]
        
        opportunities.append({"title": title, "deadline": deadline, "link": link})

    df = pd.DataFrame(opportunities)
    save_to_db(df)
    print("Data saved!")