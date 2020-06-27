# Use to populate bill keywords table in database
from db.BillCache import BillCache
from bills.ExtractiveSummarizer import ExtractiveSummarizer

bill_cache = BillCache()
all_bills = bill_cache.get_bill_from_session(105)
for bills in all_bills:
    print(bills)
    bill = {'title': bills.get('TITLE'), 'summary': bills.get('SUMMARY')}
    extractive_summarizer = ExtractiveSummarizer(bill)
    print(extractive_summarizer.get_summary())



