from main_pack import create_app
from main_pack.config import Config

app = create_app()

app_port = int(Config.APP_PORT) if Config.APP_PORT else 5000
app_host = Config.APP_HOST or "0.0.0.0"

if __name__ == "__main__":
	if Config.USE_MIDDLEWARE_PROFILER:
		from werkzeug.middleware.profiler import ProfilerMiddleware
		app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[5], profile_dir='./profile')
	app.jinja_env.cache = {}
	app.run(host=app_host, port=app_port, threaded=True)