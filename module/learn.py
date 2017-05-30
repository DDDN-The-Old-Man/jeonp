import csv
import sqlite3
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


DATABASE = '../database.db'
DB = sqlite3.connect(DATABASE)


class TaggedBody:
    def __init__(self, tags, data):
        self.tags = tags
        self.data = data


# Return formatted datasets
def get_datasets(path):
    with open(path, 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter=';')
        tags = []
        data = []
        for row in rows:
            if row[0] == 'O' or row[0] == 'C':
                continue
            tags.append(row[0])
            data.append(row[3])

    return TaggedBody(tags, data)


"""
# Return formatted datasets
def get_datasets_DB(path):
    db = sqlite3.connect(DATABASE)
    GET_ID_QUERY = 'SELECT id FROM article WHERE u_id = ?'
    PARSE_QUERY = 'SELECT parsed FROM parsed_article WHERE id = ?'
    with open(path, 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter=';')
        count = 0
        tags = []
        data = []
        for row in rows:
            if row[0] == 'O' or row[0] == 'C':
                continue
            id = db.execute(GET_ID_QUERY, [str(row[1])]).fetchone()
            print (id)
            parsed = db.execute(PARSE_QUERY, [id]).fetchall()
            tags.append(row[0])
            data.append(row[4])
            # TODO :: NOT  ALL LABELED
            count += 1
            if count >= 220:
                break

    return TaggedBody(tags, data)
"""


# Vectorize article's body and tag name
def vectorize(tb):
    vectorizer = CountVectorizer()
    # tf_transformer = TfidfTransformer(use_idf=False)
    tb.tags = [0 if tag == 'F' else 1 for tag in tb.tags]
    # Use datas in DB to construct bag of words model
    ARTICLE_QUERY = 'SELECT body FROM article'
    cur = DB.execute(ARTICLE_QUERY)
    db_data = cur.fetchall()
    db_data = [body[0] for body in db_data]
    vectorizer = vectorizer.fit(tb.data + db_data)
    tb.data = vectorizer.transform(tb.data)
    print (tb.data.shape)
    # tb.data = tf_transformer.fit_transform(tb.data)


# Classify given vectorized bodys
def classify(tb):
    classifier = MultinomialNB()
    # Use odd number datasets as train set
    classifier.fit(tb.data[1::2], tb.tags[1::2])
    predicted = classifier.predict(tb.data[::2])
    predicted_proba = classifier.predict_proba(tb.data[::2])
    score = metrics.accuracy_score(tb.tags[::2], predicted)
    report = metrics.classification_report(tb.tags[::2], predicted,
            target_names=['F', 'T'])
    return (score, report, predicted_proba)


# Make formatted datasets from raw data
taggedBody = get_datasets('output.csv')
# Vectorize datasets
vectorize(taggedBody)
# Classify datasets
result = classify(taggedBody)
print (result[0], result[1], result[2])
