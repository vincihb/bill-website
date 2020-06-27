from bs4 import BeautifulSoup
from db.legacy.CongressionalSession import CongressCache
import requests
import json


def get_missing_img(first, last):
	# first check if we've already cached the result to be kind to others
	cache = get_cached_photo_url(first_name=first, last_name=last)
	if cache.available():
		return cache.get_json()

	# see if we can retrieve a photo from the bioguide
	b_url = get_bioguide_url(first=first, last=last)
	if b_url != '':
		return b_url

	# if we get here, google doesn't have it and the congressional api doesn't have it... sooo wikipedia?
	f_url = get_wiki_photo(first, last)
	if f_url != '':
		return f_url

	# if we still can't find anything... the internet is too hard
	return ''  # couldn't find an image!! :(


def get_cached_photo_url(first_name, last_name):
	return CongressCache(first_name=first_name, last_name=last_name)


def cache_photo_url(url, first_name, last_name):
	return CongressCache(first_name=first_name, last_name=last_name, photo_url=url)


# pulls down image urls from bioguide.congress.gov if google civic is too lazy to
def get_bioguide_url(first, last, last_name_only=False):
	url = ''
	if last_name_only:
		data_string = 'lastname=' + last
	else:
		data_string = 'lastname=' + last + '&firstname=' + first

	headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': str(len(data_string))}
	html = requests.post('http://bioguide.congress.gov/biosearch/biosearch1.asp', headers=headers, data=data_string)
	soup = BeautifulSoup(html.content, 'html.parser')
	links = soup.find_all('a')

	if len(links) > 1:
		html2 = requests.get(links[0].get())
		soup2 = BeautifulSoup(html2.content, 'html.parser')
		imgs = soup2.find_all('img')

		if len(imgs) > 1:
			url = 'http:' + imgs[1].get()  # must append the http: to retrieved urls from this source
			cache = cache_photo_url(url, first, last)
			return cache.get_json()

	# if we don't get a url with the given name try again with just the last name
	# (helpful in cases where google civic gives nicknames instead of legal names)
	if not last_name_only and url == '':
		return get_bioguide_url(first, last, last_name_only=True)

	return url


# gets a photo from Wikipedia using their API
def get_wiki_photo(first, last):
	get_url = 'https://en.wikipedia.org/w/api.php?action=query&titles=' + first + '_' + last + \
			'&prop=images&imlimit=20&format=json'
	html = requests.get(get_url)

	wiki_json = json.loads(html.content)
	if "-1" not in wiki_json['query']['pages']:
		file = get_most_relevant_file_name(wiki_json['query']['pages'], first, last)
		url = 'https://commons.wikimedia.org/wiki/' + file
		html = requests.get(url)
		soupy = BeautifulSoup(html.content, 'html.parser')
		imgs = soupy.find_all('img')
		if len(imgs) > 1:
			url = imgs[0].get()
			cache = cache_photo_url(url, first, last)
			return cache.get_json()

	return ''  # our last ditch attempt has failed, I hate you internet, I quit


def get_most_relevant_file_name(pages, first, last):
	relevant_title = ''
	best_relevance = 0

	for key in pages:
		images = pages[key]['images']
		for image in images:
			current_relevance = 0
			current_title = image['title']

			if first in current_title:
				current_relevance += 1

			if last in current_title:
				current_relevance += 1

			if (first + ' ' + last) in current_title:  # give highest precedence to something that has both names in order
				current_relevance += 2

			if current_relevance > best_relevance:
				best_relevance = current_relevance
				relevant_title = current_title

		break  # we only want to do the first (most relevant) key/page the API returns

	return relevant_title
