from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from collections import Counter
from string import punctuation


class BillMetadataBuilder:
    def __init__(self, bill):
        self.bill = bill
        self.stripped_tokens = []
        self.bow = []
        self.top_10 = []
        self.top_25 = []
        self.top_25_words = []
        self.top_10_nouns = []
        self.top_10_nouns_freq = []
        self.sentences = []
        self.title_pos = []
        self.summary_pos = []

        self.pos_tagged = False

    def get_bag_of_words(self, corpus=''):
        # if we've already done the parse, don't do it twice
        if len(self.bow) != 0:
            return self.bow

        b = self.bill
        # we weight title words slightly higher by including the title and short title
        if corpus == '':
            corpus = \
                b['title'] + ' ' + b['short_title'] + ' ' + b['sponsor_name'] + ' ' + b['sponsor_name'] + ' ' + \
                b['summary'] + ' ' + b['committees']

        bill_bow = self.get_stripped_bag_of_words(corpus)
        self.bow = bill_bow
        return bill_bow

    def get_total_words(self, corpus=''):
        if len(self.bow) == 0:
            self.get_bag_of_words(corpus)
        return len(self.bow)

    def get_top_25_words(self, corpus=''):
        if len(self.bow) == 0:
            self.get_bag_of_words(corpus)

        if len(self.top_25) > 0:
            return self.top_25_words

        c = Counter(self.bow)

        self.top_25 = c.most_common(25)
        # extract just the words, just in case we just want those
        self.top_25_words = [w[0] for w in self.top_25]
        return self.top_25_words

    def get_top_10_words(self, corpus=''):
        if len(self.bow) == 0:
            self.get_bag_of_words(corpus)

        if len(self.top_10) > 0:
            return self.top_10

        c = Counter(self.bow)

        self.top_10 = c.most_common(10)
        return self.top_10

    def get_title_pos(self):
        if len(self.title_pos) > 0:
            return self.title_pos

        self.title_pos = self.get_pos(self.bill['title'])
        return self.title_pos

    def get_summary_pos(self):
        # if there's no summary, return as there's no point in trying to tag it
        # or if it's already been tagger, don't do it again
        if len(self.bill['summary']) < 1 or len(self.summary_pos) > 0:
            return self.summary_pos

        self.summary_pos = self.get_pos(self.bill['summary'])
        return self.summary_pos

    def get_pos_tags(self):
        # if we've already tagged, don't redo
        if self.pos_tagged:
            return self.summary_pos

        self.get_title_pos()
        self.get_summary_pos()
        self.pos_tagged = True
        return self.summary_pos

    def get_top_n_nouns(self, n=10):
        tags = self.get_pos_tags()
        if len(tags) == 0 or len(self.top_10_nouns) > 0:
            return self.top_10_nouns

        nouns = [pair[0] for pair in tags if pair[1] == 'NNP' or pair[1] == 'NN' or pair[1] == 'NNS']
        c = Counter(nouns)
        self.top_10_nouns_freq = c.most_common(n)
        self.top_10_nouns = [w[0] for w in self.top_10_nouns_freq]
        return self.top_10_nouns

    @staticmethod
    def get_stripped_bag_of_words(corpus):
        stop_words = list(punctuation) + stopwords.words('english') + ['bill', 'act']
        bow = []
        for w in corpus.lower().split():
            # don't carry single letters into the BOW
            if w not in stop_words and len(w) > 1:
                bow.append(w)

        return bow

    @staticmethod
    def get_pos(corpus):
        corpus_tokens = word_tokenize(corpus.lower())
        return pos_tag(corpus_tokens)

    def __str__(self):
        return 'Parser for Bill: ' + self.bill['bill_id']
