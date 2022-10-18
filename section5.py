import requests
from bs4 import BeautifulSoup

url = "https://realpython.github.io/fake-jobs/"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

jobs = []

card_content_tags = soup.find_all('div', class_='card-content')

for job in card_content_tags:
  job_title = job.find('h2')
  if job_title:
    job_title = job_title.text.strip()
  
  company = job.find('h3', class_='company')
  if company:
    company = company.text.strip()

  location = job.find('p', class_='location')
  if location:
    location_parts = location.text.strip().split(', ')
    city = location_parts[0]
    state = location_parts[1]
    location = location.text.strip()

  date = job.find('time')
  if date:
    date = date.text.strip()

  footer = job.find('footer')
  links = footer.find_all('a')

  link_href = ''
  for link in links:
    if link.text == 'Apply':
      link_href = link['href']

  jobs.append({
    "title":job_title,
    "company":company,
    "city":city,
    "state":state,
    "date_posted":date,
    "apply_link":link_href
  })

for job in jobs:    
  print(job)
  
