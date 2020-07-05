# Use to populate bill keywords table in database
from db.BillCache import BillCache
from bills.BillMetadataBuilder import BillMetadataBuilder
from sqlite3 import IntegrityError

bill_cache = BillCache()

for session in range(105, 117):
    print(session)
    all_bills = bill_cache.get_bill_from_session(session)
    for bills in all_bills:
        bill = {'title': bills.get('TITLE'), 'short_title': bills.get('SHORT_TITLE'), 'summary': bills.get('SUMMARY'),
            'sponsor_name': '', 'committees': ''}
        extractive_summarizer = BillMetadataBuilder(bill)
        corpus = bill.get('title') + ' ' + bill.get('summary')
        top_10_words = extractive_summarizer.get_top_10_words(corpus)
        top_10_words = [(t[0], t[1]) for t in top_10_words]
        for words in top_10_words:
            try:
                bill_cache.store_keyword_to_bill(words[0], bills.get('ID'), words[1])
            except IntegrityError:
                print('Keyword and bill id already in database')