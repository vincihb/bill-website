import requests, time, json
from Pickler import Pickler
from config.ConfReader import conf


class PropublicaScraper:
    CURRENT_CONGRESS = conf.CURRENT_CONGRESS
    DELAY_INTERVAL = 1.5
    MAX_MISSES = 5

    @staticmethod
    def get_senators():
        return PropublicaScraper.get_members_of_congress('senate', 'Senate Members', 80,
                                                         PropublicaScraper.CURRENT_CONGRESS)

    @staticmethod
    def get_house_members():
        return PropublicaScraper.get_members_of_congress('house', 'House Members', 102,
                                                         PropublicaScraper.CURRENT_CONGRESS)

    @staticmethod
    def get_members_of_congress(house, file_cache, min_session, max_session):
        house = house.lower()
        if house != 'house' and house != 'senate':
            house = 'house'

        # Add the API key in
        header = {'X-API-Key': conf.PROPUBLICA_API_KEY}

        members = dict()
        for i in range(min_session, max_session + 1):
            # slow us down so the scraping sucks less
            time.sleep(PropublicaScraper.DELAY_INTERVAL)
            print(house + ' session: ' + str(i))
            res = requests.get('https://api.propublica.org/congress/v1/' + str(i) + '/' + house + '/members.json',
                               headers=header)

            if res.status_code != 200:
                PropublicaScraper.log_error('ERROR: Could not connect to the server for index ' + str(i), res.text)
                continue

            data = res.json()
            for member in data['results'][0]['members']:
                member_id = member['id']
                # if the member has already been added, just update the
                if member_id in members:
                    members[member_id]['first_session'] = i
                else:
                    members[member_id] = member
                    members[member_id]['first_session'] = i
                    members[member_id]['last_session'] = i

        Pickler.save_obj(members, file_cache)

        return members

    @staticmethod
    def get_bills(congress_session_min, congress_session_max, num_bills=100, chamber='both', offset=0):
        abs_min_bill_congress = 105
        per_page = 20

        # Add the API key in
        header = {'X-API-Key': conf.PROPUBLICA_API_KEY}

        if congress_session_min < abs_min_bill_congress:
            congress_session_min = abs_min_bill_congress

        if congress_session_max > PropublicaScraper.CURRENT_CONGRESS:
            congress_session_max = PropublicaScraper.CURRENT_CONGRESS

        original_num_pages = (num_bills // per_page)
        page_offset = (offset // per_page)
        misses = 0
        for session in range(congress_session_min, congress_session_max + 1):
            session_bills = dict()

            for i in range(page_offset, original_num_pages):
                time.sleep(PropublicaScraper.DELAY_INTERVAL)
                offset = i * per_page

                print('Bill series: ' + str(session) + '/introduced/' + str(offset))
                res = requests.get('https://api.propublica.org/congress/v1/' + str(session) + '/' +
                                   chamber + '/bills/introduced.json?offset=' + str(offset),
                                   headers=header)

                if res.status_code != 200:
                    if misses > PropublicaScraper.MAX_MISSES:
                        break
                    else:
                        misses += 1

                    PropublicaScraper.log_error('ERROR: Failed to get data for: ' + str(session)
                                                + '/introduced/' + str(offset), res.text)
                    continue

                try:
                    data = res.json()
                    retrieved = len(data['results'][0]['bills'])

                    # if we got no results we should stop making requests :)
                    if retrieved == 0:
                        print('Retrieved 0 bills, finishing...')
                        break

                    print('Retrieved ' + str(retrieved) + ' bills... Storing')

                    for bill in data['results'][0]['bills']:
                        bill_id = bill['bill_id']
                        session_bills[bill_id] = bill
                except json.decoder.JSONDecodeError:
                    PropublicaScraper.log_error('Error decoding JSON for bill set, skipping: '
                                                + str(session) + '/introduced/' + str(offset),
                                                res.text)
                    continue

            save_location = 'Bill Set-' + str(session) + '-3'
            print('Done with congressional session: ' + str(session))
            print('Saving to ' + save_location + '...')
            Pickler.save_obj(session_bills, save_location)

        print('Done!')

    @staticmethod
    def get_bills_for_session(session, num_bills=15000):
        PropublicaScraper.get_bills(session, session, num_bills)

    @staticmethod
    def log_error(message, text):
        print(message)
        with open('error.txt', 'a+') as err_file:
            err_file.write(message + '\n')
            err_file.write(text + '/n')
