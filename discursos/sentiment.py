import collections
import nltk
import datetime
import re
from dashboard.models import Discurso

def get_words_in_sentences(sentences):
    all_words = []
    for (words, category) in sentences:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
      features['contains(%s)' % word] = (word in document_words)
    return features

def collect_sentences(rawtuples):
    sentences = []
    for (words, category) in rawtuples:
      words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
      sentences.append((words_filtered, category))
    return sentences

def tuple_from_queryset(queryset, parameter):
    punctuation = re.compile(r'[-.?!,":;()|0-9]') 
    sentence_tuple = []
    for q in queryset:
        sentence_tuple.append((punctuation.sub("", q.sumario.lower().encode('utf-8')), q.partido.sigla.lower()))
    return sentence_tuple

def precision_recall(classifier, testfeats):
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)
    for i, (feats, label) in enumerate(testfeats):
        refsets[label].add(i)
        observed = classifier.classify(feats)
        testsets[observed].add(i)
    precisions = {}
    recalls = {}
    for label in classifier.labels():
        precisions[label] = nltk.metrics.precision(refsets[label],
        testsets[label])
        recalls[label] = nltk.metrics.recall(refsets[label], testsets[label])
    return precisions, recalls


arena = Discurso.objects.filter(data__gt=datetime.date(1968, 10, 01), partido__sigla="ARENA")
arena_sentences = tuple_from_queryset(arena, 'arena')

mdb = Discurso.objects.filter(data__gt=datetime.date(1968, 10, 01) , partido__sigla="MDB")
mdb_sentences = tuple_from_queryset(mdb, 'mdb')

training_sentences = collect_sentences(arena_sentences + mdb_sentences)

word_features = get_word_features(get_words_in_sentences(training_sentences))

training_set = nltk.classify.apply_features(extract_features, training_sentences)

classifier = nltk.NaiveBayesClassifier.train(training_set)

#--

check_sentences = tuple_from_queryset(Discurso.objects.filter(estado__sigla='CE'), 'arena')
check_set = nltk.classify.apply_features(extract_features, collect_sentences(check_sentences))

#classifier.show_most_informative_features(32) p/ visualizar diferencas
#classifier.classify(extract_features(sentence.split())) p/ classificar um resultado
#nltk.classify.util.accuracy(classifier, training_set) p/ testar accuracy


