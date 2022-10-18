import requests
from bs4 import BeautifulSoup

url = "https://realpython.github.io/fake-jobs/"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

card_content_tags = soup.find_all('div', class_='card-content')

print(card_content_tags)
