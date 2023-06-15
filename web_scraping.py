import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import requests
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\USER\Documents\Web Projects\Scraping\affable-hydra-384612-904fb3580023.json",scope)
client = gspread.authorize(creds)


# Open the Google Sheets spreadsheet
spreadsheet = client.open('Web_Scraping')

# Access the desired worksheet
worksheet = spreadsheet.sheet1

#Scraping
keywords = ['freelance', 'climate']
url = 'https://jobs.ffwd.org/jobs'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

job_listings = soup.find_all('div', class_='job-listing')
filtered_jobs = []
for job in job_listings:
    job_title = job.find('h2').text
    if any(keyword in job_title.lower() for keyword in keywords):
        filtered_jobs.append(job_title)
for i, job in enumerate(filtered_jobs):
    sheet.update_cell(i+1, 1, job)

