from api.propublica.PropublicaScraper import PropublicaScraper
from tool.Pickler import Pickler


class ToPickle:
    @staticmethod
    def get_senators():
        return ToPickle.get_members_of_congress('senate', 'Senate Members', 102, PropublicaScraper.CURRENT_CONGRESS)

    @staticmethod
    def get_house_members():
        return ToPickle.get_members_of_congress('house', 'House Members', 102, PropublicaScraper.CURRENT_CONGRESS)

    @staticmethod
    def get_bills(congress_session_min, congress_session_max, num_bills=100, chamber='both', offset=0):
        abs_min_bill_congress = 105

        if congress_session_min < abs_min_bill_congress:
            congress_session_min = abs_min_bill_congress

        if congress_session_max > PropublicaScraper.CURRENT_CONGRESS:
            congress_session_max = PropublicaScraper.CURRENT_CONGRESS

        for session in range(congress_session_min, congress_session_max + 1):
            session_bills = PropublicaScraper.get_session_bills(session=session, chamber=chamber, num_bills=num_bills,
                                                                offset=offset)

            save_location = 'Bill Set-' + str(session) + '-3'
            print('Done with congressional session: ' + str(session))
            print('Saving to ' + save_location + '...')
            Pickler.save_obj(session_bills, save_location)

        print('Done!')

    @staticmethod
    def get_members_of_congress(house, file_cache, min_session, max_session):
        members = PropublicaScraper.get_members_of_congress(house, min_session, max_session)
        Pickler.save_obj(members, file_cache)
        return members

    @staticmethod
    def get_bills_for_session(session, num_bills=15000):
        return ToPickle.get_bills(session, session, num_bills=num_bills)

