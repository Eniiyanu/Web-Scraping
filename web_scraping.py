import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import requests

# Authorization
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    r"C:\Users\USER\Documents\Web Projects\Scraping\affable-hydra-384612-904fb3580023.json", scope)
client = gspread.authorize(creds)

# Open the Google Sheets spreadsheet
spreadsheet = client.open('Web_Scraping')

# Access the desired worksheet
worksheet = spreadsheet.sheet1

# Scraping
keywords = ['remote', 'climate', 'social impact', 'Green jobs', 'tech', 'product', 'freelance', 'contract',
            'environment', 'sustainability', 'renewable energy', 'clean energy', 'conservation', 'eco-friendly',
            'renewables', 'carbon', 'CSR', 'ethical', 'green', 'sustainable', 'innovation', 'cleantech', 'energy efficiency',
            'environmental', 'ecosystem', 'eco-conscious', 'renewable resources', 'zero waste', 'responsible', 'ethical sourcing',
            'environmental justice', 'renewable power', 'low-carbon', 'recycling', 'green living', 'green technology',
            'carbon footprint', 'social responsibility', 'fair trade', 'conservationist', 'renewable materials', 'natural resources',
            'green economy', 'sustainable development', 'renewable solutions', 'clean technology', 'environmental stewardship',
            'eco-innovation', 'low impact', 'green business', 'environmental impact', 'energy conservation', 'eco-friendly products',
            'sustainable practices', 'renewable sources', 'environmental sustainability', 'climate action', 'sustainable solutions',
            'renewable infrastructure', 'renewable initiatives', 'sustainable living', 'green initiatives', 'sustainable energy',
            'renewable sector', 'clean power', 'sustainable future', 'carbon neutral', 'green energy', 'renewable projects',
            'sustainable resources', 'climate change', 'eco-consciousness', 'sustainable development goals', 'renewable solutions',
            'developer', 'software engineer', 'web developer', 'data analyst', 'UX/UI designer', 'database administrator',
            'network administrator', 'IT manager', 'cybersecurity analyst', 'AI engineer', 'machine learning engineer',
            'front-end developer', 'back-end developer', 'full stack developer', 'mobile app developer', 'cloud architect',
            'systems analyst', 'QA engineer', 'DevOps engineer', 'blockchain developer', 'game developer', 'IT consultant',
            'data scientist', 'product manager', 'artificial intelligence', 'virtual reality', 'augmented reality',
            'big data', 'cloud computing', 'internet of things', 'cybersecurity', 'robotics', 'content marketing', 'officer','Manager', 'computer vision']

url = 'https://climatebase.org/jobs?l=&q=&p=0&remote=false'

try:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    job_listings = soup.find_all('div', class_='job-card-wrapper')
    filtered_jobs = []
    for job in job_listings:
        site = 'Climatebase'
        # Extract job title
        job_title = soup.find('div', class_='ListCard__Title-sc-1dtq0w8-4 hVVEUN list_card__title').text

# Extract job URL
        job_url = soup.find('a', class_='ListCard__ContainerLink-sc-1dtq0w8-0 jfVKDr list_card__featured list_card comp')['href']

# Extract location
        location = soup.find('div', class_='MetadataInfo__MetadataInfoStyle-hif7kv-1').text.strip()


        if job_url is not None:
            job_url = job_url['href']

            job_data = {
                'Site/Job source': site,
                'URL': job_url,
                'Location': location,
                'Job role': job_title,
            }

            if any(keyword.lower() == job_data['Job role'].lower() for keyword in keywords):
                filtered_jobs.append(job_data)

    # Print the scraped job details to the terminal
    for job in filtered_jobs:
        print(f"Site/Job source: {job['Site/Job source']}")
        print(f"URL: {job['URL']}")
        print(f"Location: {job['Location']}")
        print(f"Job role: {job['Job role']}")
        print("------------------------------------")

    # Check the length of filtered_jobs
    print(f"Total matched jobs: {len(filtered_jobs)}")

    # Update the Google Sheets
    for i, job in enumerate(filtered_jobs):
        worksheet.update_cell(i + 1, 1, job['Site/Job source'])
        worksheet.update_cell(i + 1, 2, job['URL'])
        worksheet.update_cell(i + 1, 3, job['Location'])
        worksheet.update_cell(i + 1, 4, job['Job role'])

    print("Job details scraped and updated successfully.")
except Exception as e:
    print("An error occurred:", str(e))
