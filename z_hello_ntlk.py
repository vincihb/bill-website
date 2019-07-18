import time
from Pickler import Pickler
from bills.ExtractiveSummarizer import ExtractiveSummarizer
from nltk.tokenize import sent_tokenize, word_tokenize

start_time = time.time()

articles = Pickler.load_obj('test-articles')

# article = dict()
# article['title'] = ""
# article['summary'] = """
# """


article = articles[4]
# Pickler.save_obj(articles, 'test-articles')


summ = ExtractiveSummarizer(article)

short = summ.get_first_n_summary(shorten_to_len=4)
short_2 = summ.get_similarity_summary(shorten_to_len=4)
saved_pct = (len(short)/len(article['summary'])) * 100

print('')
print(article['title'])
print(short)
print('')
print('Compressed to {0:0.2f}% of original'.format(saved_pct))
print('')
print('Program executed in: {0:.2f}s'.format(time.time() - start_time))

def diff(summ1, summ2):
    sentences = sent_tokenize(summ1)
    s_s2 = sent_tokenize(summ1)
    similarity = 0
    for s in sentences:
        if s in summ2:
            similarity += 1

    # divide the number of common sentences by the
    # average num of sentences in both summaries
    return similarity / ((len(sentences) + len(s_s2)) / 2)

print(diff(short, short_2))
