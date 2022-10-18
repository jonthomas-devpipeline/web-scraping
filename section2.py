import requests
from bs4 import BeautifulSoup

url = "https://realpython.github.io/fake-jobs/"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

job_titles = soup.find_all('h2')

for job_title in job_titles:
  print(job_title.text)
