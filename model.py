from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import string
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import re
from simplemma import text_lemmatizer


def clean_text(text):
    text = text.replace("Â", "a")
    text = text.replace("â", "a")
    text = text.replace("î", "i")
    text = text.replace("Î", "ı")
    text = text.replace("İ", "i")
    text = text.replace("I", "ı")
    text = text.replace(u"\u00A0", " ")
    text = text.replace("|", " ")

    text = re.sub(r"@[A-Za-z0-9]+", " ", text)
    text = re.sub(r"(.)\1+", r"\1\1", text)
    text = re.sub(r"https?:\/\/\S+", " ", text)
    text = re.sub(r"http?:\/\/\S+", " ", text)
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"#(\w+)", " ", text)
    text = re.sub(r"^\x00-\x7F]+", " ", text)
    text = re.sub(r"[^A-Za-zâîığüşöçİĞÜŞÖÇ]+", " ", text)
    text = re.sub(r"((https://[^\s]+))", " ", text)
    text = " ".join(text.lower().strip().split())

    return " ".join(text_lemmatizer(text, lang="tr"))


def clean_row(row):
    content = clean_text(row["content"])

    return content


df = pd.read_excel('excelFiles/newsData2.xlsx')
# df["clean_content"] = df.apply(lambda row: clean_row(row), axis=1)

X = df.clean_content.to_numpy()
y = df.new_tag.to_numpy()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0)

# Naive Bayes ile model oluşturma
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

model_NB = MultinomialNB()
model_NB.fit(X_train, y_train)
print("NB train accuracy:", model_NB.score(X_train, y_train))
print("NB test accuracy:", model_NB.score(X_test, y_test))

predictions_train = model_NB.predict(X_train)
print("NB Train F1:", f1_score(y_train, predictions_train))
predictions_test = model_NB.predict(X_test)
print("NB Test F1:", f1_score(y_test, predictions_test))

# SVM ile model oluşturma
sc_X = StandardScaler(with_mean=False)
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)
classifier = SVC(kernel='linear', random_state=0)
classifier.fit(X_train, y_train)
print("SVM train accuracy:", classifier.score(X_train, y_train))
print("SVM test accuracy:", classifier.score(X_test, y_test))

# decision tree ile model oluşturma ve cross validation kullanma ve grid search ile en iyi parametreleri bulma
clf = DecisionTreeClassifier(criterion="entropy", max_depth=5)
clf.fit(X_train, y_train)
clf.score(X_test, y_test)
clf = DecisionTreeClassifier(criterion="entropy", max_depth=5)
scores = cross_val_score(clf, X_train, y_train, cv=5)
parameters = {"criterion": ["entropy", "gini", "log_loss"],
              "max_depth": range(2, 100)}

clf = GridSearchCV(DecisionTreeClassifier(), parameters,
                   cv=5, n_jobs=4, verbose=3)
clf.fit(X_train, y_train)
print("Best score:", clf.best_score_, "Best params:", clf.best_params_)
tree = clf.best_estimator_
print(tree.score(X_train, y_train))
print(tree.score(X_test, y_test))
