from bs4 import BeautifulSoup
import requests

def parse_article_turkmenportal(url):

	data = {}

	try:
		res = requests.get(url)
		soup = BeautifulSoup(res.text, 'html.parser')

		title = soup.find('h1')
		if not title:
			raise Exception

		title = title.text.strip()

		div_elements = soup.find_all('div')
		body = ''
		for div_element in div_elements:
			divWithClass = div_element.get('class')
			if divWithClass:
				if divWithClass[0] == "article_text":
					body = div_element.text

		if not body:
			raise Exception

		body = body.strip()
		data = {
			"title": title,
			"body": body
		}

	except Exception as e:
		print(e)

	return data