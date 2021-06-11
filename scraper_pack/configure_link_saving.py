
from scraper_pack.parser_config import get_current_parser_config
from scraper_pack.run_parser_bot import run_parser_bot

from main_pack import db
from main_pack.models import Media

def configure_link_saving(link_list, author=None):
	for link in link_list:
		filtering = {
			"MediaUrl": link,
			"GCRecord": None,
		}
		if author:
			filtering["MediaAuthor"] = author

		current_article = Media.query.filter_by(**filtering).first()
		if not current_article:
			# print(f"no article for {author} | link {link}")
			current_config = get_current_parser_config(author)
			media_data = run_parser_bot(link, author, current_config)
			# print('-----------')
			# print(media_data)
			new_media = Media(**media_data)
			db.session.add(new_media)

	db.session.commit()





