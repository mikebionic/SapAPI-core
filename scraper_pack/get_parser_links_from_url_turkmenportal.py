from bs4 import BeautifulSoup
import requests

main_url = "http://127.0.0.1:8000/order/6"

def get_parser_links_from_url_turkmenportal(url = main_url):
	res = requests.get(url)
	soup = BeautifulSoup(res.text, 'html.parser')

	articles = soup.find_all('article')
	linkList = []

	for article in articles:
		current_article_soup = BeautifulSoup(str(article), 'html.parser')
		current_article_link = current_article_soup.find('a')
		if current_article_link:
			current_article_link = current_article_link.get('href')
			if current_article_link.find('http') > -1:
				linkList.append(current_article_link)

	return linkList