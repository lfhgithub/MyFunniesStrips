from typing import Union
from comic_scrpaer import scrape_comicskingdom, scrape_gocomics
from jinja2 import Environment, FileSystemLoader
import os
import sys
import webbrowser

file_loader: FileSystemLoader = FileSystemLoader('templates')

env = Environment(loader=file_loader)

# template_filename = 'w3css.html'
template_filename = 'w3cssil.html'  # css inline, result html works everywere
template = env.get_template(template_filename)


def main():
	comics = scrape_comicskingdom() + scrape_gocomics()

	comic_strip_html = template.render(comics=comics)
	path: Union[bytes, str] = os.path.abspath('daily_comics.html')
	url = 'file://' + path

	with open(path, 'w', closefd=True) as f:
		f.write(comic_strip_html)
	webbrowser.open(url, new=2, autoraise=True)
	sys.exit()


if __name__ == '__main__':
	main()
