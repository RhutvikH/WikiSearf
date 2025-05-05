import sqlite3

def create_idf_table(path: str) -> None:
    """Creates idf table for wiki_searf

    Args:
        path (str): path to the database
    """

    connection: sqlite3.Connection = sqlite3.connect(path)
    cursor: sqlite3.Cursor = connection.cursor()

    cursor.execute('''
            ALTER TABLE words ADD COLUMN idf REAL
        ''')

    cursor.execute('''
            SELECT word_id, COUNT(DISTINCT doc_id) as df
            FROM postings
            GROUP BY word_id
        ''')

    all_lens = cursor.fetchall()
    print(all_lens[:10])
