import math
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

load_dotenv()


def load_vocab():
    vocab = {}
    with open('vocab.txt', 'r', encoding='utf-8', errors='ignore') as f:
        vocab_terms = f.readlines()
    with open('idf-values.txt', 'r', encoding='utf-8', errors='ignore') as f:
        idf_values = f.readlines()
    for (term, idf_value) in zip(vocab_terms, idf_values):
        vocab[term.strip()] = int(idf_value.strip())
    return vocab


def load_documents():
    with open('documents.txt', 'r', encoding='utf-8', errors='ignore') as f:
        documents = f.readlines()
    return [document.strip().split() for document in documents]


def load_inverted_index():
    inverted_index = {}
    with open('inverted-index.txt', 'r', encoding='utf-8', errors='ignore') as f:
        inverted_index_terms = f.readlines()
    for row_num in range(0, len(inverted_index_terms), 2):
        term = inverted_index_terms[row_num].strip()
        documents = inverted_index_terms[row_num + 1].strip().split()
        inverted_index[term] = documents
    return inverted_index


def load_link_of_qs():
    with open("Qdata/Qindex.txt", "r", encoding='utf-8', errors='ignore') as f:
        return f.readlines()


vocab_idf_values = load_vocab()
documents        = load_documents()
inverted_index   = load_inverted_index()
Qlink            = load_link_of_qs()


def get_tf_dictionary(term):
    tf_values = {}
    if term in inverted_index:
        for document in inverted_index[term]:
            if document not in tf_values:
                tf_values[document] = 1
            else:
                tf_values[document] += 1
        for document in tf_values:
            tf_values[document] /= len(documents[int(document)])
    return tf_values


def get_idf_value(term):
    return math.log(len(documents) / vocab_idf_values[term])


def calculate_sorted_order_of_documents(query_terms):
    potential_documents = {}
    for term in query_terms:
        if term not in vocab_idf_values:
            continue
        tf_values_by_document = get_tf_dictionary(term)
        idf_value = get_idf_value(term)
        for document in tf_values_by_document:
            if document not in potential_documents:
                potential_documents[document] = tf_values_by_document[document] * idf_value
            else:
                potential_documents[document] += tf_values_by_document[document] * idf_value
    for document in potential_documents:
        potential_documents[document] /= len(query_terms)
    potential_documents = dict(sorted(potential_documents.items(), key=lambda item: item[1], reverse=True))
    ans = []
    for document_index in potential_documents:
        ans.append({
            "Question Link": Qlink[int(document_index) - 1][:-2],
            "Score": round(potential_documents[document_index], 6)
        })
    return ans


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')


class SearchForm(FlaskForm):
    search = StringField('Search coding problems')
    submit = SubmitField('Search')


@app.route("/", methods=['GET', 'POST'])
def home():
    form         = SearchForm()
    results      = []
    query_string = ""
    search_error = None

    if form.validate_on_submit():
        query_string = form.search.data.strip()
        q_terms      = [term.lower() for term in query_string.split() if term]
        try:
            results = calculate_sorted_order_of_documents(q_terms)[:20]
        except Exception:
            search_error = "Something went wrong. Please try again."

    return render_template(
        'index.html',
        form=form,
        results=results,
        query_string=query_string,
        search_error=search_error
    )


@app.route("/api/search/<query>")
def api_search(query):
    q_terms = [term.lower() for term in query.strip().split()]
    return jsonify(calculate_sorted_order_of_documents(q_terms)[:20])


if __name__ == '__main__':
    app.run(debug=True)