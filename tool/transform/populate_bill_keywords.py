# Use to populate bill keywords table in database
from db.BillCache import BillCache
from bills.BillMetadataBuilder import BillMetadataBuilder
import re

bill_cache = BillCache()
all_bills = bill_cache.get_bill_from_session(105)
for bills in all_bills:
    print(bills)
    bill = {'title': bills.get('TITLE'), 'short_title': bills.get('SHORT_TITLE'), 'summary': bills.get('SUMMARY'),
            'sponsor_name': '', 'committees': ''}
    extractive_summarizer = BillMetadataBuilder(bill)
    corpus = bill.get('title') + ' ' + bill.get('summary')
    corpus = re.sub(r'[^\w\s]', '', corpus)
    total_words = extractive_summarizer.get_total_words(corpus)
    top_10_words = extractive_summarizer.get_top_10_words(corpus)
    top_10_words = [(t[0], t[1]/(float(total_words))) for t in top_10_words]
    print(top_10_words)
    exit()
