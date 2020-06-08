import requests
from bs4 import BeautifulSoup
from comics_name_lists import gccomic_names, ckcomic_names

GOCOMICS_BASE_URL = 'http://www.gocomics.com'
GOCOMICS_LIST_URL = 'http://www.gocomics.com/comics/a-to-z'
COMICSKINGDOM_BASE_URL = 'http://comicskingdom.com'
COMICSKINGDOM_LIST_URL = 'http://comicskingdom.com/comics'


def scrape_gocomics():
	"""Returns ocomics strips reference strips name in comics_name_lists.py for today or Sunday"""
	res = requests.get(GOCOMICS_LIST_URL)
	res.raise_for_status()
	soup = BeautifulSoup(res.text, 'lxml')
	comic_pages = [a['href'] for a in
				   soup.find_all('a', class_='gc-blended-link gc-blended-link--primary col-12 col-sm-6 col-lg-4',
								 href=True)
				   if a.text]

	# generate comic url sequenced by comic_names
	comic_view_name = []
	for y in gccomic_names:
		for x in comic_pages:
			if ('/' + y + '/') in x:
				comic_view_name.append(x)
	comic_pages = [GOCOMICS_BASE_URL + x for x in comic_view_name]
	comic_imgs = []
	for url in comic_pages:
		try:
			res = requests.get(url)
			res.raise_for_status()
		except Exception as err:
			print(err)
			continue
		print()
		print(url)
		soup = BeautifulSoup(res.text, 'lxml')
		image_url = soup.find('picture', class_='item-comic-image').img
		alt = image_url['alt'] + '| Go Comics'
		src = image_url['src']
		thiscomic = "GoComics"
		comic_imgs.append({'url': url, 'alt': alt, 'src': src, 'frmcomic': thiscomic})
	return comic_imgs


def scrape_comicskingdom():
	"""Returns comicskingdom strips reference strips name in comics_name_lists.py for today or Sunday"""
	res = requests.get(COMICSKINGDOM_LIST_URL)
	res.raise_for_status()
	soup = BeautifulSoup(res.text, 'lxml')

	""" Returns href links for comics group"""
	comic_group = soup.find("div", {"class": "links-wrapper"})
	comic_pages = [page_list.a.get("href") for page_list in comic_group.find_all(class_="comic-link mb1")]
	# print(comic_pages)

	# generate comic url sequenced by comic_names
	comic_view_name = []
	for y in ckcomic_names:
		for x in comic_pages:
			if y in x:
				comic_view_name.append(x)

	comic_pages = [COMICSKINGDOM_BASE_URL + x for x in comic_view_name]
	# print(comic_pages)
	comic_imgs = []
	for url in comic_pages:
		try:
			res = requests.get(url)
			res.raise_for_status()
		except Exception as err:
			print(err)
			continue
		print()
		print(url)
		soup = BeautifulSoup(res.text, 'lxml')

		# Find and get the print image url in byprtsrc
		byprtsrc = soup.find('img', class_='buy-print-image')['src']

		# Find and get the strip title in comic_title
		# comic_title_s = soup.find('title').text

		# Comic strip description and date
		strip_name = soup.find('slider-prints')['feature-name']
		strip_date = soup.find('slider-prints')['date']
		strip_description = strip_name + ' Comic Strip for ' + strip_date + ' | ComicsKingdom'

		alt = strip_description
		src = byprtsrc
		thiscomic = "Kingdom"
		comic_imgs.append({'url': url, 'alt': alt, 'src': src, 'frmcomic': thiscomic})
	# print(comic_imgs)

	# Allow time between url requests
	# time.sleep(comic_req_url.elapsed.total_seconds())

	return comic_imgs


def main():
	days_from_today = 0
	# comics = scrape_gocomics()
	comics = scrape_comicskingdom()
	# comics = scrape_comicskingdom() + scrape_gocomics()
	print(comics)


if __name__ == '__main__':
	main()
