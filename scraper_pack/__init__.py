from scraper_pack.configure_link_saving import configure_link_saving
from scraper_pack.parser_config import parser_config

def main_parser():
	for config in parser_config:
		links_list = config["get_links_function"](config["article_links_url"])
		print(links_list)
		configure_link_saving(links_list, config["author"])
	print("parser done")