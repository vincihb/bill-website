from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag
from collections import Counter
from string import punctuation


class BillMetadataBuilder:
    def __init__(self, bill):
        self.bill = bill
        self.stripped_tokens = []
        self.bow = []
        self.top_25 = []
        self.top_25_words = []
        self.sentences = []
        self.title_pos = []
        self.summary_pos = []

    def get_bag_of_words(self):
        # if we've already done the parse, don't do it twice
        if len(self.bow) != 0:
            return self.bow

        b = self.bill
        # we weight title words slightly higher by including the title and short title
        bill_corpus = \
            b['title'] + ' ' + b['short_title'] + ' ' + b['sponsor_name'] + ' ' + b['sponsor_name'] + ' ' + \
            b['summary'] + ' ' + b['committees']

        bill_bow = self.get_stripped_bag_of_words(bill_corpus)

        self.bow = bill_bow
        return bill_bow

    @staticmethod
    def get_stripped_bag_of_words(corpus):
        stop_words = list(punctuation) + stopwords.words('english')
        bow = []
        for w in corpus.lower().split():
            # don't carry single letters into the BOW
            if w not in stop_words and len(w) > 1:
                bow.append(w)

        return bow

    def get_top_25(self):
        if len(self.bow) == 0:
            self.get_bag_of_words()

        if len(self.top_25) > 0:
            return self.top_25_words

        c = Counter(self.bow)

        self.top_25 = c.most_common(25)

        # extract just the words, just in case we just want those
        self.top_25_words = [w[0] for w in self.top_25]
        return self.top_25_words

    def get_sentence_tokens(self):
        if len(self.sentences) > 0:
            return self.sentences

        tokens = sent_tokenize(self.bill['summary'])
        self.sentences = tokens
        return tokens

    def get_pos_tags(self):
        if len(self.summary_pos) > 0:
            return self.summary_pos

        title_tokes = word_tokenize(self.bill['title'])
        self.title_pos = pos_tag(title_tokes)
        summary_tokens = word_tokenize(self.bill['summary'])
        self.summary_pos = pos_tag(summary_tokens)
        return self.summary_pos

    def get_top_25_nouns(self):
        tags = self.get_pos_tags()
        tags

    def __str__(self):
        return 'Parser for Bill: ' + self.bill['bill_id']
