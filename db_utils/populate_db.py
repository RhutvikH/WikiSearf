import gzip
import sqlite3
import xml.etree.ElementTree as ET
import spacy
from collections import Counter

nlp = spacy.load('en_core_web_sm')

def yield_documents(path):
    with gzip.open(path, 'rt', encoding='utf-8') as file:
        context = ET.iterparse(file, events=("start", "end"))
        id: int = 0

        for _, (event, elem) in enumerate(context):
            if event=='end' and elem.tag == 'doc':
                title = elem.findtext('title', "").strip("Wikipedia: ")
                abstract = elem.findtext('abstract')
                url = elem.findtext('url')

                links = [ (sublink.findtext('anchor', "").strip(), sublink.findtext('link', "").strip()) for sublink in elem.findall('.//sublink') ]
                # print(f"Title: {title}\nAbstract: {abstract}\nUrl: {url}\nLinks: {len(links)}")

                elem.clear()

                yield {'doc_id':id, 'title':title, 'abstract':abstract, 'url':url, 'links':links}

                id += 1
                if id % 1000 == 0:
                    print(id)

                # if id > 50:
                #     break


def add_documents_to_db(db_path: str, doc_path: str):

    connection: sqlite3.Connection = sqlite3.connect(db_path)
    cursor: sqlite3.Cursor = connection.cursor()
    cursor.execute("PRAGMA journal_mode = WAL")

    for doc in yield_documents(doc_path):
        doc_id: int = doc['doc_id']
        title: str = doc['title']
        url: str = doc['url']
        abstract: str = doc['abstract']
        links: str = str(doc['links'])
        counts: dict = Counter([word.lemma_ for word in nlp(" ".join([title.lower(), abstract.lower()]))\
                                if not all([word.is_stop, word.is_digit, word.is_punct, word.is_space])])

        doc_len: int = sum(counts.values())

        cursor.execute("""
            INSERT OR IGNORE INTO documents(doc_id, title, url, abstract, length) VALUES (?, ?, ?, ?, ?)
        """, (doc_id, title, url, abstract, doc_len))

        cursor.execute("""
            INSERT OR IGNORE INTO doc_links(doc_id, links) VALUES (?, ?)
        """, (doc_id, links))


        for w in counts:

            cursor.execute("""
                INSERT OR IGNORE INTO words(word) VALUES (?)
            """, (w,))

            cursor.execute("""
                    SELECT word_id FROM words WHERE word = ?        
                """, (w,))

            word_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO postings(word_id, doc_id, frequency) VALUES (?, ?, ?)
            """, (word_id, doc_id, counts[w]))


        if doc_id % 1000 == 0:
            connection.commit()
            connection.execute("BEGIN TRANSACTION")

    connection.close()
