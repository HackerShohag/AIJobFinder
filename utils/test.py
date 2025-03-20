from utils.model import match_opportunities
from utils.scraper import scrape_opportunities

def get_user_profile():
    print("Welcome! Let's gather your academic details.")

    name = input("Enter your name: ")
    study_field = input("What is your field of study? ")
    research_interests = input("What are your research interests? ")
    extracurriculars = input("Any extracurricular activities? ")
    
    user_data = {
        "name": name,
        "study_field": study_field,
        "research_interests": research_interests,
        "extracurriculars": extracurriculars
    }

    return user_data


if __name__ == "__main__":
    # run the scraper periodically to get the latest opportunities
    scrape_opportunities()

    user_profile = get_user_profile()
    print("Profile Saved:", user_profile)

    match_opportunities(user_profile)