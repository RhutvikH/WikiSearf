import sqlite3

def create_tables(path: str) -> None:
    """Creates required tables for wiki_searf

    Args:
        path (str): path to store the database
    """

    connection: sqlite3.Connection = sqlite3.connect(path)
    cursor: sqlite3.Cursor = connection.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents(
                doc_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                url TEXT,
                abstract TEXT,
                length INTEGER
            )
        ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS words(
                word_id INTEGER PRIMARY KEY,
                word TEXT UNIQUE NOT NULL
            )
        ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS postings(
                word_id INTEGER NOT NULL,
                doc_id INTEGER NOT NULL,
                frequency INTEGER NOT NULL,
                PRIMARY KEY (word_id, doc_id),
                FOREIGN KEY (word_id) REFERENCES words(word_id),
                FOREIGN KEY (doc_id) REFERENCES documents(doc_id)
            )
        ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS doc_links(
                doc_id INTEGER PRIMARY KEY,
                links TEXT,
                FOREIGN KEY (doc_id) REFERENCES documents(doc_id) 
            )
        ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS doc_idf(
                word_id INTEGER PRIMARY KEY,
                idf REAL,
                FOREIGN KEY (word_id) REFERENCES words(word_id) 
            )
        ''')

    connection.commit()
    connection.close()
