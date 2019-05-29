from Pickler import Pickler
from bills.BillMetadataBuilder import BillMetadataBuilder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

# NLTK_SET = 'nltk_113_500'
#
# bills = Pickler.load_obj('complete/Bill Set-116-Complete')
#
# print(len(bills))
#
# key_data = dict()
# for key in bills:
#
#     bill = bills[key]
#     if bill['bill_type'] != 's' and bill['bill_type'] != 'hr' or bill['enacted'] is not None:
#         continue
#
#     bill_metadata = dict()
#     metadata_builder = BillMetadataBuilder(bill)
#
#     bill_metadata['bow'] = metadata_builder.get_bag_of_words()
#     bill_metadata['top_25'] = metadata_builder.get_top_25()
#     print(bill['bill_type'] + ': ' + bill['short_title'])
#     print(bill_metadata['top_25'][:10])
#     print('')
#     key_data[key] = bill_metadata

with open('obj/pandas_dfs/test.json', 'w+') as f:
    dfj = pd.DataFrame(np.random.randn(5, 2), columns=list('AB'))
    f.write(dfj.to_json())
