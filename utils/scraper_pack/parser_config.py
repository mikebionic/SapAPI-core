from .parse_article_turkmenportal import parse_article_turkmenportal
from .get_parser_links_from_url_turkmenportal import get_parser_links_from_url_turkmenportal

parser_config = [
	{
		"author": "Turkmenportal",
		"url": "https://turkmenportal.com",
		"article_links_url": "https://turkmenportal.com/blog/novosti/tehnologii",
		"parser_function": parse_article_turkmenportal,
		"get_links_function": get_parser_links_from_url_turkmenportal,
	}
]

def get_current_parser_config(author):
	current_config = {}
	for config in parser_config:
		if config["author"] == author:
			current_config = config
	
	return current_config