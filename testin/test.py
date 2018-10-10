import newspaper

cnn_paper = newspaper.build('http://cnn.com')
cnn_paper = newspaper.build('http://cnn.com')

# once you have the urls.... use keywords to try and pick out words commonly associated with things we're interested in
keywords = ['bill', 'politics', 'house', 'senate', 'law']

# then parse and grab only urls holding information we find useful
neatArticles = []
for article in cnn_paper.articles:
	for word in keywords:
		if word in article.url:
			neatArticles.append(article.url)

# now neat articles is hopefully full of useful articles, we can go on to parse
for art in neatArticles:
	print(art)