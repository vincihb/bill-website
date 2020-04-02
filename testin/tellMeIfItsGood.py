import requests
from tool.Pickler import Pickler
import datetime

# our final list
finalList = []
tmpDict = {}

# label mapping
lblMap = ['not helpful', 'helpful']

# first grab like a billion results
for i in range(1, 2):
	headers = {'Authorization': '127ae28c3362490c94e16d337a103f70'}
	res = requests.get('https://newsapi.org/v2/everything?domains=cnn.com&language=en&page=' + str(i), headers=headers).json()

	for article in res['articles']:
		tmpDict[article['url']] = article['title']

# now let's walk through our massive list with a user
print("Do these titles seem relevant?")
for it in tmpDict:
	print(tmpDict[it])
	helpful = input('y/n? :')
	if helpful == 'y':
		finalList.append({'url':it, 'label': 1})

print('The final list is:')
for it in finalList:
	print(it)

Pickler.save_obj(finalList, 'training set' + str(datetime.datetime))

