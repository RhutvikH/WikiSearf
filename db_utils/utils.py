import sqlite3
import numpy as np
import spacy
import heapq
from collections import defaultdict

nlp = spacy.load('en_core_web_sm-3.8.0')

def show_some_entries(db_path: str):

    connection: sqlite3.Connection = sqlite3.connect(db_path)
    cursor: sqlite3.Cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM postings WHERE word_id=1127
    """)

    rows = cursor.fetchall()
    print(rows)

    connection.close()


def find_word(db_path: str, word: str):

    connection: sqlite3.Connection = sqlite3.connect(db_path)
    cursor: sqlite3.Cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM words WHERE word = ?
    """, (word,))

    word_id: int = cursor.fetchone()

    if word_id is None:
        return -1

    # print(word_id)
    return word_id[0]


def find_docs_with_word(db_path: str, word_id: str):

    connection: sqlite3.Connection = sqlite3.connect(db_path)
    cursor: sqlite3.Cursor = connection.cursor()
    # word_id: int = find_word(db_path, word)

    cursor.execute("""
        SELECT * FROM postings WHERE word_id = ?
    """, (word_id,))

    docs = cursor.fetchall()
    doc_ids: list = []

    for doc in docs:
        doc_ids.append(doc[1])

    return doc_ids


def find_word_count(db_path: str, word_id: int):
    connection: sqlite3.Connection = sqlite3.connect(db_path)
    cursor: sqlite3.Cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM postings WHERE word_id = ?
    """, (word_id,))

    word_count: int = cursor.fetchone()[0]

    return word_count


def get_avg_doc_length(db_path: str):
    connection: sqlite3.Connection = sqlite3.connect(db_path)
    cursor: sqlite3.Cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(d.length) / COUNT(*) FROM documents as d 
    """)

    avg_doc_length: float = cursor.fetchone()[0]

    return avg_doc_length


def show_document(db_path: str, doc_id: int):

    connection: sqlite3.Connection = sqlite3.connect(db_path)
    cursor: sqlite3.Cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM documents WHERE doc_id = ?
    """, (doc_id,))

    doc = cursor.fetchone()

    print(doc)

def get_single_doc(db_path: str, doc_id: int):

    connection: sqlite3.Connection = sqlite3.connect(db_path)
    cursor: sqlite3.Cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM documents WHERE doc_id = ?
    """, (doc_id,))

    doc = cursor.fetchone()
    print(doc)
    return doc


def get_docs(db_path: str, best_doc_ids):

    all_docs: list = []

    for id in best_doc_ids:
        all_docs.append(get_single_doc(db_path, id))

    return all_docs


def get_doc_db_size(db_path: str):

    connection: sqlite3.Connection = sqlite3.connect(db_path)
    cursor: sqlite3.Cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM documents
        """)

    length: int = cursor.fetchone()[0]

    return length


def bm_get_word_idf(db_path: str, word_id: int):

    db_len: int = get_doc_db_size(db_path)
    word_count = find_word_count(db_path, word_id)

    return np.log((db_len - word_count + 0.5) / (word_count + 0.5))


def bm_find_tf(db_path: str, doc_id: int, word: str, avg_doc_length: float, k: float = 1.2, b: float = 0.75):

    # tf is normalized in tf-idf, but in bm25 it is the raw count
    connection: sqlite3.Connection = sqlite3.connect(db_path)
    cursor: sqlite3.Cursor = connection.cursor()

    cursor.execute("""
        SELECT title, abstract, length FROM documents where doc_id = ?
        """, (doc_id,))

    title, abstract, length = cursor.fetchone()
    count: int = " ".join([title, abstract]).lower().count(word.lower())

    tf: float = (count * (k + 1)) / (count + k * (1 - b + b * (length / avg_doc_length)))

    # print(tf)
    return tf


def get_random_docs(db_size: int, num_docs: int):

    random_indices: np.ndarray = np.random.choice(db_size, size=(num_docs), replace=False)
    return list(map(int, random_indices))


def get_top_docs(db_path: str, query: str, n: int, db_size: int, avg_doc_length: float):

    polished_query: list = [q for q in nlp(query.lower())\
    if not all([q.is_stop, q.is_digit, q.is_punct, q.is_space])]

    word_ids: dict = {str(word): find_word(db_path, str(word)) for word in polished_query}
    word_doc_ids: dict = {word_id: find_docs_with_word(db_path, word_id) for word_id in word_ids.values()}

    # for word in polished_query:
    #     print(word, len(word), type(word))
    #     print(find_word(db_path, word))

    tf_idfs: dict = defaultdict(int)

    for word in word_ids:
        idf: float = bm_get_word_idf(db_path, word_ids[word])
        doc_ids: list = word_doc_ids[word_ids[word]]

        for doc_id in doc_ids:
            tf_idfs[doc_id] += bm_find_tf(db_path, doc_id, word, avg_doc_length) * idf

    # print(tf_idfs)
    n_largest: list = heapq.nlargest(n, tf_idfs, key = lambda tf_idf: tf_idfs[tf_idf])

    if len(n_largest) < n:
        print(f"Documents from index {len(n_largest)} onwards are irrelevant to the query\n")

    n_largest.extend(get_random_docs(db_size, n - len(n_largest)))
    print(n_largest)

    return n_largest


# db_path: str = "db/wikip_db.db"
