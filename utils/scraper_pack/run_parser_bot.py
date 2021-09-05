import uuid

def run_parser_bot(link, author, current_config):
	media_data = {}
	data = current_config["parser_function"](link)
	if data:
		media_data = {
			"MediaGuid": uuid.uuid4(),
			"MediaName": "Article",
			"MediaDesc": f"Article from {author}",			
			"MediaTitle": data["title"],
			"MediaBody": data["body"],
			"MediaAuthor": author,
			"MediaUrl": link,
		}
	return media_data
