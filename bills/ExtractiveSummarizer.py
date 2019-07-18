from bills.BillMetadataBuilder import BillMetadataBuilder
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class ExtractiveSummarizer:
    """
    The title_multiplier allows us to tweak how sensitive our summary is to the title vs the rest of the text in the
    document.
    At minimum the document must have a title and summary, otherwise the constructor will throw an error
    the corpus can be tweaked using the set_corpus method
    """
    def __init__(self, bill, title_multiplier=0.01, mode='basic'):
        self.mode = mode
        self.bill = bill
        self.builder = BillMetadataBuilder(bill)
        self.corpus = self.bill['title'] + ' ' + self.bill['summary']
        self.body_len = len(self.bill['summary'])

        self.summary = ''
        self.stemmed_title_words = []
        self.top_25_stemmed = []
        self.top_10_nouns_stemmed = []

        self.title_weight = (len(bill['title']) + len(bill['summary']) // 10) * title_multiplier

    # just in case we want to define a larger word set for making summarization choices
    def set_corpus(self, new_corpus):
        self.corpus = new_corpus

    def get_summary(self):
        if self.mode == 'basic':
            self.get_first_n_summary()
        elif self.mode == 'best_n':
            self.get_best_n_summary()
        else:
            self.get_similarity_summary()

    """ SUMMARIZATION METHODS """

    """
    Works best for web-news based articles that have the most important content towards the front of the article
    Takes a FIFO approach to summarization.
      Most (web) news articles have the most crucial details early in the document body,
      with subsequent text being more detail oriented.
      This algorithm follows this notion by picking the most relevant early sentences
      until its sentence quota or percentage goal is met.
    """
    def get_first_n_summary(self, shorten_to_pct=0.5, shorten_to_len=-1):
        self.prep_for_summary()
        corpus = self.bill['summary']
        self.summary = ''
        paragraphs = corpus.split('\n')

        end_condition = self.select_end_condition(shorten_to_pct, shorten_to_len)

        # take the first and last sentence of the paragraph, plus the 'most relevant'
        # body sentence
        for p in paragraphs:
            # if we exceed the desired summary length, bail
            if end_condition[0](end_condition[1]):
                break

            sentences = sent_tokenize(p)
            num_sentences = len(sentences)
            # if we get no sentences back, jump to next paragraph
            if num_sentences == 0:
                continue

            self.summary += sentences[0] + ' '

            if num_sentences == 1:
                self.summary += '\n'
                continue

            if num_sentences == 2:
                self.summary += sentences[-1]
                self.summary += '\n'
                continue

            self.summary += self._get_best_sentence(sentences[1:-1]) + ' '
            self.summary += sentences[-1]
            self.summary += '\n'

        return self.summary

    """
    Mixture of the first_n and similarity methods
      Calculate the scores for all of the sentences, and then pull the best n % or n sentences
      If score option is provided, the straight up score of a line or the score density of a 
      line can be used to compute the line's rank
    """
    def get_best_n_summary(self, shorten_to_pct=0.5, shorten_to_len=-1, score='density'):
        self.prep_for_summary()
        self.summary = ''

        end_condition = self.select_end_condition(shorten_to_pct, shorten_to_len)

        # Calculate the best sentence values
        sentences = sent_tokenize(self.bill['summary'])
        scored = list()
        idx = 0
        for s in sentences:
            if score == 'density':
                scored.append((idx, self._get_line_score_density(s)))
            else:
                scored.append((idx, self._score_line(s)))

            idx += 1

        scored.sort(key=lambda pair: pair[1])

        # Repeatedly iterate over the sentences, taking the ones with the highest
        # individual score until we exceed the desired length
        take = list()
        while not end_condition[0](end_condition[1]):
            self.summary = ''
            take.append(scored.pop())
            for index in take:
                self.summary += sentences[index[0]] + " "

        indices = [pair[0] for pair in take]
        indices.sort()
        self.summary = ''
        for index in indices:
            self.summary += sentences[index] + "\n"

        return self.summary

    """
    Use the TextRank algorithm to build a summary using similarity matrices
    we can either reduce the length by a percentage (shorten_to_pct) or by number of words (shorted_to_len)
    Not particularly efficient for large documents
      Tokenizes and gets a document word count.
    """
    def get_similarity_summary(self, shorten_to_pct=0.5, shorten_to_len=-1):
        # if we already made a summary, return that
        if len(self.summary) > 0:
            return self.summary

        sentences = sent_tokenize(self.bill['summary'])

        end_condition = self.select_end_condition(shorten_to_pct, shorten_to_len)

        # we're going to skip pulling in a huge word vector and instead just use the words provided in the document
        counter = CountVectorizer()
        x = counter.fit_transform(sentences)

        arr = x.toarray()
        sentence_vects = [v.tolist() for v in arr]
        similarity = np.zeros([len(sentences), len(sentences)])
        # compute the cartesian similarity matrix for all the sentences
        for i in range(len(sentence_vects)):
            for j in range(len(sentence_vects)):
                similarity[i][j] = cosine_similarity([sentence_vects[i]], [sentence_vects[j]])[0, 0]

        # sum the similarities for each sentence relative to the document.
        similarity = similarity.sum(axis=0)

        # extract the indices and similarity scores and sort them by similarity score
        similarity = [(index, val) for (index, val) in enumerate(similarity)]
        similarity.sort(key=lambda pair: pair[1])

        # Repeatedly iterate over the similarities, taking the sentence with the highest
        # document similarity until we exceed the desired length
        take = list()
        while not end_condition[0](end_condition[1]):
            self.summary = ''
            take.append(similarity.pop())
            for index in take:
                self.summary += sentences[index[0]] + " "

        indices = [pair[0] for pair in take]
        indices.sort()
        self.summary = ''
        for index in indices:
            self.summary += sentences[index] + "\n"

        return self.summary

    """ HELPER METHODS """

    # prepare to build a summary by getting the title and corpus words with the greatest weight
    def prep_for_summary(self):
        self._title_pass()
        self.top_25_stemmed = self.stem_list(self.builder.get_top_25_words(self.corpus))
        self.top_10_nouns_stemmed = self.stem_list(self.builder.get_top_n_nouns(10))

    # take a pass at the title to pull the most common verbs and nouns
    def _title_pass(self):
        title_pos = self.builder.get_title_pos()
        noun_verb_pos_tags = ['NN', 'NNP', 'NNS', 'VB', 'VBP']
        verbs_and_nouns = [pair[0] for pair in title_pos if pair[1] in noun_verb_pos_tags]
        self.stemmed_title_words = self.stem_list(verbs_and_nouns)
        return verbs_and_nouns

    def _get_best_sentence(self, middle_sentences):
        if len(middle_sentences) == 1:
            return middle_sentences[0]

        scores = []
        for s in middle_sentences:
            scores.append(self._score_line(s))

        return middle_sentences[scores.index(max(scores))]

    """
    For the simple summarizer we prioritize sentences in the following method
      If the line contains a stemmed word from the title, we add the
      defined title_weight from the constructor
      If the line contains a word in the top 10 stemmed nouns add 3
      If a line contains one of the top 25 stemmed words add 1
    """
    def _score_line(self, line):
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

    """
    Score the line based on the density of score to the length of the line
    This should help to week out sentences that are just really long, and therefore
    statistically can score higher just due to increased vector length
    """
    def _get_line_score_density(self, line):
        score = self._score_line(line)
        return score/len(line)

    """ Methods for regulating the end conditions of the summarizer"""

    def has_exceeded_len_pct(self, pct):
        return (len(self.summary) / self.body_len) > pct

    def has_exceeded_len_count(self, count):
        return self.summary.count('. ') + self.summary.count('.\n') >= count

    # select our maximum length determination strategy
    # default is percentage, but we can do sentence count if desired
    def select_end_condition(self, pct, count):
        len_condition = self.has_exceeded_len_pct
        upper_thresh = pct
        if count != -1 and count > 0:
            len_condition = self.has_exceeded_len_count
            upper_thresh = count

        return len_condition, upper_thresh

    # Helper stemmer method for lists
    @staticmethod
    def stem_list(lst):
        stemmer = SnowballStemmer('english')
        return [stemmer.stem(token) for token in lst]
