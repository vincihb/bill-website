import requests
# sources = ['bbc-news', 'cbc-news', 'politico']

headers = {'Authorization': '127ae28c3362490c94e16d337a103f70'}

res = []

# for src in sources:
# print(src + ':')
d = requests.get('https://newsapi.org/v2/everything?domains=cnn.com&language=en', headers=headers)

js = d.json()
for article in js['articles']:
	res.append(article['url'])
	print(article['url'])
	print(article['title'])

