from bills.BillMetadataBuilder import BillMetadataBuilder
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize


class Summarizer:
    def __init__(self, bill, title_multiplier=0.01):
        self.bill = bill
        self.builder = BillMetadataBuilder(bill)

        self.simple_summary = ''

        self.summary = ''
        self.stemmed_title_words = []
        self.top_25_stemmed = []
        self.top_10_nouns_stemmed = []

        self.title_weight = (len(bill['title']) + len(bill['summary']) // 10) * title_multiplier

    def prep_for_summary(self):
        self.title_pass()
        self.top_25_stemmed = self.stem_list(self.builder.get_top_25_words())
        self.top_10_nouns_stemmed = self.stem_list(self.builder.get_top_n_nouns(10))

    # Works best for web-news based articles that have the most important content towards the from of the article
    def get_simple_summary(self, shorten_to=0.5):
        corpus = self.bill['summary']
        self.simple_summary = ''
        paragraphs = corpus.split('\n')

        # take the first and last sentence of the paragraph, plus the 'most relevant'
        # body sentence
        for p in paragraphs:
            # if we exceed the desired summary length, bail
            if len(self.simple_summary)/len(self.bill['summary']) > shorten_to:
                break

            sentences = sent_tokenize(p)
            num_sentences = len(sentences)
            # if we get no sentences back, jump to next paragraph
            if num_sentences == 0:
                continue

            self.simple_summary += sentences[0] + ' '

            if num_sentences == 1:
                self.simple_summary += '\n'
                continue

            if num_sentences == 2:
                self.simple_summary += sentences[-1]
                self.simple_summary += '\n'
                continue

            self.simple_summary += self.get_best_sentence(sentences[1:-1]) + ' '
            self.simple_summary += sentences[-1]
            self.simple_summary += '\n'

        return self.simple_summary

    def get_best_sentence(self, middle_sentences):
        if len(middle_sentences) == 1:
            return middle_sentences[0]

        scores = []
        for s in middle_sentences:
            scores.append(self.score_line(s))

        return middle_sentences[scores.index(max(scores))]

    def get_summary(self, shorten_to=0.5):
        if len(self.summary) > 0:
            return self.summary

        self.builder.get_top_25_words()

        tokens = self.builder.get_sentence_tokens()
        scores = []
        for line in tokens:
            scores.append(self.score_line(line))

        # BUILD SUMMARY #
        return self.summary

    # take a pass at the title to pull the most common verbs and nouns
    def title_pass(self):
        title_pos = self.builder.get_title_pos()
        noun_verb_pos_tags = ['NN', 'NNP', 'NNS', 'VB', 'VBP']
        verbs_and_nouns = [pair[0] for pair in title_pos if pair[1] in noun_verb_pos_tags]
        self.stemmed_title_words = self.stem_list(verbs_and_nouns)
        return verbs_and_nouns

    def score_line(self, line):
        words = word_tokenize(line)
        stemmed = self.stem_list(words)
        score = 0
        for word in stemmed:
            if word in self.stemmed_title_words:
                score += self.title_weight

            if word in self.top_10_nouns_stemmed:
                score += 3

            if word in self.top_25_stemmed:
                score += 1

        return score

    @staticmethod
    def stem_list(lst):
        stemmer = SnowballStemmer('english')
        return [stemmer.stem(token) for token in lst]
