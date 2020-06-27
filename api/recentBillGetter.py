import requests
import json
from db.legacy.BillManager import BillManager

b_manager = BillManager()


def get_recent_bills():
	header = {'X-API-Key': '7vbxYrafGzoLQb6IJtaubinW3pHhmv2EImvro1g3'}

	response = requests.get('https://api.propublica.org/congress/v1/115/house/bills/active.json', headers=header)
	if response.status_code != 200:
		return

	js = json.loads(response.content)
	print(js)
	for bill in js['results'][0]['bills']:
		bill_item = b_manager.get_bill_from_propublica_data(bill)
		b_manager.insert_bill(bill_item)


""" Returns the congress number that should be used in requests made to Probublica """


def test_propublica_congress_number(current_congress: int):
	header = {'X-API-Key': '7vbxYrafGzoLQb6IJtaubinW3pHhmv2EImvro1g3'}
	response = requests.get(
		'https://api.propublica.org/congress/v1/' + str(current_congress) + '/house/bills/active.json', headers=header)

	if response.status_code == 200:
		response2 = requests.get(
			'https://api.propublica.org/congress/v1/' + str(current_congress + 1) + '/house/bills/active.json',
			headers=header)
		if response2.status_code == 200:
			return current_congress + 1

	return current_congress


get_recent_bills()
