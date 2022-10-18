import requests
from bs4 import BeautifulSoup
from os.path import exists
import time
import random

def randsleep(min_seconds, max_seconds):
  sleep_time = random.randint(min_seconds, max_seconds)
  time.sleep(sleep_time)

production = False

if not exists("fake-jobs.html") or production == True:
  print("Requesting URL...")
  url = "https://realpython.github.io/fake-jobs/"
  page = requests.get(url)
  page_content = page.content
  with open('fake-jobs.html', 'w') as outfile:
    outfile.write(page.content.decode())
else:
  print("Reading file...")
  with open('fake-jobs.html', 'r') as infile:
    page = infile.read()
    page_content = page.encode('utf-8')

soup = BeautifulSoup(page_content, "html.parser")

jobs = []

h2_titles = soup.find_all('h2', string=lambda text: "python" in text.lower())

for h2_tag in h2_titles:
  job = h2_tag.parent.parent.parent

  job_title = h2_tag.text

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
  
  print("Loading subpages...", end='')
  for job in jobs:
    url = job['apply_link']
    if not url:
      continue
    randsleep(2,7)
    print('.', end='')
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    content_div = soup.find('div', class_='content')

    description_tag = content_div.find('p')
    if not description_tag:
      continue
    description = description_tag.text.strip()

    job['description'] = description
    
    print()
print(f"{job['title']}\n{job['company']} -- {job['city']}, {job['state']}\n{job['description']}\n{job['date_posted']}\nApply Here: {job['apply_link']}\n")
